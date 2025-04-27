from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# === 1. Generate Kunci ===
alice_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
alice_public_key = alice_private_key.public_key()

# === 2. Simpan Kunci Privat ===
with open("alice_private_key.pem", "wb") as private_file:
    private_file.write(
        alice_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()  # Kunci tidak dienkripsi
        )
    )

# === 3. Simpan Kunci Publik ===
with open("alice_public_key.pem", "wb") as public_file:
    public_file.write(
        alice_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Kunci telah disimpan sebagai file!")

# === 4. Muat Kunci Privat dari File ===
with open("alice_private_key.pem", "rb") as private_file:
    loaded_private_key = serialization.load_pem_private_key(
        private_file.read(),
        password=None,  # Karena sebelumnya tidak dienkripsi
        backend=default_backend()
    )

# === 5. Muat Kunci Publik dari File ===
with open("alice_public_key.pem", "rb") as public_file:
    loaded_public_key = serialization.load_pem_public_key(
        public_file.read(),
        backend=default_backend()
    )

print("Kunci telah dimuat kembali dari file!")

# === 6. Periksa apakah kunci yang dimuat sama dengan kunci asli ===
print("Apakah kunci privat sama?:", loaded_private_key.private_numbers() == alice_private_key.private_numbers())
print("Apakah kunci publik sama?:", loaded_public_key.public_numbers() == alice_public_key.public_numbers())
