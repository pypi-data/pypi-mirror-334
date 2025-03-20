def convert_celsius_to_fahrenheit(value: float, is_delta: bool = False) -> float:
    value = value * 1.8
    
    if not is_delta:
        value += 32.0
        
    return value

def convert_bar_to_psi(value: float) -> float:
    return value * 14.5037738