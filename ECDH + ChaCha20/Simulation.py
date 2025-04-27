import time
import threading
from memory_profiler import memory_usage
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def compute_shared_secret(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    return shared_key

start_time1 = time.perf_counter()
private_key1 = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key1 = private_key1.public_key()
end_time1 = time.perf_counter()
elapsed_time_A = (end_time1 - start_time1)*1000


start_time2 = time.perf_counter()
private_key2 = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key2 = private_key2.public_key()
end_time2 = time.perf_counter()
elapsed_time_B = (end_time2 - start_time2)*1000


private_value1 = private_key1.private_numbers().private_value
public_numbers1 = public_key1.public_numbers()

private_value2 = private_key2.private_numbers().private_value
public_numbers2 = public_key2.public_numbers()

print("==== A KEYS ====")
print("A Private Key (int):", private_value1)
print("A Public Key X (int):", public_numbers1.x)
print("A Public Key Y (int):", public_numbers1.y)


print("\n==== B KEYS ====")
print("B Private Key (int):", private_value2)
print("B Public Key X (int):", public_numbers2.x)
print("B Public Key Y (int):", public_numbers2.y)



start_time = time.perf_counter()
start_mem = memory_usage()[0] 

# 4. Hitung shared secret
shared_secret1 = compute_shared_secret(private_key1, public_key2)


shared_secret2 = compute_shared_secret(private_key2, public_key1)


end_mem = memory_usage()[0]                    # Selesai catat penggunaan memori (MB)
end_time = time.perf_counter()                 # Selesai catat waktu

elapsed_time_ms = (end_time - start_time) * 1000
used_memory_mb = end_mem - start_mem

print("\n==== SHARED SECRETS ====")
print("Shared Secret (A)  :", shared_secret1.hex())
print("Shared Secret (B)  :", shared_secret2.hex())

print(f"\nWaktu pembangkitan kunci A  : {elapsed_time_A:.3f} ms")
print(f"Waktu pembangkitan kunci B    : {elapsed_time_B:.3f} ms")

print(f"\nWaktu Eksekusi     : {elapsed_time_ms:.3f} ms")
print(f"Penggunaan Memori    : {used_memory_mb:.3f} MB")
