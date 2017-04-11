# RSA Algorithm Project

"""Note: The functions in this project encrypt and decrypt by BLOCKS, not
by individual letters.
Also please note that the ASCII codes per character are three-digits long, not two.
This program requires a list of primes named 'primes.txt' which is provided.
It also requires a 'privateKey.txt' where n and d are stored, and 'publicKey.txt' where
n and e are stored. n is stored in the first line, d/e are stored in the second line.
During the first execution of this program, the user should either 
provide their own keys by creating and editing the text files, or generate the keys 
so that the text files are created if the text files are missing.
"""

import random

def findInverse(d, phi, t, t2):
	#this function uses the extended euclidean algorithm to find the inverse of d mod phi
	#t and t2 should start as 0 and 1 respectively
	r = phi
	r2 = d

	if r2 == 0:
		if r > 1:
			return "d is not invertible" #d is not invertible
		else:
			return t
	q = r // r2

	return findInverse(r-q*r2, r2, t2, t-q*t2)

def gcd(a,b):
	while (b):
		a, b = b, a % b
	return a

def findCoprime(a, phi):
	#a should be max(p,q)
	a += 1 #the number coprime with phi must be greater than a

	while(gcd(a, phi) != 1):
		a += 1
	return a

def encrypt(e, n, s):
	#function encrypts in blocks
	#e and n are the public key, s is the string of numbers to be encrypted
	#returns a string of numbers that is the encrypted message

	num = s.split()
	encrypted = ""

	for i in num:
		temp = (int(i) ** e) % n

		encrypted = encrypted + str(temp) + " "
	return encrypted

def decrypt(d, n, s):
	#function decrypts in blocks
	#d and n are the private keys
	#s is the string of numbers to be decrypted

	num = s.split()
	decrypted = ""

	for i in num:
		temp = (int(i) ** d) % n

		decrypted = decrypted + str(temp) + " "
	return decrypted

def messageToASCII(s, digit):
	#returns a string of numbers which is the ASCII values of s
	#each character has an ASCII code that is three-digits long
	#the string is separated into blocks, which each has a length less than digit
	#digit is the number of digits in n

	asc = ""
	t = ""
	i = 0

	while i < len(s):
		temp = ord(s[i])
		if temp < 100:
			temp = "0" + str(temp)
		asc += str(temp)
		i +=1

		if len(asc) > digit:
			asc = asc[:-3]
			t = t + asc + ' '
			asc = ''
			i -=1
		elif i == len(s):
			t += asc
	return t

def messageFromASCII(s):
	num = s.split()
	message = ""
	
	for i in num:
		temp = i
		while ((len(temp)%3) !=0):
			#add zeros to the beginning of the string if it is not divisible by 3
			#we do this because the ASCII table goes up to dec 127, a three digit number
			temp = "0" + temp
	
		pos=0
		while pos < len(temp):
			asc = int(temp[pos:pos+3])
			message = message+ chr(asc)
			pos +=3
	return message

def randomPrime():
	#returns two random prime numbers
	f = open('primes.txt') #primes.txt is a list of primes provided
	s = []

	for index in f:
		a = int(index.rstrip("\n"))
		s.append(a)

	i = random.randrange(0,len(s)+1,1)
	i2 = random.randrange(0, len(s)+1,1)
	return s[i], s[i2]

def generateKeys(p,q):
	#takes p and q and returns n, e, d, and digits in n
	n = p * q
	digit = len(str(n)) #math.floor(math.log(n,10))
	phi = (p-1)*(q-1)

	d = findCoprime(max(p,q), phi)
	e = findInverse(d, phi, 0, 1)
	if e < 0:
		e += phi

	return n, e, d, digit

# ------------- SET UP ------------- 
#these variables must be initiated 
n = 0
e = 0
d = 0
digit = 0

# ------------- ENCRYPTING AND DECRYPTING ------------- 
isRun = True
while (isRun):
	choice = input("""Choose an option:
	a. Encrypt with n and e provided in publicKey.txt.
	b. Decrypt with n and d provided in privateKeytxt.
	c. Input n and e and encrypt a message.
	e. Generate new keys.
	f. Display public keys in publicKey.txt.
	Enter anything else to quit.\n""")
	if choice == "a":
		try:
			publicKey = open("publicKey.txt", 'r')
			publ = publicKey.readlines()

			n = int(publ[0])
			e = int(publ[1])
			digit = len(str(n))

			publicKey.close()

			message = input("Message to encrypt: ")
			messageASCII = messageToASCII(message, digit)
			encrypted = encrypt(e, n, messageASCII)
			decrypted = decrypt(d, n, encrypted)
			# print("Message in English:", message)
			print("Message in ASCII:", messageASCII)
			print("Encrypted message:", encrypted)
		except IndexError:
			print("publicKey.txt is empty. Please generate keys first.")
		except FileNotFoundError:
			print("publicKey.txt is not found. Please generate keys first.")
	elif choice == "b":
		try:
			privateKey = open("privateKey.txt", 'r')
			priv = privateKey.readlines()

			n = int(priv[0])
			d = int(priv[1])
			digit = len(str(n))

			privateKey.close()

			encrypted = input("Message to decrypt: ")
			decrypted = decrypt(d, n, encrypted)
			print("Decrypted message in ASCII:", decrypted)
			print("Decrypted message in English:", messageFromASCII(decrypted))
		except IndexError:
			print("privateKey.txt is empty. Please generate keys first.")
		except FileNotFoundError:
			print("privateKey.txt is not found. Please generate keys first.")
	elif choice == "c":
		n2 = int(input("Choose an n: "))
		e2 = int(input("Choose an e: "))
		digit2= len(str(n2))
		message = input("Message to encrypt: ")
		messageASCII = messageToASCII(message, digit2)
		encrypted = encrypt(e2,n2, messageASCII)
		print("Encrypted:", encrypted)
	elif choice == "e":
		try:
			p, q = randomPrime()
			n,e,d,digit = generateKeys(p,q)
			privateKey = open("privateKey.txt", 'w')
			publicKey = open("publicKey.txt", 'w')
			privateKey.write(str(n)+"\n")
			privateKey.write(str(d))
			publicKey.write(str(n)+"\n")
			publicKey.write(str(e))
			publicKey.close()
			privateKey.close()
			print("New public key and private key have been written to text files.")
		except FileNotFoundError:
			print("primes.txt is not found.")
	elif choice == 'f':
		try:
			publicKey = open("publicKey.txt", 'r')
			publ = publicKey.readlines()

			n = int(publ[0])
			e = int(publ[1])
			digit = len(str(n))

			publicKey.close()

			print("n is", n)
			print("e is", e)
		except IndexError:
			print("publicKey.txt is empty. Please generate keys first.")
		except FileNotFoundError:
			print("publicKey.txt is not found. Please generate keys first.")
	else:
		print("Good bye~")
		isRun = False
