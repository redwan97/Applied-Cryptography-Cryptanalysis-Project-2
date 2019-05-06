from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa




def loadPrivateKey():
	with open('private.pem', 'rb') as file:
		privateKey = serialization.load_pem_private_key(
			file.read(),
			password = None,
			backend	= default_backend()	
		)

def loadPublicKey():
	with open('public.pem', 'rb') as file:
		publicKey = serialization.load_pem_public_key(
			file.read(),
			password = None,
			backend	= default_backend()	
		)

def generateKeys():
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

	with open('private.pem', 'wb') as f:
	    f.write(pem)

	#save public key to directory
	pem = publicKey.public_bytes(
	    encoding=serialization.Encoding.PEM,
	    format=serialization.PublicFormat.SubjectPublicKeyInfo
	)

	with open('public.pem', 'wb') as f:
	    f.write(pem)

	keys = {
		'public' : publicKey,
		'private' : privateKey
	}

	return keys


def encrypt(ptext, publicKey):
	ctext = publicKey.encrypt(
		ptext,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA1()),
			algorithm=hashes.SHA1(),
			label=None
		)

	)
	return ctext

def decrypt(ctext, privateKey):
	ptext = privateKey.decrypt(
		ctext,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA1()),
			algorithm=hashes.SHA1(),
			label=None
		)
	)
	return ptext