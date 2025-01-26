import { renderHook, act } from "@testing-library/react";
import { useNavigate } from "react-router";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { auth } from "../../../firebase";
import { AuthContext } from "../../../context/AuthContext";
import useHomePage from "../useHomePage";

jest.mock("react-router", () => ({
  useNavigate: jest.fn(),
}));

jest.mock("firebase/auth", () => ({
  GoogleAuthProvider: jest.fn(),
  signInWithPopup: jest.fn(),
}));

jest.mock("../../../firebase", () => ({
  auth: {},
}));

describe("useHomePage", () => {
  const mockNavigate = jest.fn();
  const mockUseNavigate = useNavigate as jest.Mock;
  const mockSignInWithPopup = signInWithPopup as jest.Mock;
  const mockGoogleAuthProvider = GoogleAuthProvider as unknown as jest.Mock;

  const mockAuthContext = {
    user: null,
    loading: false,
  };

  const wrapper =
    (authContextVal: any) =>
    ({ children }: { children: React.ReactNode }) =>
      (
        <AuthContext.Provider value={authContextVal}>
          {children}
        </AuthContext.Provider>
      );

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseNavigate.mockReturnValue(mockNavigate);
  });

  it("should navigate to /chat if user is authenticated", () => {
    mockAuthContext.user = { uid: "123" } as any;
    renderHook(() => useHomePage(), { wrapper: wrapper(mockAuthContext) });
    expect(mockNavigate).toHaveBeenCalledWith("/chat");
  });

  it("should not navigate if user is not authenticated", () => {
    mockAuthContext.user = null;
    renderHook(() => useHomePage(), { wrapper: wrapper(mockAuthContext) });
    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it("should handle Google login", async () => {
    mockAuthContext.user = null;
    const { result } = renderHook(() => useHomePage(), {
      wrapper: wrapper(mockAuthContext),
    });
    await act(async () => {
      await result.current.handleGoogleLogin();
    });
    expect(mockGoogleAuthProvider).toHaveBeenCalled();
    expect(mockSignInWithPopup).toHaveBeenCalledWith(auth, expect.any(Object));
  });

  it("should handle login error", async () => {
    const consoleErrorSpy = jest.spyOn(console, "error").mockImplementation();
    mockSignInWithPopup.mockRejectedValueOnce(new Error("Login failed"));
    mockAuthContext.user = null;
    const { result } = renderHook(() => useHomePage(), {
      wrapper: wrapper(mockAuthContext),
    });
    await act(async () => {
      await result.current.handleGoogleLogin();
    });
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      "Error during login:",
      "Login failed"
    );
    consoleErrorSpy.mockRestore();
  });
});
