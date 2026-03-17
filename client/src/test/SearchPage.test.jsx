import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
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

// Mock fetch globally
const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

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
    mockFetch.mockClear();
    localStorage.clear();

    // Default: trending fetch returns known items, search returns empty
    mockFetch.mockImplementation((url) => {
      if (url.includes("/api/trending-all")) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              movies: [{ id: 1, title: "The Matrix", type: "movie", rating: 4.5, imageUrl: null }],
              shows: [{ id: 2, title: "Breaking Bad", type: "tv", rating: 5.0, imageUrl: null }],
              games: [],
              books: [{ id: 3, title: "Dune", type: "book", rating: 4.8, imageUrl: null }],
            }),
        });
      }
      // search endpoint
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ results: [] }),
      });
    });
  });

  it("renders default trending section and shows initial media cards", async () => {
    renderWithTheme(<SearchPage />);

    // While loading, skeleton cards are shown
    // After fetch resolves, trending movies should appear
    await waitFor(() =>
      expect(screen.getByText("The Matrix")).toBeInTheDocument()
    );

    // Trending tabs should be present
    expect(screen.getByRole("button", { name: "Movies" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "TV Shows" })).toBeInTheDocument();
  });

  it("filters results by search query when Search is submitted", async () => {
    // Override fetch so search returns one result
    mockFetch.mockImplementation((url) => {
      if (url.includes("/api/trending-all")) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ movies: [], shows: [], games: [], books: [] }),
        });
      }
      if (url.includes("/api/search")) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              results: [{ id: 3, title: "Dune", type: "book", rating: 4.8, imageUrl: null }],
            }),
        });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });

    renderWithTheme(<SearchPage />);

    const input = screen.getByPlaceholderText(
      "Search for movies, books, games, TV shows..."
    );

    fireEvent.change(input, { target: { value: "Dune" } });
    fireEvent.click(screen.getByRole("button", { name: "Search" }));

    await waitFor(() =>
      expect(screen.getByText("Search Results (1)")).toBeInTheDocument()
    );
    expect(screen.getByText("Dune")).toBeInTheDocument();
  });

  it("shows 'No media found...' when filter matches nothing, and reset restores results", async () => {
    // Override fetch so search returns no results
    mockFetch.mockImplementation((url) => {
      if (url.includes("/api/trending-all")) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              movies: [{ id: 1, title: "The Matrix", type: "movie", rating: 4.5, imageUrl: null }],
              shows: [],
              games: [],
              books: [],
            }),
        });
      }
      // search returns empty
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ results: [] }),
      });
    });

    renderWithTheme(<SearchPage />);

    const input = screen.getByPlaceholderText(
      "Search for movies, books, games, TV shows..."
    );

    fireEvent.change(input, { target: { value: "this will not match" } });
    fireEvent.click(screen.getByRole("button", { name: "Search" }));

    await waitFor(() =>
      expect(
        screen.getByText("No media found matching your search.")
      ).toBeInTheDocument()
    );

    // Reset button appears in the no-results state
    fireEvent.click(screen.getByRole("button", { name: "Clear Filters" }));

    // After reset, trending section is back
    await waitFor(() =>
      expect(screen.getByText("The Matrix")).toBeInTheDocument()
    );
  });
});

/*
SOURCES / TEMPLATES USED:
- Vitest docs: `vi.mock`, `vi.fn`, `vi.importActual`, `beforeEach`
- React Testing Library docs: `render`, `screen`, `fireEvent`, `waitFor`
- react-router-dom testing pattern: mock `useNavigate`
- React Context pattern: wrap component with `<ThemeContext.Provider>`
*/