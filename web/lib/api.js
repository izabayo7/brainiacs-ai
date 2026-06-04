// Thin client for the FastAPI backend. All calls run in the browser.

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail || detail;
    } catch {
      // body wasn't JSON; keep the status text
    }
    const error = new Error(detail);
    error.status = res.status;
    throw error;
  }
  return res.json();
}

export const api = {
  listStudents: () => request("/students"),
  listConcepts: (studentId) => request(`/concepts?student_id=${studentId}`),
  getConcept: (conceptId, studentId) =>
    request(`/concepts/${conceptId}?student_id=${studentId}`),
  getProgress: (studentId) => request(`/progress/${studentId}`),
  generateQuiz: (conceptId, studentId) =>
    request(`/quiz/${conceptId}/generate?student_id=${studentId}`, { method: "POST" }),
  submitQuiz: (conceptId, payload) =>
    request(`/quiz/${conceptId}/submit`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
