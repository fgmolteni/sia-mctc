import locale
from num2words import num2words

def number_to_text(number):
    """Converts a number to its text representation in Spanish."""
    try:
        return num2words(number, lang='es').capitalize()
    except Exception as e:
        return str(e)

def number_to_currency(number):
    """Formats a number as Argentine Peso currency."""
    try:
        # First, try the standards-compliant locale-based approach.
        locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
        return locale.currency(number, grouping=True)
    except locale.Error:
        # If the locale is not supported, fall back to manual formatting.
        # This is a safe alternative for environments without the locale installed.
        formatted_str = f'{number:,.2f}'
        # Swap the separators to match Argentine format ($ 1.234,56)
        arg_formatted_str = formatted_str.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f'$ {arg_formatted_str}'
    except Exception as e:
        # Catch any other unexpected errors.
        return str(e)
