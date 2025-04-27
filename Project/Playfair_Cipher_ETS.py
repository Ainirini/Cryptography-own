# -*- coding: utf-8 -*-


list_huruf = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#MEMBUAT DIGRAPH (MEMISAH MENJADI BEBERAPA PASANGAN HURUF)
def Digraph(text):
	Digraph = []
	grup = 0
	for i in range(2, len(text), 2):
		Digraph.append(text[grup:i])

		grup = i
	Digraph.append(text[grup:])
	return Digraph

def Bagi_huruf(text):
	text= text.replace("j", "i")
	k = len(text)

	if k % 2 == 0:
		for i in range(0, k, 2):
			if text[i] == text[i+1] and text[i+1] == str('z'):
				huruf_baru = text[0:i+1] + str('x') + text[i+1:]
				continue

			if text[i] == text[i+1] and text[i+1] != str('z'):
				huruf_baru = text[0:i+1] + str('z') + text[i+1:]
				huruf_baru = Bagi_huruf(huruf_baru)
				break
			else:
				huruf_baru = text

	else:
		for i in range(0, k-1, 2):
			if text[i] == text[i+1] and text[i+1] == str('z'):
				huruf_baru = text[0:i+1] + str('x') + text[i+1:]
				continue
			if text[i] == text[i+1]:
				huruf_baru = text[0:i+1] + str('z') + text[i+1:]
				huruf_baru = Bagi_huruf(huruf_baru)
				break
			else:
				huruf_baru = text + str('z')

	return huruf_baru

print(Bagi_huruf('Playfair Cipher'))


#MEMBUAT MATRIKS KUNCI
def kuncipersegi(word, list_huruf):
	katakunci = []
	for i in word:
		if i not in katakunci:
			if i == 'j':
				katakunci.append('i')
			else:
				katakunci.append(i)

	elemenkunci = []
	for i in katakunci:
		if i not in elemenkunci:
			elemenkunci.append(i)
	for i in list_huruf:
		if i not in elemenkunci:
			elemenkunci.append(i)

	matriks = []
	while elemenkunci != []:
		matriks.append(elemenkunci[:5])
		elemenkunci = elemenkunci[5:]

	return matriks

def search(mat, element):
  for i in range(5):
    for j in range(5):
      if(mat[i][j] == element):
        return i, j

#ENKRIPSI PLAINTEXT
def Enkripsi_baris(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	if e1c == 4:
		char1 = matr[e1r][0]
	else:
		char1 = matr[e1r][e1c+1]

	char2 = ''
	if e2c == 4:
		char2 = matr[e2r][0]
	else:
		char2 = matr[e2r][e2c+1]

	return char1, char2

def Enkripsi_kolom(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	if e1r == 4:
		char1 = matr[0][e1c]
	else:
		char1 = matr[e1r+1][e1c]

	char2 = ''
	if e2r == 4:
		char2 = matr[0][e2c]
	else:
		char2 = matr[e2r+1][e2c]

	return char1, char2

def Enkripsi_bentukpersegi(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	char1 = matr[e1r][e2c]

	char2 = ''
	char2 = matr[e2r][e1c]

	return char1, char2

def EnkripsiPlayfairCipher(matriks, plainList):
	Cipher_text = []
	for i in range(0, len(plainList)):
		c1 = 0
		c2 = 0
		ele1_x, ele1_y = search(matriks, plainList[i][0])
		ele2_x, ele2_y = search(matriks, plainList[i][1])

		if ele1_x == ele2_x:
			c1, c2 = Enkripsi_baris(matriks, ele1_x, ele1_y, ele2_x, ele2_y)
		elif ele1_y == ele2_y:
			c1, c2 = Enkripsi_kolom(matriks, ele1_x, ele1_y, ele2_x, ele2_y)
		else:
			c1, c2 = Enkripsi_bentukpersegi(
				matriks, ele1_x, ele1_y, ele2_x, ele2_y)

		cipher = c1 + c2
		Cipher_text.append(cipher)
	return Cipher_text

#DEKRIPSI CIPHER
def Dekripsi_baris(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	if e1c == 0:
		char1 = matr[e1r][4]
	else:
		char1 = matr[e1r][e1c-1]

	char2 = ''
	if e2c == 0:
		char2 = matr[e2r][4]
	else:
		char2 = matr[e2r][e2c-1]

	return char1, char2

def Dekripsi_kolom(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	if e1r == 0:
		char1 = matr[4][e1c]
	else:
		char1 = matr[e1r-1][e1c]

	char2 = ''
	if e2r == 0:
		char2 = matr[4][e2c]
	else:
		char2 = matr[e2r-1][e2c]

	return char1, char2

def Dekripsi_bentukpersegi(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	char1 = matr[e1r][e2c]

	char2 = ''
	char2 = matr[e2r][e1c]

	return char1, char2

def DekripsiPlayfairCipher(matriks, plainList):
	Cipher_text = []
	for i in range(0, len(plainList)):
		c1 = 0
		c2 = 0
		ele1_x, ele1_y = search(matriks, plainList[i][0])
		ele2_x, ele2_y = search(matriks, plainList[i][1])

		if ele1_x == ele2_x:
			c1, c2 = Dekripsi_baris(matriks, ele1_x, ele1_y, ele2_x, ele2_y)
		elif ele1_y == ele2_y:
			c1, c2 = Dekripsi_kolom(matriks, ele1_x, ele1_y, ele2_x, ele2_y)
		else:
			c1, c2 = Dekripsi_bentukpersegi(
				matriks, ele1_x, ele1_y, ele2_x, ele2_y)

		cipher = c1 + c2
		Cipher_text.append(cipher)
	return Cipher_text

Plain_text = input("Input PlainText = ")
Plain_text = Plain_text.replace(" ", "")
Plain_text = Plain_text.lower()
Plaintext_List = Digraph(Bagi_huruf(Plain_text))

Key_text = input("Input KeyText = ")
Key_text = Key_text.replace(" ", "")
Key_text = Key_text.lower()
matriks = kuncipersegi(Key_text, list_huruf)

CipherList = EnkripsiPlayfairCipher(matriks, Plaintext_List)
Cipher_text = ""
for i in CipherList:
	Cipher_text += i

Dekripsi_Cipher_text = Digraph(Cipher_text)

Dekripsi_Plaintext_list = DekripsiPlayfairCipher(matriks, Dekripsi_Cipher_text)

Plaintext_text = ""
for i in Plaintext_List:
  Plaintext_text += i

Dekripsi_Plaintext_text = ""
for i in Dekripsi_Plaintext_list:
  Dekripsi_Plaintext_text += i

print("Plaintext: " + Plaintext_text)
print("Ciphertext: " + Cipher_text)
print("Plaintext setelah Dekripsi: " + Dekripsi_Plaintext_text)
