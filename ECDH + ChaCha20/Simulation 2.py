import threading
import time
from memory_profiler import memory_usage
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os

barrier = threading.Barrier(2)  # Sinkronisasi dua thread

def generate_key_pair():
    barrier.wait()  # Pastikan kedua proses mulai bersamaan
    start_time = time.perf_counter()
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000  # Konversi ke ms
    return private_key, public_key, elapsed_time

# Variabel untuk menyimpan hasil
private_key1, public_key1, elapsed_time_A = None, None, None
private_key2, public_key2, elapsed_time_B = None, None, None

def key_gen_A():
    global private_key1, public_key1, elapsed_time_A
    private_key1, public_key1, elapsed_time_A = generate_key_pair()

def key_gen_B():
    global private_key2, public_key2, elapsed_time_B
    private_key2, public_key2, elapsed_time_B = generate_key_pair()

# Jalankan kedua proses secara paralel
thread1 = threading.Thread(target=key_gen_A)
thread2 = threading.Thread(target=key_gen_B)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

# Ekstraksi nilai kunci privat dan publik
private_value1 = private_key1.private_numbers().private_value
public_numbers1 = public_key1.public_numbers()

private_value2 = private_key2.private_numbers().private_value
public_numbers2 = public_key2.public_numbers()

# Menampilkan kunci
print("\n==== A KEYS ====")
print("A Private Key (int) :", private_value1)
print("A Public Key X (int):", public_numbers1.x)
print("A Public Key Y (int):", public_numbers1.y)

print("\n==== B KEYS ====")
print("B Private Key (int) :", private_value2)
print("B Public Key X (int):", public_numbers2.x)
print("B Public Key Y (int):", public_numbers2.y)

# Perhitungan shared secret dengan pengukuran waktu dan memori
def compute_shared_secret(private_key, peer_public_key):
    return private_key.exchange(ec.ECDH(), peer_public_key)

start_mem = memory_usage()[0]  # Awal penggunaan memori
start_time = time.perf_counter()  # Awal waktu eksekusi

shared_secret1 = compute_shared_secret(private_key1, public_key2)
shared_secret2 = compute_shared_secret(private_key2, public_key1)

end_time = time.perf_counter()  # Akhir waktu eksekusi
end_mem = memory_usage()[0]  # Akhir penggunaan memori

elapsed_time_ms = (end_time - start_time) * 1000
used_memory_mb = end_mem - start_mem

# Menampilkan shared secret dan metrik
print("\n==== SHARED SECRETS ====")
print("Shared Secret (A)  :", shared_secret1.hex())
print("Shared Secret (B)  :", shared_secret2.hex())

print(f"\nWaktu pembangkitan kunci A    : {elapsed_time_A:.3f} ms")
print(f"Waktu pembangkitan kunci B    : {elapsed_time_B:.3f} ms")

print(f"\nWaktu Eksekusi Shared Secret   : {elapsed_time_ms:.3f} ms")
print(f"Penggunaan Memori              : {used_memory_mb:.3f} MB")


def derive_key(shared_secret):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(16), 
        info=b"key derivation", 
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)

derived_key = derive_key(shared_secret1)

print("\n==== DERIVED KEYS (HKDF-SHA256) ====")
print("Derived Key  :", derived_key.hex())

import base64

# Simpan dalam bentuk hexadecimal
with open("derived_key_hex.txt", "w") as file:
    file.write(derived_key.hex())

# Simpan dalam bentuk Base64
with open("derived_key_base64.txt", "w") as file:
    file.write(base64.b64encode(derived_key).decode())

# Baca kembali dari file (hex)
with open("derived_key_hex.txt", "r") as file:
    loaded_key_hex = bytes.fromhex(file.read())

# Baca kembali dari file (Base64)
with open("derived_key_base64.txt", "r") as file:
    loaded_key_base64 = base64.b64decode(file.read())

#print("Loaded Key (Hex):", loaded_key_hex.hex())
#print("Loaded Key (Base64):", loaded_key_base64.hex())
