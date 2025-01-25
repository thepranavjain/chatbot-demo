import { useState, useEffect } from "react";
import { ChatSession } from "../../utils/types";
import { axiosAuthInstance } from "../../utils/api";

const useAllChats = () => {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(false);
  const [isApiCallOngoing, setIsApiCallOngoing] = useState(false);

  const deleteChat = async (sessionId: number) => {
    setIsApiCallOngoing(true);
    try {
      await axiosAuthInstance.delete(`/messaging/chat-session/${sessionId}`);
      setChatSessions((prevChatSessions) =>
        prevChatSessions.filter(({ id }) => id !== sessionId)
      );
    } catch (error) {
      console.error("Error deleting chat sessions:", error);
    } finally {
      setIsApiCallOngoing(false);
    }
  };

  useEffect(() => {
    const fetchChatSessions = async () => {
      setLoading(true);
      try {
        const response = await axiosAuthInstance.get("/messaging/chat-session");
        setChatSessions(response.data);
      } catch (error) {
        console.error("Error fetching chat sessions:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchChatSessions();
  }, []);

  return { chatSessions, deleteChat, isApiCallOngoing, loading };
};

export default useAllChats;
