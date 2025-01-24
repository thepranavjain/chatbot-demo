import { useState, useEffect } from "react";
import { ChatSession } from "../../utils/types";
import { axiosAuthInstance } from "../../utils/api";

const useAllChats = () => {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);

  useEffect(() => {
    const fetchChatSessions = async () => {
      try {
        const response = await axiosAuthInstance.get("/messaging/chat-session");
        setChatSessions(response.data);
      } catch (error) {
        console.error("Error fetching chat sessions:", error);
      }
    };

    fetchChatSessions();
  }, []);

  return { chatSessions };
};

export default useAllChats;
