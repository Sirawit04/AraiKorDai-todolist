"""
Unit tests for the SimpleCalculator class.
"""

import pytest
from calculator import SimpleCalculator


class TestSimpleCalculator:
    """Test cases for SimpleCalculator operations."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert SimpleCalculator.add(10, 5) == 15
        assert SimpleCalculator.add(0, 0) == 0
        assert SimpleCalculator.add(100, 50) == 150

    def test_add_negative_numbers(self):
        """Test adding with negative numbers."""
        assert SimpleCalculator.add(-10, -5) == -15
        assert SimpleCalculator.add(-10, 5) == -5
        assert SimpleCalculator.add(10, -5) == 5

    def test_add_decimals(self):
        """Test adding decimal numbers."""
        assert SimpleCalculator.add(7.5, 2.5) == 10.0
        assert SimpleCalculator.add(3.14, 2.86) == pytest.approx(6.0)
        assert SimpleCalculator.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract_positive_numbers(self):
        """Test subtracting two positive numbers."""
        assert SimpleCalculator.subtract(10, 5) == 5
        assert SimpleCalculator.subtract(5, 10) == -5
        assert SimpleCalculator.subtract(10, 10) == 0

    def test_subtract_negative_numbers(self):
        """Test subtracting with negative numbers."""
        assert SimpleCalculator.subtract(-10, -5) == -5
        assert SimpleCalculator.subtract(-10, 5) == -15
        assert SimpleCalculator.subtract(10, -5) == 15

    def test_subtract_decimals(self):
        """Test subtracting decimal numbers."""
        assert SimpleCalculator.subtract(10.5, 3.5) == 7.0
        assert SimpleCalculator.subtract(5.5, 2.2) == pytest.approx(3.3)

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert SimpleCalculator.multiply(10, 5) == 50
        assert SimpleCalculator.multiply(0, 100) == 0
        assert SimpleCalculator.multiply(7, 8) == 56

    def test_multiply_negative_numbers(self):
        """Test multiplying with negative numbers."""
        assert SimpleCalculator.multiply(-10, -5) == 50
        assert SimpleCalculator.multiply(-10, 5) == -50
        assert SimpleCalculator.multiply(10, -5) == -50

    def test_multiply_decimals(self):
        """Test multiplying decimal numbers."""
        assert SimpleCalculator.multiply(2.5, 4) == 10.0
        assert SimpleCalculator.multiply(3.5, 2) == 7.0
        assert SimpleCalculator.multiply(1.5, 1.5) == pytest.approx(2.25)

    def test_divide_positive_numbers(self):
        """Test dividing two positive numbers."""
        assert SimpleCalculator.divide(10, 2) == 5.0
        assert SimpleCalculator.divide(10, 5) == 2.0
        assert SimpleCalculator.divide(7, 2) == 3.5

    def test_divide_negative_numbers(self):
        """Test dividing with negative numbers."""
        assert SimpleCalculator.divide(-10, -2) == 5.0
        assert SimpleCalculator.divide(-10, 2) == -5.0
        assert SimpleCalculator.divide(10, -2) == -5.0

    def test_divide_decimals(self):
        """Test dividing decimal numbers."""
        assert SimpleCalculator.divide(10.0, 4) == 2.5
        assert SimpleCalculator.divide(7.5, 2.5) == 3.0

    def test_divide_by_zero(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            SimpleCalculator.divide(10, 0)

    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        assert SimpleCalculator.divide(0, 5) == 0.0
        assert SimpleCalculator.divide(0, -5) == 0.0

    def test_large_numbers(self):
        """Test operations with large numbers."""
        assert SimpleCalculator.add(1000000, 2000000) == 3000000
        assert SimpleCalculator.multiply(1000, 1000) == 1000000
        assert SimpleCalculator.divide(1000000, 1000) == 1000.0

    def test_very_small_numbers(self):
        """Test operations with very small decimal numbers."""
        assert SimpleCalculator.add(0.001, 0.002) == pytest.approx(0.003)
        assert SimpleCalculator.multiply(0.1, 0.1) == pytest.approx(0.01)
        assert SimpleCalculator.divide(0.1, 0.01) == pytest.approx(10.0)
