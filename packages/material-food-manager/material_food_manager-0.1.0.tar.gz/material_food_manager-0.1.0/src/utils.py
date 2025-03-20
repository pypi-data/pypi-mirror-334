def calculate_total_price(items):
    total = sum(item['price'] * item['quantity'] for item in items)
    return total

def validate_input(value, value_type=float):
    try:
        value_type(value)
        return True
    except ValueError:
        return False

def format_price(price):
    return f"${price:.2f}"