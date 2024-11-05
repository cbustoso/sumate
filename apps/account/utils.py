import re
import unicodedata
from itertools import cycle
from functools import lru_cache

@lru_cache(maxsize=None)
def validate_rut(rut: str) -> bool:
    """
    Validates a Chilean RUT.

    Parameters:
    - rut (str): The RUT to validate.

    Returns:
    bool: True if the RUT is valid, False otherwise.
    """
    rut = rut.replace('.', '').replace('-', '')

    if rut == "nan":
        return False
    
    try:
        body, verifier = rut[:-1], rut[-1].upper()
    except Exception as e:
        return False
    
    try:
        body = int(body)
    except Exception as e:
        return False
    
    # Reverse the body and calculate the modulus
    reversed_digits = map(int, reversed(str(body)))
    factors = cycle(range(2, 8))
    modulus = sum(d * f for d, f in zip(reversed_digits, factors)) % 11
    
    # Determine the expected verification digit
    if modulus == 1:
        expected_verifier = 'K'
    elif modulus == 0:
        expected_verifier = '0'
    else:
        expected_verifier = str(11 - modulus)
    
    # Validate the RUT
    return verifier == expected_verifier

                  
@lru_cache(maxsize=None)
def normalize_name(name: str) -> str:
    """
    Normalizes a name by removing accents, making it lowercase, and removing special characters.

    Parameters:
    - name (str): The name to normalize.

    Returns:
    str: The normalized name.
    """
    # Remove accents and other diacritics
    name = ''.join(
        c for c in unicodedata.normalize('NFD', str(name))
        if unicodedata.category(c) != 'Mn'
    )
    # Remove special characters like punctuation
    name = re.sub(r'[^\w\s]', '', name)
    return name.lower()
