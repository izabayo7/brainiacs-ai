"use client";

// Renders a flowchart spec { nodes, edges } as inline SVG — light fills, black
// strokes — matching the printed-manual look. One renderer, reused for lesson
// ```flowchart blocks and exercise prompt_diagram.
//
// Layout is driven by the GRAPH, not the node declaration order: nodes are ranked
// by their forward edges, decision branches go into separate columns, every edge is
// routed from its own `from` to its own `to`, and a back-edge (an edge pointing to
// an earlier rank) is drawn out through a left channel and back up — which is what
// makes a loop actually look like a loop.
//
// Shapes: terminal = oval, io = parallelogram, process = rectangle,
//         decision = diamond, connector = small circle.
// A spec with nodes and no edges renders as a labelled legend.

const FILL = {
  terminal: "#eef2ff",
  io: "#ecfeff",
  process: "#f8fafc",
  decision: "#fff7ed",
  connector: "#ffffff",
};

const CHAR_W = 7.3;
const PAD_X = 26;
const NODE_H = 46;
const DIAMOND_H = 72;
const MIN_W = 130;
const MAX_W = 380;
const COL_GAP = 56; // horizontal space between columns
const RANK_GAP = 34; // vertical space between ranks
const MARGIN = 20;
const CHANNEL = 36; // reserved left lane that back-edges travel up

function nodeWidth(node) {
  if (node.shape === "connector") return 40;
  const base = (node.text || "").length * CHAR_W + PAD_X * 2;
  // A diamond wastes its corners, so widen it to keep the label inside.
  const w = node.shape === "decision" ? base * 1.3 : base;
  return Math.max(MIN_W, Math.min(MAX_W, w));
}
function nodeHeight(node) {
  if (node.shape === "connector") return 40;
  if (node.shape === "decision") return DIAMOND_H;
  return NODE_H;
}

function Shape({ node, cx, cy }) {
  const w = nodeWidth(node);
  const h = nodeHeight(node);
  const x = cx - w / 2;
  const y = cy - h / 2;
  const stroke = "#0f172a";
  const fill = FILL[node.shape] || "#ffffff";
  const common = { fill, stroke, strokeWidth: 1.6 };
  let shape;
  if (node.shape === "terminal") {
    shape = <rect x={x} y={y} width={w} height={h} rx={h / 2} ry={h / 2} {...common} />;
  } else if (node.shape === "process") {
    shape = <rect x={x} y={y} width={w} height={h} rx={6} {...common} />;
  } else if (node.shape === "io") {
    const s = 16;
    shape = <polygon points={`${x + s},${y} ${x + w},${y} ${x + w - s},${y + h} ${x},${y + h}`} {...common} />;
  } else if (node.shape === "decision") {
    shape = <polygon points={`${cx},${y} ${x + w},${cy} ${cx},${y + h} ${x},${cy}`} {...common} />;
  } else if (node.shape === "connector") {
    shape = <circle cx={cx} cy={cy} r={h / 2} {...common} />;
  } else {
    shape = <rect x={x} y={y} width={w} height={h} rx={6} {...common} />;
  }
  return (
    <g>
      {shape}
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
            fontSize="13" fontFamily="ui-monospace, monospace" fill="#0f172a">
        {node.text}
      </text>
    </g>
  );
}

// A label with a white halo so it stays readable where it crosses a line.
function EdgeLabel({ x, y, anchor, children }) {
  return (
    <text x={x} y={y} textAnchor={anchor} fontSize="11" fill="#475569"
          fontFamily="ui-monospace, monospace"
          stroke="#ffffff" strokeWidth="3" paintOrder="stroke"
          dominantBaseline="central">
      {children}
    </text>
  );
}

