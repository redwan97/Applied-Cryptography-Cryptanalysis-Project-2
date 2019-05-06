from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

import os

current_path = os.path.dirname(os.path.abspath(__file__))								# Get the path of this script
publicKeyDirectory = os.path.join(current_path,'PublicKeys')							# Join the path of this script with the publickeys folder

def loadPrivateKey(name):
	privateFileName = name + '_private.pem'
	with open(privateFileName, 'rb') as file:
		privateKey = serialization.load_pem_private_key(
			file.read(),
			password = None,
			backend	= default_backend()	
		)
		return privateKey


def loadPublicKey(name):
	#Extra os stuff allows the saving of public key into the publicKey directory
	publicFileName = name + '_public.pem'
	publicFileName = os.path.join(publicKeyDirectory, publicFileName)
	with open(publicFileName, 'rb') as file:
		publicKey = serialization.load_pem_public_key(
			file.read(),
			backend	= default_backend()	
		)
		return publicKey

def generateKeys(name):
	#generates private key
	privateKey = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
		backend=default_backend()
	)

	#generates public key from private key
	publicKey = privateKey.public_key()

	#save private key to directory
	pem = privateKey.private_bytes(
	    encoding=serialization.Encoding.PEM,
	    format=serialization.PrivateFormat.PKCS8,
	    encryption_algorithm=serialization.NoEncryption()
	)

	privateFileName = name + '_private.pem'
	with open(privateFileName, 'wb') as f:
	    f.write(pem)

	#save public key to directory
	pem = publicKey.public_bytes(
	    encoding=serialization.Encoding.PEM,
	    format=serialization.PublicFormat.SubjectPublicKeyInfo
	)

	#Extra os stuff allows the saving of public key into the publicKey directory
	publicFileName = name + '_public.pem'
	publicFileName = os.path.join(publicKeyDirectory, publicFileName)
	with open(publicFileName, 'wb') as f:
	    f.write(pem)

	'''
	keys = {
		'public' : publicKey,
		'private' : privateKey
	}

	return keys
	'''

def encrypt(ptext, publicKey):
	ctext = publicKey.encrypt(
		ptext,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)

	)
	return ctext

def decrypt(ctext, privateKey):
	ptext = privateKey.decrypt(
		ctext,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return ptext


def test():
	generateKeys('test')
	prKey = loadPrivateKey('test')
	puKey = loadPublicKey('test')

	x = ("test text").encode()
	ct = encrypt(x, puKey)
	pt = decrypt(ct, prKey)

	print("Test: ", pt)


