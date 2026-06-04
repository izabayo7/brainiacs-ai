"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getStudentId, setStudentId } from "@/lib/student";

// No real auth in the demo — just pick who you are.
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

  if (error) return <p className="text-sm text-red-600">Could not load students: {error}</p>;

  return (
    <div className="flex items-center gap-3">
      <label htmlFor="student" className="text-sm text-gray-600">
        Signed in as
      </label>
      <select
        id="student"
        value={selected ?? ""}
        onChange={(e) => handleSelect(Number(e.target.value))}
        className="rounded-lg border border-gray-300 px-3 py-2 text-sm bg-white"
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