// Lay the graph out: ranks (y) from forward edges, columns (x) so decision
// branches sit side by side, and a flag for which edges are back-edges.
function layout(nodes, edges) {
  const byId = {};
  nodes.forEach((n) => { byId[n.id] = n; });
  const valid = edges.filter((e) => byId[e.from] && byId[e.to]);

  const out = {};
  nodes.forEach((n) => { out[n.id] = []; });
  valid.forEach((e) => { out[e.from].push(e); });

  // Back-edge = an edge whose target is still on the DFS stack (i.e. an ancestor).
  // Removing these breaks the cycle so ranks are well defined.
  const back = new Set();
  const state = {}; // undefined = unseen, 1 = on stack, 2 = done
  const dfs = (id) => {
    state[id] = 1;
    for (const e of out[id]) {
      if (state[e.to] === 1) back.add(e);
      else if (!state[e.to]) dfs(e.to);
    }
    state[id] = 2;
  };
  const indeg = {};
  nodes.forEach((n) => { indeg[n.id] = 0; });
  valid.forEach((e) => { indeg[e.to] += 1; });
  const roots = nodes.filter((n) => indeg[n.id] === 0).map((n) => n.id);
  (roots.length ? roots : [nodes[0].id]).forEach((id) => { if (!state[id]) dfs(id); });
  nodes.forEach((n) => { if (!state[n.id]) dfs(n.id); }); // disconnected pieces

  const forward = valid.filter((e) => !back.has(e));
  const fout = {};
  nodes.forEach((n) => { fout[n.id] = []; });
  const findeg = {};
  nodes.forEach((n) => { findeg[n.id] = 0; });
  forward.forEach((e) => { fout[e.from].push(e); findeg[e.to] += 1; });

  // Ranks via longest path (Kahn topological order over forward edges).
  const rank = {};
  nodes.forEach((n) => { rank[n.id] = 0; });
  const remaining = { ...findeg };
  const queue = nodes.filter((n) => findeg[n.id] === 0).map((n) => n.id);
  const topo = [];
  while (queue.length) {
    const id = queue.shift();
    topo.push(id);
    for (const e of fout[id]) {
      rank[e.to] = Math.max(rank[e.to], rank[id] + 1);
      if ((remaining[e.to] -= 1) === 0) queue.push(e.to);
    }
  }
  nodes.forEach((n) => { if (!topo.includes(n.id)) topo.push(n.id); });

  // Columns: a node's first forward child stays in its column; later children
  // (the second exit of a decision) shift right. A merge pulls back toward the
  // smallest column its parents offered.
  const col = {};
  for (const id of topo) {
    if (col[id] === undefined) col[id] = 0;
    const base = col[id];
    fout[id].forEach((e, k) => {
      const want = base + k; // k === 0 -> same column
      col[e.to] = col[e.to] === undefined ? want : Math.min(col[e.to], want);
    });
  }

  const maxRank = Math.max(...nodes.map((n) => rank[n.id]));
  const maxCol = Math.max(...nodes.map((n) => col[n.id]));

  const colW = [];
  for (let c = 0; c <= maxCol; c += 1) {
    const ws = nodes.filter((n) => col[n.id] === c).map(nodeWidth);
    colW[c] = ws.length ? Math.max(...ws) : MIN_W;
  }
  const rankH = [];
  for (let r = 0; r <= maxRank; r += 1) {
    const hs = nodes.filter((n) => rank[n.id] === r).map(nodeHeight);
    rankH[r] = hs.length ? Math.max(...hs) : NODE_H;
  }

  const hasBack = back.size > 0;
  const leftPad = MARGIN + (hasBack ? CHANNEL : 0);
  const colCenter = [];
  let x = leftPad;
  for (let c = 0; c <= maxCol; c += 1) {
    colCenter[c] = x + colW[c] / 2;
    x += colW[c] + COL_GAP;
  }
  const svgW = x - COL_GAP + MARGIN;

  const rankTop = [];
  let y = MARGIN;
  for (let r = 0; r <= maxRank; r += 1) {
    rankTop[r] = y;
    y += rankH[r] + RANK_GAP;
  }
  const svgH = y - RANK_GAP + MARGIN;

  const pos = {};
  const colRight = []; // rightmost edge of any node in each column, for gutter routing
  nodes.forEach((n) => {
    const w = nodeWidth(n);
    const h = nodeHeight(n);
    const cx = colCenter[col[n.id]];
    const cy = rankTop[rank[n.id]] + rankH[rank[n.id]] / 2;
    pos[n.id] = {
      cx, cy, shape: n.shape, rank: rank[n.id],
      top: cy - h / 2, bottom: cy + h / 2, left: cx - w / 2, right: cx + w / 2,
    };
    colRight[col[n.id]] = Math.max(colRight[col[n.id]] ?? 0, cx + w / 2);
  });

  return { pos, fout, forward, back, svgW, svgH, leftPad, colRight, col };
}

