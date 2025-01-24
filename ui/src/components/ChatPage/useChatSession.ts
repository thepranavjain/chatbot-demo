import { useEffect, useState } from "react";
import { axiosAuthInstance } from "../../utils/api";

export const useChatSession = (sessionId?: string | null) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    const fetchMessages = async () => {
      if (sessionId) {
        const response = await axiosAuthInstance.get(
          `/messaging/chat-session/messages/${sessionId}`
        );
        setMessages(response.data);
        // Scroll to the bottom of the chat
        window.scrollTo(0, document.body.scrollHeight);
      }
    };
    fetchMessages();
  }, [sessionId]);

  const sendMessage = async () => {
    if (!input) return;

    const response = await axiosAuthInstance.post("/messaging/message", {
      content: input,
      session_id: sessionId || undefined,
    });

    setMessages((prevMessages: any[]) => [
      ...prevMessages,
      {
        id: Math.random(),
        content: input,
        session_id: sessionId,
        role: "user",
      },
      response.data,
    ]);
    setInput("");
  };

  return { messages, input, setInput, sendMessage };
};
