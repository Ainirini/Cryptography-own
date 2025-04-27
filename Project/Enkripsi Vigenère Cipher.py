# Fungsi untuk enkripsi Vigenère Cipher
def encrypt_vigenere(plaintext, key):
    encrypted_text = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    plaintext_int = [ord(i) for i in plaintext]
    
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
        encrypted_text.append(chr(value + 65))  # Mengembalikan ke huruf besar
    
    return ''.join(encrypted_text)

# Fungsi untuk membaca file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
        return None

# Fungsi utama
def main():
    # Baca file input
    file_path = input("Masukkan nama file teks (dengan ekstensi): ")
    plaintext = read_file(file_path)
    
    if plaintext is None:
        return
    
    # Meminta input kunci
    key = input("Masukkan kunci untuk enkripsi: ").upper()

    # Enkripsi menggunakan Vigenère Cipher
    encrypted_text = encrypt_vigenere(plaintext.upper(), key)
    
    # Tampilkan hasil enkripsi
    print(f"Teks hasil enkripsi: {encrypted_text}")

# Panggil fungsi utama
if __name__ == "__main__":
    main()
