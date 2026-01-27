"""
A simple calculator that can perform basic arithmetic operations:
addition, subtraction, multiplication, and division.
"""


class SimpleCalculator:
    """A simple calculator for basic arithmetic operations."""

    @staticmethod
    def add(a, b):
        """Add two numbers."""
        return a + b

    @staticmethod
    def subtract(a, b):
        """Subtract two numbers."""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Multiply two numbers."""
        return a * b

    @staticmethod
    def divide(a, b):
        """Divide two numbers.
        
        Raises:
            ValueError: If divisor is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def calculate_velocity(distance: float, time: float) -> float:
        if time <= 0:
            raise ValueError("Time must be greater than zero")
        return distance / time


def main():
    """Run the calculator in interactive mode."""
    calc = SimpleCalculator()
    
    print("=" * 50)
    print("       SIMPLE CALCULATOR")
    print("=" * 50)
    print("\nAvailable operations:")
    print("  + (add)")
    print("  - (subtract)")
    print("  * (multiply)")
    print("  / (divide)")
    print("  exit (quit)")
    print("=" * 50 + "\n")
    
    while True:
        try:
            operation = input("Enter operation (+, -, *, /, exit): ").strip()
            
            if operation.lower() == 'exit':
                print("Thank you for using the calculator!")
                break
            
            if operation not in ['+', '-', '*', '/']:
                print("Invalid operation. Please try again.\n")
                continue
            
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if operation == '+':
                result = calc.add(num1, num2)
            elif operation == '-':
                result = calc.subtract(num1, num2)
            elif operation == '*':
                result = calc.multiply(num1, num2)
            elif operation == '/':
                result = calc.divide(num1, num2)
            
            print(f"\n{num1} {operation} {num2} = {result}\n")
            
        except ValueError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()
