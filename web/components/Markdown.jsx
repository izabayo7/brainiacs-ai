"use client";

import ReactMarkdown from "react-markdown";
import Flowchart from "./Flowchart";

// react-markdown wrapper that renders ```flowchart blocks (JSON {nodes, edges}) as
// SVG diagrams. All other code blocks fall through to the normal (dark) styling.
function FlowchartBlock({ source }) {
  try {
    return <Flowchart spec={JSON.parse(source)} />;
  } catch {
    // Never lose content: show the source if the JSON is malformed.
    return <pre className="bg-slate-900 text-slate-100 rounded-xl p-4 my-4 overflow-x-auto text-sm font-mono">{source}</pre>;
  }
}

const components = {
  code({ className, children, ...props }) {
    const lang = /language-(\w+)/.exec(className || "")?.[1];
    if (lang === "flowchart") {
      return <FlowchartBlock source={String(children).replace(/\n$/, "")} />;
    }
    return (
      <code className={className} {...props}>
        {children}
      </code>
    );
  },
  // Don't wrap a flowchart block in <pre> (which would apply dark code styling).
  pre({ children }) {
    const child = Array.isArray(children) ? children[0] : children;
    const cls = child?.props?.className || "";
    if (cls.includes("language-flowchart")) return <>{children}</>;
    return <pre>{children}</pre>;
  },
};

export default function Markdown({ children }) {
  return <ReactMarkdown components={components}>{children}</ReactMarkdown>;
}
