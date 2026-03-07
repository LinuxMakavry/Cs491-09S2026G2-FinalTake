import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import LoginPage from "../pages/Login/LoginPage";

const mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

describe("LoginPage", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    localStorage.clear();
  });

  it("shows validation error if email or password missing", () => {
    render(<LoginPage />);
    fireEvent.click(screen.getByRole("button", { name: "Login" }));

    expect(
      screen.getByText("Please enter both email and password")
    ).toBeInTheDocument();
  });

  it("stores user and navigates on valid login", () => {
    render(<LoginPage />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "test@test.com" }
    });

    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "password123" }
    });

    fireEvent.click(screen.getByRole("button", { name: "Login" }));

    const stored = JSON.parse(localStorage.getItem("user"));
    expect(stored.email).toBe("test@test.com");
    expect(stored.isLoggedIn).toBe(true);
    expect(mockNavigate).toHaveBeenCalledWith("/search");
  });
});

/*
SOURCES:
- Vitest documentation (mocking + test structure)
- React Testing Library documentation (render, screen, fireEvent)
- react-router-dom testing pattern (mocking useNavigate)
*/