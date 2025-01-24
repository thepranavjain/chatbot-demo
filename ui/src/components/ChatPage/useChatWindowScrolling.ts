import { useEffect, useRef } from "react";

export const useChatWindowScrolling = (messages: any[]) => {
  const chatWindowRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // Scroll to the bottom of the chat window when messages change
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  return { chatWindowRef };
};
