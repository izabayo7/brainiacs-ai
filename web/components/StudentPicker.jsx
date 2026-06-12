"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getStudentId, setStudentId } from "@/lib/student";

// No real auth in the demo — pick which learner you are.
export default function StudentPicker({ onChange }) {
  const [students, setStudents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .listStudents()
      .then((list) => {
        setStudents(list);
        const existing = getStudentId();
        const initial = existing && list.some((s) => s.id === existing) ? existing : list[0]?.id;
        if (initial) {
          setSelected(initial);
          setStudentId(initial);
          onChange?.(initial);
        }
      })
      .catch((e) => setError(e.message));
  }, []);

  function handleSelect(id) {
    setSelected(id);
    setStudentId(id);
    onChange?.(id);
  }

  if (error) return <p className="text-sm text-red-600">API offline: {error}</p>;

  return (
    <div className="flex items-center gap-2 rounded-xl border border-line bg-white px-3 py-1.5 shadow-card">
      <span className="grid h-7 w-7 place-items-center rounded-full bg-brand-600 text-xs font-semibold text-white">
        {(students.find((s) => s.id === selected)?.name || "?").slice(0, 1)}
      </span>
      <select
        aria-label="Select learner"
        value={selected ?? ""}
        onChange={(e) => handleSelect(Number(e.target.value))}
        className="bg-transparent text-sm font-medium text-ink focus:outline-none"
      >
        {students.map((s) => (
          <option key={s.id} value={s.id}>
            {s.name}
          </option>
        ))}
      </select>
    </div>
  );
}
