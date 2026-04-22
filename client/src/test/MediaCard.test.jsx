import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import MediaCard from "../components/media/MediaCard";

// Mock react-router-dom's useNavigate so clicks don't actually change routes
const mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

describe("MediaCard", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it("renders title, type, and rating value", () => {
    render(
      <MediaCard
        id={123}
        title="Inception"
        type="movie"
        rating={4.7}
        imageUrl={null}
      />
    );

    expect(screen.getByText("Inception")).toBeInTheDocument();
    expect(screen.getByText("movie")).toBeInTheDocument();
    // rating is rendered via rating.toFixed(1)
    expect(screen.getByText("4.7")).toBeInTheDocument();
  });

  it("shows placeholder when imageUrl is missing", () => {
    render(
      <MediaCard id={1} title="No Poster" type="movie" rating={3.5} imageUrl={null} />
    );

    expect(screen.getByText("No Image")).toBeInTheDocument();
  });

  it("navigates to /media/:type/:id when clicked", () => {
    const { container } = render(
      <MediaCard
        id={42}
        title="The Matrix"
        type="movie"
        rating={4.5}
        imageUrl={null}
      />
    );

    // Click the card root element
    const card = container.querySelector(".media-card");
    expect(card).toBeTruthy();

    fireEvent.click(card);
    expect(mockNavigate).toHaveBeenCalledWith("/media/movie/42");
  });
});

/*
SOURCES / TEMPLATES USED:
- Vitest docs: `describe/it/expect`, `vi.mock`, `vi.fn`, `vi.importActual`
- React Testing Library docs: `render`, `screen`, `fireEvent`
- react-router-dom testing pattern: mock `useNavigate` for navigation assertions
*/