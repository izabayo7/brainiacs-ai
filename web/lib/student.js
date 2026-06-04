"use client";

// Demo has no auth — the selected student id lives in localStorage.
const KEY = "brainiacs.studentId";

export function getStudentId() {
  if (typeof window === "undefined") return null;
  const raw = window.localStorage.getItem(KEY);
  return raw ? Number(raw) : null;
}

export function setStudentId(id) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, String(id));
}
