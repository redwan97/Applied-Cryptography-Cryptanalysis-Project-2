import socket
import os
import sys

rsaLocation = os.path.abspath(os.path.join(os.getcwd(), os.pardir))                                 # Get the current directory and find its parent directory, its where RSAkeys.py is located
sys.path.insert(0, rsaLocation)                                                                     # Add that path to sys so it can be imported

import rsaKeys
import keyGen

s = socket.socket()
host = socket.gethostname()                                                                         # host = input(str("Please enter host address of the sender: "))                                                
port = 8000
s.connect((host,port))
print("Connected to ", host, " ... ")

rsaKeys.generateKeys('client')                                                                      # Generate public-private key pair for client
client_private_key = rsaKeys.loadPrivateKey('client')                                               # Load client private key
client_public_key = rsaKeys.loadPublicKey('client')                                                 # Load client public key
server_public_key = rsaKeys.loadPublicKey('server')                                                 # Load server public key


s.send(b'Ready to do asymmetric encryption to establish shared secret key ...')                     # Let server know that the client is ready to asymmetric handshake
encrypted_secret_key = s.recv(1024)                                                                 # Recieve the encrypted secret key
#print(encrypted_secret_key)
SECRET_KEY = None
try:
    SECRET_KEY = rsaKeys.decrypt(encrypted_secret_key, client_private_key)                          # Try to decrypt the secret key using clients private key
except ValueError:                                                                                  # If error, then manually extract secret key ... error sometimes occurs ...
    print("Encountered error trying to decrypt. Manually taking secret key ...")
    filename = os.path.join(rsaLocation,'ServerDirectory','secretkey.key')
    file = open(filename,'rb')
    SECRET_KEY = file.read(1024)

print("Recieved Secret Key from server. Decrypted using client private key ...")
#print(SECRET_KEY.decode())

# START ADDING SYMMETRIC ENCRYPTION HERE, SECRET KEY SHOULD BE NOW AVAILABLE TO BOTH
option = input("Send or recieve file? (s/r) : ")                                                    # Client specifies whether to send or recieve file
s.send(option.encode())                                                                             # Sends this information to server 

if (option == 's' or option == 'S' or option == 'send' or option == 'Send'):                        # The client is sending a file
    filename = input(str("filename : "))                                                            # Select the filename to send to server, include .txt
    file = open(filename,'rb')                                                                      # Open file for reading
    filedata = file.read(1024)

    #Takes file data and encrypts it using the secret key. This cipher data is sent instead of the plain text file data
    cdata = keyGen.encryptMsg(filedata, SECRET_KEY)                                                 # Read the opened file
    s.send(cdata)                                                                                   # Send the read file contents to client
    print("The file has been sent successfully")                                                    # Let client know that file has been sent

elif (option == 'r' or option == 'R' or option == 'recieve' or option == 'Recieve'):                # The client wants is recieving a file
    filename = input(str("Please enter a filename for the incoming file: "))                        # Name the file to be recived  (something.txt), make sure to put .txt
    file_data = s.recv(1024)

    #Takes file data and decrypts it using the secret key. This plain data is recieved instead of the cipher text file data
    pdata = keyGen.decryptMsg(file_data, SECRET_KEY)                                                # Recieved 1024 bytes, needs to be updated for larger files
    file = open(filename,'wb')                                                                      # Open the named filed to be written into
    file.write(pdata)                                                                               # Write into the opened file the recieved data
    file.close()                                                                                    # Close file
    print("File has been received successfully")                                                    # Let client know that file has been received

else:
    print("Invalid option. Terminating program ...")




