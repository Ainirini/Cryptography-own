from sympy import randprime
from math import gcd

# Fungsi untuk menghasilkan bilangan prima besar
def generate_large_prime(bits=512):
    # Menghasilkan bilangan prima acak dalam rentang bit tertentu
    lower_bound = 2**(bits - 1)
    upper_bound = 2**bits - 1
    return randprime(lower_bound, upper_bound)

# Fungsi untuk menghitung invers modular
def modular_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    
    while e > 0:
        # Loop menghitung hasil pembagian dan sisa secara iteratif hingga e = 0
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        # nilai x dan y diubah pada setiap iterasi untuk mendekati solusi
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y
    
    if temp_phi == 1: # temp_phi = 1 modular inverse ditemukan
        # (d + phi) jika d negatif
        return d + phi if d < 0 else d
    return None

# Fungsi untuk mengenkripsi
def encrypt(public_key, plaintext):
    e, n = public_key # public key (e,n)
    # Enkripsi tiap karakter (ASCII) menjadi ciphertext
    return [pow(ord(char), e, n) for char in plaintext]

# Fungsi untuk mendekripsi
def decrypt(private_key, ciphertext):
    d, n = private_key # private key (d,n)
    # Dekripsi tiap angka ciphertext kembali ke karakter
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)

# menemukan nilai e yang relatif prima
def find_e(phi):
    #Mulai dari nilai kecil (biasanya 2) dan cari sampai relatif prima
    e = 2
    while e < phi:
        if gcd(e, phi) == 1:
            return e  # Relatif prima ditemukan
        e += 1
    #raise ValueError("Tidak ada nilai e yang valid ditemukan.")


# Langkah 1: Generasi kunci
p = generate_large_prime(512)
q = generate_large_prime(512)
while p == q:  # Pastikan p dan q berbeda
    q = generate_large_prime(512)
n = p * q
phi = (p - 1) * (q - 1)
#e = 65537
e = find_e(phi)  # Otomatis menentukan e
#print(f"Nilai e yang ditemukan: {e}")

d = modular_inverse(e, phi)

# Kunci publik dan privat
public_key = (e, n)
private_key = (d, n)

print(f"Bilangan prima p: {p}")
print(f"Bilangan prima q: {q}")
print(f"Panjang bilangan p: {len(str(p))}")
print(f"Panjang bilangan q: {len(str(q))}")
# Input dari terminal
print()
plaintext = input("Plaintext: ")

print()

# Langkah 2: Enkripsi
ciphertext = encrypt(public_key, plaintext)
print(f"Ciphertext: {ciphertext}")

print()

# Langkah 3: Dekripsi
decrypted_text = decrypt(private_key, ciphertext)
print(f"Plaintext (dekripsi): {decrypted_text}")
