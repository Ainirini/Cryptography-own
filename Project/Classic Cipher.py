# Fungsi untuk membentuk kunci yang sesuai panjang plaintext
def generate_key(plaintext, key):
    key = list(key)
    if len(plaintext) == len(key):
        return key
    else:
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

# Fungsi untuk enkripsi
def vigenere_encrypt(plaintext, key):
    cipher_text = []
    key = generate_key(plaintext, key)
    
    for i in range(len(plaintext)):
        # Menyelaraskan huruf alfabet (A=0, B=1, ..., Z=25)
        x = (ord(plaintext[i]) + ord(key[i])) % 26
        # Mengubahnya kembali ke huruf
        x += ord('A')
        cipher_text.append(chr(x))
    
    return "".join(cipher_text)

# Fungsi untuk dekripsi
def vigenere_decrypt(cipher_text, key):
    original_text = []
    key = generate_key(cipher_text, key)
    
    for i in range(len(cipher_text)):
        # Menyelaraskan huruf alfabet
        x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
        # Mengubahnya kembali ke huruf
        x += ord('A')
        original_text.append(chr(x))
    
    return "".join(original_text)

# Contoh penggunaan
plaintext = "YESAYAANANDA"  # Pastikan input huruf kapital
key = "BOCILCINABRO"

cipher_text = vigenere_encrypt(plaintext, key)
print("Ciphertext:", cipher_text)

decrypted_text = vigenere_decrypt(cipher_text, key)
print("Decrypted text:", decrypted_text)
