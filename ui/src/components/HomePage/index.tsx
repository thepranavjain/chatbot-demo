import React, { useContext, useEffect } from "react";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { auth } from "../../firebase";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import { ReactComponent as GoogleIcon } from "../../assets/icons/google-icon.svg";

const HomePage = () => {
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext?.user) {
      navigate("/chat");
    }

    return () => {};
  }, [authContext?.user, navigate]);

  const handleGoogleLogin = async () => {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
    } catch (error: any) {
      console.error("Error during login:", error.message);
    }
  };

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
