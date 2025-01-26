import { renderHook, act, waitFor } from "@testing-library/react";
import useAllChats from "../useAllChats";
import { axiosAuthInstance } from "../../../utils/api";
import { ChatSession } from "../../../utils/types";

jest.mock("../../../utils/api");

describe("useAllChats", () => {
  const mockChatSessions: ChatSession[] = [
    {
      id: 1,
      name: "Chat 1",
      user_email: "test1@example.com",
      created: "2025-01-01T00:00:00Z",
      updated: "2025-01-01T00:00:00Z",
    },
    {
      id: 2,
      name: "Chat 2",
      user_email: "test2@example.com",
      created: "2025-01-02T00:00:00Z",
      updated: "2025-01-02T00:00:00Z",
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("fetches chat sessions on mount", async () => {
    (axiosAuthInstance.get as jest.Mock).mockResolvedValueOnce({
      data: mockChatSessions,
    });

    const { result, rerender } = renderHook(() => useAllChats());

    expect(result.current.loading).toBe(true);

    rerender();

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
    expect(result.current.chatSessions).toEqual(mockChatSessions);
  });

  it("handles error when fetching chat sessions", async () => {
    (axiosAuthInstance.get as jest.Mock).mockRejectedValueOnce(
      new Error("Error fetching chat sessions")
    );

    const { result, rerender } = renderHook(() => useAllChats());

    expect(result.current.loading).toBe(true);
    rerender();

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.chatSessions).toEqual([]);
  });

  it("deletes a chat session", async () => {
    (axiosAuthInstance.get as jest.Mock).mockResolvedValueOnce({
      data: mockChatSessions,
    });
    (axiosAuthInstance.delete as jest.Mock).mockResolvedValueOnce({});

    const { result } = renderHook(() => useAllChats());

    await waitFor(() => {
      expect(result.current.chatSessions).toEqual(mockChatSessions);
    });
    await act(async () => {
      await result.current.deleteChat(1);
    });

    expect(result.current.chatSessions).toEqual([mockChatSessions[1]]);
  });

  it("handles error when deleting a chat session", async () => {
    (axiosAuthInstance.get as jest.Mock).mockResolvedValueOnce({
      data: mockChatSessions,
    });
    (axiosAuthInstance.delete as jest.Mock).mockRejectedValueOnce(
      new Error("Error deleting chat session")
    );

    const { result } = renderHook(() => useAllChats());

    await waitFor(() => {
      expect(result.current.chatSessions).toEqual(mockChatSessions);
    });

    await act(async () => {
      await result.current.deleteChat(1);
    });

    expect(result.current.chatSessions).toEqual(mockChatSessions);
  });
});
