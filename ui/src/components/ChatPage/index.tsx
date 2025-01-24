import React from "react";
import { Link } from "react-router-dom";
import { useChatSession } from "./useChatSession";
import Markdown from "react-markdown";
import "./ChatPage.scss";
import { cx } from "@emotion/css";
import { useChatWindowScrolling } from "./useChatWindowScrolling";
import { useChatNavigation } from "./useChatNavigation";
import { ReactComponent as BackIcon } from "../../assets/icons/back-icon.svg";
import LoadingSpinner from "../LoadingSpinner";

const ChatPage = () => {
  const { sessionId } = useChatNavigation();

  const { messages, input, setInput, sendMessage, isSendingMessage, loading } =
    useChatSession(sessionId);

  const { chatWindowRef } = useChatWindowScrolling(messages);

  return (
    <div className="wrapper">
      <Link
        to="/chat"
        className="btn btn-light back-button d-grid justify-content-center align-items-center p-3"
      >
        <BackIcon height="20px" width="20px" />
      </Link>
      <div className="container my-3 d-flex flex-column gap-3 h-100">
        <div className="chat-window" ref={chatWindowRef}>
          {loading ? (
            <LoadingSpinner />
          ) : (
            messages.map((msg: any) => (
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
            ))
          )}
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
            disabled={isSendingMessage || loading}
          />
          <button
            disabled={isSendingMessage || loading || !Boolean(input)}
            type="submit"
            className="btn btn-primary"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
