import { useContext } from "react";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { AuthContext } from "../context/AuthContext";

const useLogin = () => {
  const authContext = useContext(AuthContext);

  const handleLogout = () => {
    signOut(auth)
      .then(() => console.log("User signed out"))
      .catch((error) => console.error("Error during logout:", error));
  };

  return { user: authContext?.user, handleLogout };
};

export default useLogin;
