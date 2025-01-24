import React from "react";
import { Navigate } from "react-router-dom";
import useLogin from "../../hooks/useLogin";
import LoadingSpinner from "../LoadingSpinner";

interface PrivateRouteProps {
  children: JSX.Element;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const { user, authLoading, handleLogout } = useLogin();

  return authLoading ? (
    <div className="vh-100 vw-100 d-grid justify-content-center align-items-center">
      <LoadingSpinner />
    </div>
  ) : user ? (
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
      {children}
    </>
  ) : (
    <Navigate to="/" />
  );
};

export default PrivateRoute;
