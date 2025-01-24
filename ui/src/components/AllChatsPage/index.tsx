import React from "react";
import useAllChats from "./useAllChats";
import { Link } from "react-router-dom";

const AllChatsPage: React.FC = () => {
  const { chatSessions } = useAllChats();

  return (
    <div className="container py-3">
      <Link to={"/chat/new"}>
        <button className="btn btn-primary mb-3">+ New Chat</button>
      </Link>
      <div className="row">
        {chatSessions.map((session) => (
          <div className="col-12 col-md-4 mb-3" key={session.id}>
            <a
              href={`/chat/${session.id}`}
              className="card"
              style={{ textDecoration: "none", color: "inherit" }}
            >
              <div className="card-body">
                <h5 className="card-title">{session.name}</h5>
                <p className="card-text">
                  {new Date(session.created).toDateString()}
                </p>
              </div>
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AllChatsPage;
