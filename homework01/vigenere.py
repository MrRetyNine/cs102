def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword
    while len(key) < len(plaintext):
        key += keyword
    for i in range(len(plaintext)):
        if "A" <= plaintext[i] <= "Z":
            x = (ord(plaintext[i]) + ord(key[i])) % 26
            x += ord("A")
        elif "a" <= plaintext[i] <= "z":
            x = (ord(plaintext[i]) + ord(key[i]) - 2 * ord("a")) % 26
            x += ord("a")
        else:
            x = ord(plaintext[i])
        ciphertext = str(ciphertext) + str(chr(x))
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key = keyword
    while len(key) < len(ciphertext):
        key += keyword
    for i in range(len(ciphertext)):
        x = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        if "A" <= ciphertext[i] <= "Z":
            x += ord("A")
        elif "a" <= ciphertext[i] <= "z":
            x += ord("a")
        else:
            x = ord(ciphertext[i])
        plaintext = str(plaintext) + str(chr(x))
    return plaintext
