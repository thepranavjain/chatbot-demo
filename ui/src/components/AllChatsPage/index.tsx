import React from "react";
import "./AllChatsPage.scss";
import useAllChats from "./useAllChats";
import { Link } from "react-router";
import { ReactComponent as DeleteIcon } from "../../assets/icons/close-icon.svg";
import LoadingSpinner from "../LoadingSpinner";
import { cx } from "@emotion/css";

const AllChatsPage: React.FC = () => {
  const { chatSessions, deleteChat, isApiCallOngoing, loading } = useAllChats();

  return (
    <div className="container py-3">
      <Link to={"/chat/new"}>
        <button className="btn btn-primary mb-3">+ New Chat</button>
      </Link>
      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="row">
          {chatSessions.map((session) => (
            <div
              className="chat-session col-12 col-md-4 mb-3 position-relative"
              key={session.id}
            >
              <Link
                to={`/chat/${session.id}`}
                className={cx("card chat-session-card", {
                  "disabled-link": isApiCallOngoing,
                })}
                style={{ textDecoration: "none", color: "inherit" }}
              >
                <div className="card-body">
                  <h5 className="card-title">{session.name}</h5>
                  <p className="card-text">
                    {new Date(session.created).toDateString()}
                  </p>
                </div>
              </Link>
              <button
                onClick={() => deleteChat(session.id)}
                className="btn btn-light delete-button p-1"
                disabled={isApiCallOngoing}
                data-testid={`delete-chat-${session.id}`}
              >
                <DeleteIcon height="20px" className="delete-icon" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AllChatsPage;
