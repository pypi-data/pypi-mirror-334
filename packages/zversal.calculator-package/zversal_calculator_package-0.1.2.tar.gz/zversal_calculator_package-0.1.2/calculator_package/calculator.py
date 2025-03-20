import math
import fitz

# History to store calculations
history = []

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Cannot divide by zero"
def modulus(a, b): return a % b
def exponent(a, b): return a ** b
def floordiv(a, b): return a // b if b != 0 else "Cannot divide by zero"

# Scientific functions
def square_root(a): return math.sqrt(a)
def log_base10(a): return math.log10(a)
def factorial(a): return math.factorial(int(a)) if a >= 0 else "Undefined"
def sine(a): return math.sin(math.radians(a))
def cosine(a): return math.cos(math.radians(a))
def tangent(a): return math.tan(math.radians(a))

# Function to perform calculation
def calculator():
    try:
        print("\n--- Advanced Calculator ---")
        print("Operations: +, -, *, /, %, //, **, sqrt, log, fact, sin, cos, tan, history, exit")
        
        operator = input("Enter operation: ").strip().lower()
        
        if operator == "exit":
            print("Exiting Calculator. Goodbye!")
            return
        
        elif operator == "history":
            print("\nCalculation History:")
            for i, h in enumerate(history, 1):
                print(f"{i}. {h}")
            return calculator()  # Continue
        
        # Binary operations (require two numbers)
        binary_ops = {'+', '-', '*', '/', '%', '**', '//'}
        if operator in binary_ops:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            switch = {
                '+': add, '-': subtract, '*': multiply, '/': divide,
                '%': modulus, '**': exponent, '//': floordiv
            }
            result = switch.get(operator)(a, b)
        
        # Unary operations (require one number)
        elif operator in {'sqrt', 'log', 'fact', 'sin', 'cos', 'tan'}:
            a = float(input("Enter a number: "))
            switch = {
                'sqrt': square_root, 'log': log_base10, 'fact': factorial,
                'sin': sine, 'cos': cosine, 'tan': tangent
            }
            result = switch.get(operator)(a)
        
        else:
            print("Invalid operation! Try again.")
            return calculator()
        
        history.append(f"{operator} {a} = {result}")
        print("Result:", result)
        
        return calculator()  # Recursive call for continuous usage
    
    except ValueError:
        print("Invalid input! Enter numerical values.")
        return calculator()
    
    except Exception as e:
        print(f"Error: {e}")
        return calculator()
print(f"Calculator Package Imported------{fitz}")
# Run the advanced calculator
calculator()