import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders OctoFit Tracker app', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  // Check that the main heading is present
  const heading = screen.getByText(/OctoFit Tracker/i);
  expect(heading).toBeInTheDocument();
});
