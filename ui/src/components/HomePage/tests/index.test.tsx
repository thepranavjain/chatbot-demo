import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import HomePage from "../index";
import useHomePage from "../useHomePage";

jest.mock("../useHomePage");

describe("HomePage", () => {
  const mockHandleGoogleLogin = jest.fn();

  beforeEach(() => {
    (useHomePage as jest.Mock).mockReturnValue({
      handleGoogleLogin: mockHandleGoogleLogin,
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it("renders correctly", () => {
    const { asFragment } = render(<HomePage />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("calls handleGoogleLogin when the button is clicked", () => {
    render(<HomePage />);
    const loginButton = screen.getByRole("button");
    fireEvent.click(loginButton);
    expect(mockHandleGoogleLogin).toHaveBeenCalledTimes(1);
  });
});
