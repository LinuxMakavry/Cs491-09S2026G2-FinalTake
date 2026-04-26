import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders and shows the search page by default', async () => {
    render(<App />);
    expect(
      await screen.findByPlaceholderText('Search for movies, books, games, TV shows...')
    ).toBeInTheDocument();
  });
});