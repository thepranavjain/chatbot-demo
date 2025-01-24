import React, { useContext } from "react";
import { signOut } from "firebase/auth";
import { auth } from "../../firebase";
import { AuthContext } from "../../context/AuthContext";

const AllChatsPage: React.FC = () => {
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error("AuthContext must be used within an AuthProvider");
  }

  const { user } = authContext;

  const handleLogout = () => {
    signOut(auth)
      .then(() => console.log("User signed out"))
      .catch((error) => console.error("Error during logout:", error));
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Welcome, {user?.displayName || "User"}!</h1>
      <button
        onClick={handleLogout}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default AllChatsPage;
