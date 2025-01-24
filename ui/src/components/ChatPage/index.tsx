import React from "react";
import { Link } from "react-router-dom";
import { useChatSession } from "./useChatSession"; // Import the custom hook
import Markdown from "react-markdown";
import "./ChatPage.scss";
import { cx } from "@emotion/css";
import { useChatWindowScrolling } from "./useChatWindowScrolling"; // Import the new custom hook
import { useChatNavigation } from "./useChatNavigation"; // Import the new custom hook

const ChatPage = () => {
  const { sessionId } = useChatNavigation();

  // Use the custom hook
  const { messages, input, setInput, sendMessage } = useChatSession(sessionId);

  // Use the custom hook for chat window scrolling
  const { chatWindowRef } = useChatWindowScrolling(messages);

  return (
    <div className="wrapper">
      <Link to="/chat" className="btn btn-secondary back-button">
        Back
      </Link>
      <div className="container my-3 d-flex flex-column gap-3 h-100">
        <div className="chat-window" ref={chatWindowRef}>
          {messages.map((msg: any) => (
            <div
              key={msg.id}
              className={cx(
                "message d-flex",
                msg.role === "user"
                  ? "text-end justify-content-end"
                  : "text-start justify-content-start"
              )}
            >
              <div
                className={cx("message-content", {
                  "bg-primary": msg.role === "user",
                  "bg-light": msg.role !== "user",
                })}
              >
                <Markdown>{msg.content}</Markdown>
              </div>
            </div>
          ))}
        </div>
        <form
          className="input-group"
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
        >
          <input
            type="text"
            className="form-control"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            autoFocus
          />
          <button type="submit" className="btn btn-primary">
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
