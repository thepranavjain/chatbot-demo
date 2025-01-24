import React from "react";
import useHomePage from "./useHomePage"; // Import the custom hook
import { ReactComponent as GoogleIcon } from "../../assets/icons/google-icon.svg";

const HomePage = () => {
  const { handleGoogleLogin } = useHomePage(); // Use the custom hook

  return (
    <div className="vh-100 vw-100 d-grid justify-content-center align-items-center">
      <div className="d-flex flex-column gap-3 align-items-center">
        <div>Welcome to my Chatbot app!</div>
        <div>Please login</div>
        <button
          onClick={handleGoogleLogin}
          className="btn btn-outline-primary d-grid justify-content-center align-items-center p-3"
        >
          <GoogleIcon height={"20px"} width={"20px"} />
        </button>
      </div>
    </div>
  );
};

export default HomePage;
