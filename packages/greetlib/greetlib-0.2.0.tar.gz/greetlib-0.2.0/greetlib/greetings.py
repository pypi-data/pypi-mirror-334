# greetlib/greetings.py

def greet(name: str, language: str = 'en') -> str:
    """Return a greeting in different languages."""
    greetings = {
        'en': f"Hello, {name}!",
        'es': f"Hola, {name}!",
        'fr': f"Bonjour, {name}!",
        'de': f"Hallo, {name}!",
        'it': f"Ciao, {name}!"  # Added Italian greeting
    }
    return greetings.get(language, f"Hello, {name}!")
