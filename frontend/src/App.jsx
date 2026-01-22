import React, { useState } from "react";
import { sendQuery } from "./api";
import "./styles.css";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text:
        "Hello! I am your Indian Legal Assistant. Ask anything about IPC, CrPC, Evidence Act, or Indian court procedures.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { id: Date.now(), sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendQuery(userMsg.text);
      const botMsg = {
        id: Date.now() + 1,
        sender: "bot",
        text: res.answer,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errorMsg = {
        id: Date.now() + 2,
        sender: "bot",
        text: "⚠️ Error: " + err.message,
      };
      setMessages((prev) => [...prev, errorMsg]);
    }

    setLoading(false);
  };

  return (
    <>
      <div className="header">
        <span>⚖️</span> Indian Court Guidance Chatbot
      </div>

      <div className="chat-container">
        <div className="messages-area">
          {messages.map((m) => (
            <div key={m.id} className={`message-row ${m.sender}`}>
              <div className="message-bubble">
                {m.sender === "bot" ? (
                  <ReactMarkdown>{m.text}</ReactMarkdown>
                ) : (
                  m.text
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="input-area">
          <input
            className="input-box"
            value={input}
            placeholder="Ask about IPC / CrPC / Article..."
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading}
          >
            Send
          </button>
        </div>
      </div>
    </>
  );
}