export default function Flowchart({ spec }) {
  if (!spec || !Array.isArray(spec.nodes) || spec.nodes.length === 0) return null;
  const nodes = spec.nodes;
  const edges = Array.isArray(spec.edges) ? spec.edges : [];

  // No edges: render as a labelled legend (plain vertical stack).
  if (edges.length === 0) {
    const maxW = Math.max(...nodes.map(nodeWidth));
    const svgW = maxW + 48;
    const cx = svgW / 2;
    let y = 16;
    const placed = nodes.map((n) => {
      const h = nodeHeight(n);
      const cy = y + h / 2;
      y += h + RANK_GAP;
      return { n, cy };
    });
    const svgH = y - RANK_GAP + 16;
    return (
      <div className="my-5 overflow-x-auto rounded-xl border border-line bg-white p-4">
        <svg viewBox={`0 0 ${svgW} ${svgH}`} width="100%" style={{ maxWidth: svgW }}
             role="img" aria-label="flowchart legend">
          {placed.map(({ n, cy }) => <Shape key={n.id} node={n} cx={cx} cy={cy} />)}
        </svg>
      </div>
    );
  }

  const { pos, fout, forward, back, svgW, svgH, leftPad, colRight, col } = layout(nodes, edges);

  const forwardEdge = (e, i) => {
    const a = pos[e.from];
    const b = pos[e.to];
    if (!a || !b) return null;
    const sameCol = Math.abs(a.cx - b.cx) < 0.5;
    const idx = fout[e.from].indexOf(e);
    const fromDecision = a.shape === "decision";

    let d;
    let label = null;
    if (fromDecision && idx > 0 && sameCol && b.rank > a.rank + 1) {
      // A decision's second exit that rejoins the spine below an intervening node
      // (e.g. an IF inside a loop: the "No" skips the if-body and lands on the
      // merge). A straight line would cut through that node, so route out to a
      // right-side gutter, down, and back into the target's right side.
      const gutter = (colRight[col[e.from]] ?? a.right) + COL_GAP / 2;
      d = `M ${a.right} ${a.cy} L ${gutter} ${a.cy} L ${gutter} ${b.cy} L ${b.right} ${b.cy}`;
      if (e.label) label = { x: gutter, y: a.cy - 9, anchor: "middle", text: e.label };
    } else if (sameCol) {
      d = `M ${a.cx} ${a.bottom} L ${b.cx} ${b.top}`;
      if (e.label) label = { x: a.cx + 10, y: (a.bottom + b.top) / 2, anchor: "start", text: e.label };
    } else if (fromDecision && idx > 0 && b.cx > a.cx) {
      // Second exit of a decision: leave from the right vertex, then drop in.
      d = `M ${a.right} ${a.cy} L ${b.cx} ${a.cy} L ${b.cx} ${b.top}`;
      if (e.label) label = { x: (a.right + b.cx) / 2, y: a.cy - 9, anchor: "middle", text: e.label };
    } else {
      // General column change: down, across, down.
      const midY = (a.bottom + b.top) / 2;
      d = `M ${a.cx} ${a.bottom} L ${a.cx} ${midY} L ${b.cx} ${midY} L ${b.cx} ${b.top}`;
      if (e.label) label = { x: (a.cx + b.cx) / 2, y: midY - 9, anchor: "middle", text: e.label };
    }
    return { key: `f${i}`, d, label };
  };

  const backEdge = (e, i) => {
    const a = pos[e.from];
    const b = pos[e.to];
    if (!a || !b) return null;
    const channelX = leftPad - CHANNEL / 2;
    // Out the left side of the source, up the channel, back into the target's left vertex.
    const d = `M ${a.left} ${a.cy} L ${channelX} ${a.cy} L ${channelX} ${b.cy} L ${b.left} ${b.cy}`;
    // Sit the label near the top of the channel (just under the target), where the
    // lane is clear, rather than at the mid-point where it collides with body nodes.
    const label = e.label ? { x: channelX + 6, y: b.cy + 18, anchor: "start", text: e.label } : null;
    return { key: `b${i}`, d, label };
  };

  const paths = [
    ...forward.map(forwardEdge),
    ...back.size ? [...back].map(backEdge) : [],
  ].filter(Boolean);

  return (
    <div className="my-5 overflow-x-auto rounded-xl border border-line bg-white p-4">
      <svg viewBox={`0 0 ${svgW} ${svgH}`} width="100%" style={{ maxWidth: svgW }}
           role="img" aria-label="flowchart">
        <defs>
          <marker id="fc-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
                  markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#0f172a" />
          </marker>
        </defs>
        {paths.map((p) => (
          <path key={p.key} d={p.d} fill="none" stroke="#0f172a" strokeWidth="1.5"
                markerEnd="url(#fc-arrow)" />
        ))}
        {nodes.map((n) => <Shape key={n.id} node={n} cx={pos[n.id].cx} cy={pos[n.id].cy} />)}
        {paths.map((p) => p.label && (
          <EdgeLabel key={`${p.key}l`} x={p.label.x} y={p.label.y} anchor={p.label.anchor}>
            {p.label.text}
          </EdgeLabel>
        ))}
      </svg>
    </div>
  );
}
