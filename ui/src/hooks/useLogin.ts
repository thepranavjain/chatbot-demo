import { useContext } from "react";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { AuthContext } from "../context/AuthContext";

const useLogin = () => {
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error("User should be logged in ");
  }

  const { user, loading } = authContext;

  const handleLogout = () => {
    signOut(auth)
      .then(() => console.log("User signed out"))
      .catch((error) => console.error("Error during logout:", error));
  };

  return { user, authLoading: loading, handleLogout };
};

export default useLogin;
