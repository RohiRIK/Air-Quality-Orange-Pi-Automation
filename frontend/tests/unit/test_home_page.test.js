import { render, screen } from '@testing-library/react';
import Home from '../../app/page'; // Adjust path as needed

describe('Home', () => {
  it('renders loading state initially', () => {
    render(<Home />);
    expect(screen.getByText('Loading sensor data and recommendations...')).toBeInTheDocument();
  });
});
