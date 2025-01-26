import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import AllChatsPage from "../index";
import useAllChats from "../useAllChats";

jest.mock("../useAllChats");

describe("AllChatsPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (useAllChats as jest.Mock).mockReturnValue({
      chatSessions: [],
      deleteChat: jest.fn(),
      isApiCallOngoing: false,
      loading: false,
    });
  });

  it("renders loading spinner when loading", () => {
    (useAllChats as jest.Mock).mockReturnValueOnce({
      chatSessions: [],
      deleteChat: jest.fn(),
      isApiCallOngoing: false,
      loading: true,
    });

    const { asFragment } = render(
      <MemoryRouter>
        <AllChatsPage />
      </MemoryRouter>
    );

    expect(asFragment()).toMatchSnapshot();
  });

  it("renders chat sessions", () => {
    (useAllChats as jest.Mock).mockReturnValueOnce({
      chatSessions: [
        {
          id: 1,
          name: "Chat 1",
          user_email: "test@example.com",
          created: "2025-01-01T00:00:00Z",
          updated: "2025-01-01T00:00:00Z",
        },
        {
          id: 2,
          name: "Chat 2",
          user_email: "test@example.com",
          created: "2025-01-02T00:00:00Z",
          updated: "2025-01-02T00:00:00Z",
        },
      ],
      deleteChat: jest.fn(),
      isApiCallOngoing: false,
      loading: false,
    });

    const { asFragment } = render(
      <MemoryRouter>
        <AllChatsPage />
      </MemoryRouter>
    );

    expect(asFragment()).toMatchSnapshot();
  });

  it("calls deleteChat when delete button is clicked", () => {
    const deleteChatMock = jest.fn();
    (useAllChats as jest.Mock).mockReturnValueOnce({
      chatSessions: [
        {
          id: 1,
          name: "Chat 1",
          user_email: "test@example.com",
          created: "2025-01-01T00:00:00Z",
          updated: "2025-01-01T00:00:00Z",
        },
      ],
      deleteChat: deleteChatMock,
      isApiCallOngoing: false,
      loading: false,
    });

    render(
      <MemoryRouter>
        <AllChatsPage />
      </MemoryRouter>
    );

    const deleteButton = screen.getByTestId("delete-chat-1");
    fireEvent.click(deleteButton);

    expect(deleteChatMock).toHaveBeenCalledWith(1);
  });

  it("disables delete button when API call is ongoing", () => {
    (useAllChats as jest.Mock).mockReturnValueOnce({
      chatSessions: [
        {
          id: 1,
          name: "Chat 1",
          user_email: "test@example.com",
          created: "2025-01-01T00:00:00Z",
          updated: "2025-01-01T00:00:00Z",
        },
      ],
      deleteChat: jest.fn(),
      isApiCallOngoing: true,
      loading: false,
    });

    render(
      <MemoryRouter>
        <AllChatsPage />
      </MemoryRouter>
    );

    const deleteButton = screen.getByTestId("delete-chat-1");
    expect(deleteButton).toBeDisabled();
  });
});
