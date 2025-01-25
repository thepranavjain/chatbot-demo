import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { axiosAuthInstance } from "../../utils/api";
import { ChatMessage, SendMessageRes } from "../../utils/types";

interface EditMode {
  id: number;
  content: string;
}

export const useChatSession = (sessionId?: string | null) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [editMode, setEditMode] = useState<EditMode | null>(null);
  const navigate = useNavigate();

  const handleEdit = (msg: EditMode) => {
    setEditMode({ id: msg.id, content: msg.content });
  };

  const closeEdit = () => {
    setEditMode(null);
  };

  const handleDelete = async (msgId: number) => {
    setIsSendingMessage(true);
    try {
      await axiosAuthInstance.delete(`/messaging/message/${msgId}`);
      // Update messages state by filtering out the deleted message
      setMessages((prevMessages) =>
        prevMessages.filter((msg) => msg.id !== msgId)
      );
    } catch (error) {
      console.error("Error deleting message:", error);
    } finally {
      setIsSendingMessage(false);
    }
  };

  const handleEditSubmit = async (e: React.FormEvent, msgId: number) => {
    e.preventDefault();
    if (!editMode) return;

    setIsSendingMessage(true);
    try {
      const response = await axiosAuthInstance.patch(
        `/messaging/message/${editMode.id}`,
        {
          content: editMode.content,
        }
      );
      // Update messages state with the edited message
      const updatedMessage: ChatMessage = response.data;
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === updatedMessage.id ? updatedMessage : msg
        )
      );
    } catch (error) {
      console.error("Error updating message:", error);
    } finally {
      setIsSendingMessage(false);
      setEditMode(null);
    }
  };

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

  return {
    messages,
    input,
    setInput,
    sendMessage,
    loading,
    isSendingMessage,
    editMode,
    closeEdit,
    handleDelete,
    handleEdit,
    handleEditSubmit,
  };
};
