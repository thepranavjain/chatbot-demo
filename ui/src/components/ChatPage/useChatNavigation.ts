import { useLocation } from "react-router-dom";

export const useChatNavigation = () => {
  const location = useLocation();
  const sessionId = location.pathname.includes("chat/new")
    ? null
    : location.pathname.split("/").pop();

  return { sessionId };
};
