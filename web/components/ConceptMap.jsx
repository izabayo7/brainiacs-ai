import ConceptCard from "./ConceptCard";

// The prerequisite graph as an ordered list of cards. Responsive: a single
// column that the dashboard places in a left pane on wide screens.
export default function ConceptMap({ concepts, onOpen }) {
  return (
    <div className="space-y-3">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">
        Concept map
      </h2>
      {concepts.map((c) => (
        <ConceptCard key={c.id} concept={c} onOpen={onOpen} />
      ))}
    </div>
  );
}
