import React from "react";
import { Link } from "react-router-dom";
import { useChatSession } from "./useChatSession";
import Markdown from "react-markdown";
import "./ChatPage.scss";
import { cx } from "@emotion/css";
import { useChatWindowScrolling } from "./useChatWindowScrolling";
import { useChatNavigation } from "./useChatNavigation";
import { ReactComponent as BackIcon } from "../../assets/icons/back-icon.svg";
import { ReactComponent as DeleteIcon } from "../../assets/icons/delete-icon.svg";
import { ReactComponent as EditIcon } from "../../assets/icons/edit-icon.svg";
import { ReactComponent as CloseIcon } from "../../assets/icons/close-icon.svg";
import LoadingSpinner from "../LoadingSpinner";
import { MessageRole } from "../../utils/types";

const ChatPage = () => {
  const { sessionId } = useChatNavigation();

  const {
    messages,
    input,
    setInput,
    sendMessage,
    isSendingMessage,
    loading,
    editMode,
    closeEdit,
    handleDelete,
    handleEdit,
    handleEditSubmit,
  } = useChatSession(sessionId);

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
            messages.map((msg) => (
              <div
                key={msg.id}
                className={cx(
                  "message d-flex align-items-center",
                  msg.role === MessageRole.USER
                    ? "text-end justify-content-end"
                    : "text-start justify-content-start"
                )}
              >
                {msg.role === MessageRole.USER && (
                  <div className="edit-icons justify-content-center align-items-center">
                    {editMode ? (
                      <button
                        className="btn btn-light m-2"
                        onClick={() => closeEdit()}
                        disabled={isSendingMessage}
                      >
                        <CloseIcon height="16px" width="16px" />
                      </button>
                    ) : (
                      <>
                        <button
                          className="btn btn-light m-2"
                          onClick={() => handleEdit(msg)}
                          disabled={isSendingMessage}
                        >
                          <EditIcon height="16px" width="16px" />
                        </button>
                        <button
                          className="btn btn-light m-2"
                          onClick={() => handleDelete(msg.id)}
                          disabled={isSendingMessage}
                        >
                          <DeleteIcon height="16px" width="16px" />
                        </button>
                      </>
                    )}
                  </div>
                )}
                <div
                  className={cx("message-content", {
                    "bg-primary": msg.role === MessageRole.USER,
                    "bg-light": msg.role !== MessageRole.USER,
                    "w-100": Boolean(editMode?.id),
                  })}
                >
                  {editMode && editMode?.id === msg.id ? (
                    <form
                      className="w-100"
                      onSubmit={(e) => handleEditSubmit(e, msg.id)}
                    >
                      <input
                        type="text"
                        className="w-100"
                        value={editMode.content}
                        onChange={(e) =>
                          handleEdit({
                            ...editMode,
                            content: e.target.value,
                          })
                        }
                        autoFocus
                      />
                    </form>
                  ) : (
                    <>
                      <Markdown>{msg.content}</Markdown>
                    </>
                  )}
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
