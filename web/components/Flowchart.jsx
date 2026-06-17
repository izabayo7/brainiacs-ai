"use client";

// Renders a flowchart spec { nodes, edges } as inline SVG — light fills, black
// strokes, top-to-bottom — matching the printed-manual look. One renderer, reused for
// lesson ```flowchart blocks, exercise prompt_diagram, and ordering boxes.
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
const DIAMOND_H = 70;
const GAP = 40;
const MIN_W = 130;
const MAX_W = 380;

function nodeWidth(node) {
  if (node.shape === "connector") return 40;
  const w = (node.text || "").length * CHAR_W + PAD_X * 2;
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

export default function Flowchart({ spec }) {
  if (!spec || !Array.isArray(spec.nodes) || spec.nodes.length === 0) return null;
  const nodes = spec.nodes;
  const edges = Array.isArray(spec.edges) ? spec.edges : [];

  // Simple, robust layout: stack nodes vertically in declaration order. (Branching
  // layouts for decisions arrive with the conditionals lesson.)
  const maxW = Math.max(...nodes.map(nodeWidth));
  const svgW = maxW + 48;
  const cx = svgW / 2;
  const pos = {};
  let y = 16;
  for (const n of nodes) {
    const h = nodeHeight(n);
    pos[n.id] = { cx, cy: y + h / 2, top: y, bottom: y + h };
    y += h + GAP;
  }
  const svgH = y - GAP + 16;
  const isLegend = edges.length === 0 && nodes.length > 1;

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
        {!isLegend && edges.map((e, i) => {
          const a = pos[e.from];
          const b = pos[e.to];
          if (!a || !b) return null;
          const midY = (a.bottom + b.top) / 2;
          return (
            <g key={i}>
              <line x1={a.cx} y1={a.bottom} x2={b.cx} y2={b.top}
                    stroke="#0f172a" strokeWidth="1.4" markerEnd="url(#fc-arrow)" />
              {e.label && (
                <text x={a.cx + 8} y={midY} fontSize="11" fill="#64748b"
                      fontFamily="ui-monospace, monospace">{e.label}</text>
              )}
            </g>
          );
        })}
        {nodes.map((n) => (
          <Shape key={n.id} node={n} cx={pos[n.id].cx} cy={pos[n.id].cy} />
        ))}
      </svg>
    </div>
  );
}
