def create_matrix(key):
    """Membangun matriks 5x5 berdasarkan kata kunci."""
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()

    for char in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    """Mencari posisi (baris, kolom) dari suatu huruf di matriks."""
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    # Jika karakter tidak ditemukan
    raise ValueError(f"Karakter '{char}' tidak ditemukan di matriks.")

def prepare_text(text):
    """Menyiapkan teks: membersihkan dan membuat pasangan huruf."""
    text = text.upper().replace('J', 'I').replace(' ', '')
    pairs = []
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'

        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2

    return pairs

# Fungsi lainnya tetap sama...

def encrypt_pair(matrix, a, b):
    """Mengenkripsi sepasang huruf."""
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)

    if row_a == row_b:  # Baris yang sama
        return (matrix[row_a][(col_a + 1) % 5], matrix[row_b][(col_b + 1) % 5])
    elif col_a == col_b:  # Kolom yang sama
        return (matrix[(row_a + 1) % 5][col_a], matrix[(row_b + 1) % 5][col_b])
    else:  # Persegi berbeda
        return (matrix[row_a][col_b], matrix[row_b][col_a])

def encrypt(text, key):
    """Fungsi utama untuk enkripsi."""
    matrix = create_matrix(key)
    pairs = prepare_text(text)
    encrypted_text = ''.join(
        ''.join(encrypt_pair(matrix, a, b)) for a, b in pairs
    )
    return encrypted_text

def read_file(file_path):
    """Membaca teks dari file."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Menulis teks ke file."""
    with open(file_path, 'w') as file:
        file.write(content)


input_file = 'Plaintext.txt'  # Nama file input
output_file = 'Ciphertext.txt'  # Nama file output
key = 'MATEMATIKA'

# Baca pesan dari file, enkripsi, dan simpan hasilnya
plaintext = read_file(input_file)
ciphertext = encrypt(plaintext, key)
write_file(output_file, ciphertext)

print(f"Pesan terenkripsi disimpan di {output_file}.")
