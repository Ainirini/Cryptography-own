def generate_key_matrix(key):
    # Hilangkan huruf duplikat dan ubah menjadi uppercase
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))
    matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Tanpa 'J'

    # Gabungkan key dan sisa alfabet
    combined = key + "".join([c for c in alphabet if c not in key])

    # Buat matriks 5x5 dari gabungan key + alphabet
    for i in range(0, 25, 5):
        matrix.append(list(combined[i:i + 5]))

    return matrix

def find_position(matrix, char):
    # Temukan posisi huruf di matriks
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def decrypt_pair(matrix, pair):
    r1, c1 = find_position(matrix, pair[0])
    r2, c2 = find_position(matrix, pair[1])

    if r1 == r2:  # Berada di baris yang sama
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:  # Berada di kolom yang sama
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:  # Membentuk persegi
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_playfair_cipher(ciphertext, key):
    matrix = generate_key_matrix(key)
    plaintext = ""

    # Pecah ciphertext menjadi pasangan huruf
    pairs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]

    for pair in pairs:
        plaintext += decrypt_pair(matrix, pair)

    # Kembalikan hasil dekripsi
    return plaintext

# Contoh penggunaan
ciphertext = "REKMULIRIEIRKXIPYG"  # Hasil enkripsi
key = "DEPARTEMENMATEMATIKA"

plaintext = decrypt_playfair_cipher(ciphertext, key)
print(f"Plaintext: {plaintext}")
