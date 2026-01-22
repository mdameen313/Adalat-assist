// frontend/src/api.js
export async function sendQuery(question) {
  const resp = await fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question })
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || "Server error");
  }
  return resp.json(); // { answer: "...", sources: [...] }
}
