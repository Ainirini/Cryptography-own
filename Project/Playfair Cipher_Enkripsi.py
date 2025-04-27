def generate_matrix(key):
    key = "".join(dict.fromkeys(key.replace("J", "I")))  # Hapus duplikat, ubah J jadi I
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Tanpa J
    matrix = [char for char in key if char in alphabet]
    matrix += [char for char in alphabet if char not in matrix]
    return [matrix[i:i + 5] for i in range(0, 25, 5)]  # Buat matriks 5x5

def prepare_text(text):
    text = text.upper().replace(" ", "").replace("J", "I")
    prepared = ""
    i = 0
    while i < len(text):
        prepared += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:
            prepared += 'X'  # Tambah X jika huruf berulang
        elif i + 1 < len(text):
            prepared += text[i + 1]
        i += 2
    if len(prepared) % 2 != 0:
        prepared += 'X'  # Tambah X jika panjang teks ganjil
    return prepared

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def encrypt_pair(matrix, char1, char2):
    row1, col1 = find_position(matrix, char1)
    row2, col2 = find_position(matrix, char2)

    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    plaintext = prepare_text(plaintext)
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        ciphertext += encrypt_pair(matrix, plaintext[i], plaintext[i + 1])
    return ciphertext

if __name__ == "__main__":
    plaintext = input("Masukkan teks: ")
    key = input("Masukkan kunci: ")
    ciphertext = playfair_encrypt(plaintext, key)
    print("Ciphertext:", ciphertext)
