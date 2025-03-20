"""Sample project main file for testing."""

def main():
    """Main function."""
    print("Hello from the main function!")
    result = process_data([1, 2, 3, 4, 5])
    print(f"Processed data: {result}")
    
    return result

def process_data(data):
    """Process the given data."""
    from .utils import double_values
    
    # Double all values and calculate sum
    doubled = double_values(data)
    return sum(doubled)

if __name__ == "__main__":
    main()