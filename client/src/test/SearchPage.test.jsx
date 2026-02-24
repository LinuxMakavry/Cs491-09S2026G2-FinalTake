import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SearchPage from "../pages/Search/SearchPage";
import { ThemeContext } from "../context/ThemeContext";

// Mock router navigation (SearchPage uses useNavigate)
const mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

// Helper to render SearchPage with ThemeContext provided
function renderWithTheme(ui, { theme = "light", toggleTheme = vi.fn() } = {}) {
  return render(
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {ui}
    </ThemeContext.Provider>
  );
}

describe("SearchPage", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    localStorage.clear();
  });

  it("renders default 'Browse Media' header and shows initial media cards", () => {
    renderWithTheme(<SearchPage />);

    expect(screen.getByText("Browse Media")).toBeInTheDocument();

    // A few known mock items should be visible initially
    expect(screen.getByText("The Matrix")).toBeInTheDocument();
    expect(screen.getByText("Dune")).toBeInTheDocument();
    expect(screen.getByText("Breaking Bad")).toBeInTheDocument();
  });

  it("filters results by search query when Search is submitted", () => {
    renderWithTheme(<SearchPage />);

    const input = screen.getByPlaceholderText(
      "Search for movies, books, games, TV shows..."
    );

    fireEvent.change(input, { target: { value: "Dune" } });

    // Submit the form by clicking Search button
    fireEvent.click(screen.getByRole("button", { name: "Search" }));

    expect(screen.getByText("Search Results (1)")).toBeInTheDocument();
    expect(screen.getByText("Dune")).toBeInTheDocument();

    // One of the other items should no longer be present
    expect(screen.queryByText("The Matrix")).not.toBeInTheDocument();
  });

  it("shows 'No media found...' when filter matches nothing, and reset restores results", () => {
    renderWithTheme(<SearchPage />);

    const input = screen.getByPlaceholderText(
      "Search for movies, books, games, TV shows..."
    );

    fireEvent.change(input, { target: { value: "this will not match" } });
    fireEvent.click(screen.getByRole("button", { name: "Search" }));

    expect(
      screen.getByText("No media found matching your search.")
    ).toBeInTheDocument();

    // Clear Filters button calls handleReset
    fireEvent.click(screen.getByRole("button", { name: "Clear Filters" }));

    expect(screen.getByText("Browse Media")).toBeInTheDocument();
    expect(screen.getByText("The Matrix")).toBeInTheDocument();
  });
});

/*
SOURCES / TEMPLATES USED:
- Vitest docs: `vi.mock`, `vi.fn`, `vi.importActual`, `beforeEach`
- React Testing Library docs: `render`, `screen`, `fireEvent`, query vs get patterns
- react-router-dom testing pattern: mock `useNavigate`
- React Context pattern: wrap component with `<ThemeContext.Provider>`
*/