import threading
import time
import pandas as pd
import tracemalloc
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from tabulate import tabulate

def generate_key_pair():
    start_time = time.perf_counter()
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key = private_key.public_key()
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000  # ms
    return private_key, public_key, elapsed_time

def compute_shared_secret(private_key, peer_public_key):
    return private_key.exchange(ec.ECDH(), peer_public_key)

def derive_key(shared_secret, length=32):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)

def generate_keys_thread(result, index):
    result[index] = generate_key_pair()

num_iterations = 30
results = []

for i in range(num_iterations):
    result = [None, None]
    thread1 = threading.Thread(target=generate_keys_thread, args=(result, 0))
    thread2 = threading.Thread(target=generate_keys_thread, args=(result, 1))
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    private_key1, public_key1, elapsed_time_A = result[0]
    private_key2, public_key2, elapsed_time_B = result[1]

    tracemalloc.start()
    start_time = time.perf_counter()

    shared_secret1 = compute_shared_secret(private_key1, public_key2)
    shared_secret2 = compute_shared_secret(private_key2, public_key1)

    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_shared_ms = (end_time - start_time) * 1000
    used_memory_mb = peak_mem / (1024 * 1024)

    # HKDF derivation
    derived_key = derive_key(shared_secret1)

    results.append([
        i + 1,
        elapsed_time_A,
        elapsed_time_B,
        elapsed_shared_ms,
        used_memory_mb,
        derived_key.hex()
    ])

# Output
columns = [
    "Iterasi", "Waktu Key A (ms)", "Waktu Key B (ms)",
    "Waktu Shared Secret (ms)", "Memori (MB)", "Derived Key (hex)"
]

df_results = pd.DataFrame(results, columns=columns)

# Tampilkan di terminal
print(tabulate(df_results, headers='keys', tablefmt='grid'))

# Simpan ke file
df_results.to_csv("hasil_HKDF_only.csv", index=False)
df_results.to_excel("hasil_HKDF_only.xlsx", index=False)

print("\nHasil telah disimpan ke 'hasil_HKDF_only.csv' dan 'hasil_HKDF_only.xlsx'")
