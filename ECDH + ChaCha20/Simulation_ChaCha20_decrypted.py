import pandas as pd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

# === SETUP ===
file_excel = "hasil_HKDF_only.xlsx"
file_cipher_hex = "ciphertext_hex.txt"
output_plaintext = "decrypted_output.txt"
iterasi_ke = 4  # Sesuaikan iterasi yang digunakan saat enkripsi

# === AMBIL KUNCI DARI EXCEL ===
df = pd.read_excel(file_excel)
derived_key_hex = df.loc[df["Iterasi"] == iterasi_ke, "Derived Key (hex)"].values[0]
derived_key = bytes.fromhex(derived_key_hex)

# === BACA FILE TEKS YANG BERISI HEX ===
with open(file_cipher_hex, "r") as f:
    lines = f.readlines()
    nonce_hex = lines[0].strip().split("Nonce:")[1].strip()
    ciphertext_hex = lines[1].strip().split("Ciphertext:")[1].strip()

# === KONVERSI HEX KE BYTES ===
nonce = bytes.fromhex(nonce_hex)
ciphertext = bytes.fromhex(ciphertext_hex)

# === DEKRIPSI ===
algorithm = algorithms.ChaCha20(derived_key, nonce)
cipher = Cipher(algorithm, mode=None, backend=default_backend())
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext)

# === SIMPAN PLAINTEKS SEBAGAI UTF-8 ===
try:
    teks = plaintext.decode('utf-8')
    with open(output_plaintext, "w", encoding="utf-8") as f:
        f.write(teks)
    print(f"✅ Dekripsi selesai. Hasil disimpan sebagai: {output_plaintext}")
except UnicodeDecodeError:
    print("❌ Gagal decode sebagai UTF-8. Menyimpan sebagai biner...")
    with open(output_plaintext, "wb") as f:
        f.write(plaintext)
