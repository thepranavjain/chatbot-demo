export interface ChatSession {
  id: number;
  name: string;
  user_email: string;
  created: string;
  updated: string;
}

export enum MessageRole {
  USER = "user",
  SYSTEM = "system",
}

export interface ChatMessage {
  id: number;
  role: MessageRole;
  content: string;
  session_id: number;
  created: string;
  updated: string;
}
