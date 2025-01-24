import React from "react";
import useLogin from "../../hooks/useLogin";

const AllChatsPage: React.FC = () => {
  const { user, handleLogout } = useLogin();

  return (
    <>
      <nav className="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
        <div className="container-fluid">
          <div className="navbar-brand">Welcome {user?.displayName}!</div>
          <div className="d-flex ms-auto">
            <button className="btn btn-danger" onClick={() => handleLogout()}>
              Logout
            </button>
          </div>
        </div>
      </nav>
    </>
  );
};

export default AllChatsPage;
