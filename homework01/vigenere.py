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
        if ord("A") <= ord(plaintext[i]) <= ord("Z"):
            x_lol = (ord(plaintext[i]) + ord(key[i])) % 26
            x_lol += ord("A")
        elif ord("a") <= ord(plaintext[i]) <= ord("z"):
            x_lol = (ord(plaintext[i]) + ord(key[i]) - 2 * ord("a")) % 26
            x_lol += ord("a")
        else:
            x_lol = ord(plaintext[i])
        ciphertext = str(ciphertext) + str(chr(x_lol))
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
        x_lol = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        if ord("A") <= ord(ciphertext[i]) <= ord("Z"):
            x_lol += ord("A")
        elif ord("a") <= ord(ciphertext[i]) <= ord("z"):
            x_lol += ord("a")
        else:
            x_lol = ord(ciphertext[i])
        plaintext = str(plaintext) + str(chr(x_lol))
    return plaintext
