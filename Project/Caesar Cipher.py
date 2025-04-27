def caesar_cipher(text, shift):
    result = ""
    
    # Traverse through each character in the text
    for char in text:
        # Check if it's an uppercase letter
        if char.isupper():
            # Shift the character by the given amount and wrap around using modulo
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Check if it's a lowercase letter
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            # Non-alphabetic characters remain unchanged
            result += char
            
    return result

# Example usage
plaintext = "RESKY ANDI"
shift = 7
ciphertext = caesar_cipher(plaintext, shift)
print(f"Plaintext: {plaintext}")
print(f"Ciphertext: {ciphertext}")
