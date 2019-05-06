from cryptography.fernet import Fernet

def generateKey():
	key = Fernet.generate_key()
	#print("Key Generated: ", key)

	file = open('key.key', 'wb')
	file.write(key)
	file.close()

#Get key
def readKey(filename):
	file = open(filename, 'rb')
	key = file.read()
	file.close()
	#print(key) 
	return key

def encryptMsg(msg, key):
	encoded = msg.encode()
	f = Fernet(key)
	encrypted = f.encrypt(encoded)
	return(encrypted)

def decryptMsg(msg, key): 
	f = Fernet(key)
	decrypted = f.decrypt(msg)
	return(decrypted.decode())

def encryptFile(filename, keyfilename):
	file = open(filename, 'rb')
	msg = file.read()
	file.close()
	encrypted = encryptMsg(msg, readKey(keyfilename))

	file = open('encrypted.txt', 'wb')
	file.write(encrypted)
	file.close()

def decryptFile(filename, keyfilename):
	file = open(filename, 'rb')
	msg = file.read()
	file.close()
	decrypted = decryptMsg(msg, readKey(keyfilename))

	file = open('decrypted.txt', 'wb')
	file.write(decrypted)
	file.close()





