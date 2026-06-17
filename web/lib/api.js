"use client";

// Client for the FastAPI backend. Authenticated calls attach the backend JWT that
// NextAuth stored in the session.
import { getSession } from "next-auth/react";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request(path, { auth = true, ...options } = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (auth) {
    const session = await getSession();
    if (session?.backendToken) headers.Authorization = `Bearer ${session.backendToken}`;
  }
  const res = await fetch(`${BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail || detail;
    } catch {
      /* non-JSON body */
    }
    const error = new Error(detail);
    error.status = res.status;
    throw error;
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // auth (no bearer needed)
  register: (body) =>
    request("/auth/register", { method: "POST", body: JSON.stringify(body), auth: false }),

  // authenticated
  listConcepts: () => request("/concepts"),
  getConcept: (conceptId) => request(`/concepts/${conceptId}`),
  askTutor: (conceptId, question) =>
    request(`/concepts/${conceptId}/ask`, { method: "POST", body: JSON.stringify({ question }) }),
  getProgress: () => request("/progress"),
  generateQuiz: (conceptId) => request(`/quiz/${conceptId}/generate`, { method: "POST" }),
  submitQuiz: (conceptId, payload) =>
    request(`/quiz/${conceptId}/submit`, { method: "POST", body: JSON.stringify(payload) }),
};
