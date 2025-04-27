import pandas as pd
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

# Fungsi enkripsi ChaCha20
def chacha20_encrypt(key, plaintext):
    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return nonce, ciphertext

# === INPUT ===
# 1. Ambil kunci dari file hasil HKDF
file_excel = "hasil_HKDF_only.xlsx"
df = pd.read_excel(file_excel)

# Pilih derived key dari iterasi tertentu, misalnya iterasi ke-2
iterasi_ke = 4
derived_key_hex = df.loc[df["Iterasi"] == iterasi_ke, "Derived Key (hex)"].values[0]
derived_key = bytes.fromhex(derived_key_hex)

# 2. Baca file dokumen plaintext
# Contoh: file .txt (jika .docx nanti bisa ditambahkan parser)
with open("pesan.txt", "rb") as f:
    plaintext = f.read()

# === ENKRIPSI ===
nonce, ciphertext = chacha20_encrypt(derived_key, plaintext)

# === SIMPAN OUTPUT ===
# Simpan nonce dan ciphertext dalam file biner
with open("ciphertext.bin", "wb") as f:
    f.write(nonce + ciphertext)

# Atau simpan dalam bentuk hex (jika ingin dibaca manusia)
with open("ciphertext_hex.txt", "w") as f:
    f.write("Nonce: " + nonce.hex() + "\n")
    f.write("Ciphertext: " + ciphertext.hex())

print("Enkripsi selesai. File disimpan sebagai 'ciphertext.bin' dan 'ciphertext_hex.txt'")
