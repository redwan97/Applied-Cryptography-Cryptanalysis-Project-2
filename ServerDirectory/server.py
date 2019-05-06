import socket
import os.path
import sys 

rsaLocation = os.path.abspath(os.path.join(os.getcwd(), os.pardir))                                                     # Get the current directory and find its parent directory, its where RSAkeys.py is located
sys.path.insert(0, rsaLocation)                                                                                         # Add that path to sys so it can be imported

import rsaKeys
import keyGen

rsaKeys.generateKeys('server')                                                                                          # Generate public-private key pair for server
server_private_key = rsaKeys.loadPrivateKey('server')                                                                   # Load server private key
server_public_key = rsaKeys.loadPublicKey('server')                                                                     # Load server public key
client_public_key = rsaKeys.loadPublicKey('client')                                                                     # Load client public key


s = socket.socket()
host = socket.gethostname()
port = 8000
s.bind((host,port))
s.listen(1)
print("Waiting for any incoming connections ... ")
conn, addr = s.accept()
print(addr, " Has connected to the network")

print(conn.recv(1024).decode())                                                                                         # Will let you know if client is ready for asymmetric handshake
SECRET_KEY = keyGen.generateKey()                                                                                       # Generate a secret key for symmetric encryption
encrypted_secret_key = rsaKeys.encrypt(SECRET_KEY, client_public_key)                                                   # Encrypt the secret key using clients public key (asymmetric encryption)
#print(encrypted_secret_key)
conn.send(encrypted_secret_key)                                                                                         # Send the encrypted secret key
print("Sent Secret Key to client encrypted using client public key ...")                                                # Let user know you have done so
#print(SECRET_KEY.decode())




# START ADDING SYMMETRIC ENCRYPTION HERE, SECRET KEY SHOULD BE NOW AVAILABLE TO BOTH

clientOption = conn.recv(1024).decode()                                                                                 # Server recieves clients option of sending or recieving
if (clientOption == 's' or clientOption == 'S' or clientOption == 'send' or clientOption == 'Send'):                    
    print(addr, " is sending a file.")                                                                                  # The client is sending a file
    filename = input(str("Please enter a filename for the incoming file: "))                                            # Name the file to be recived  (something.txt), make sure to put .txt
    file_data = conn.recv(1024) 

    #Takes file data and decrypts it using the secret key. This plain data is recieved instead of the cipher text file data
    pdata = keyGen.decryptMsg(file_data, SECRET_KEY)                                                                    # Recieved 1024 bytes, needs to be updated for larger files
    file = open(filename,'wb')                                                                                          # Open the named filed to be written into
    file.write(pdata)                                                                                                   # Write into the opened file the recieved data
    file.close()                                                                                                        # Close file
    print("File has been received successfully")                                                                        # Let server know that file has been received

elif (clientOption == 'r' or clientOption == 'R' or clientOption == 'recieve' or clientOption == 'Recieve'):            
    print(addr, " is requesting a file.")                                                                               # The client wants to recieve a file
    filename = input(str("filename : "))                                                                                # Select the filename to send to client, include .txt
    file = open(filename,'rb')                                                                                          # Open file for reading
    filedata = file.read(1024) 

    #Takes file data and encrypts it using the secret key. This cipher data is sent instead of the plain text file data
    cdata = keyGen.encryptMsg(filedata, SECRET_KEY)                                                                     # Read the opened file 
    conn.send(cdata)                                                                                                    # Send the read file contents to client
    print("The file has been sent successfully")                                                                        # Let server know that file has been sent
    
else:
    print("Invalid option. Terminating program ...")


