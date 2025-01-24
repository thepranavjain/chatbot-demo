import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { axiosAuthInstance } from "../../utils/api";
import { ChatMessage, SendMessageRes } from "../../utils/types";

export const useChatSession = (sessionId?: string | null) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMessages = async () => {
      if (sessionId) {
        setLoading(true);
        const response = await axiosAuthInstance.get(
          `/messaging/chat-session/${sessionId}/messages`
        );
        setMessages(response.data);
        setLoading(false);
        // Scroll to the bottom of the chat
        window.scrollTo(0, document.body.scrollHeight);
      }
    };
    fetchMessages();
  }, [sessionId]);

  const sendMessage = async () => {
    if (!input) return;

    setIsSendingMessage(true);
    const response = await axiosAuthInstance.post("/messaging/message", {
      content: input,
      session_id: sessionId || undefined,
    });
    setIsSendingMessage(false);

    const { user_message, reply } = response.data as SendMessageRes;

    setMessages((prevMessages: any[]) => [
      ...prevMessages,
      user_message,
      reply,
    ]);
    setInput("");

    if (!sessionId) {
      navigate(`/chat/${reply.session_id}`);
    }
  };

  return { messages, input, setInput, sendMessage, loading, isSendingMessage };
};
