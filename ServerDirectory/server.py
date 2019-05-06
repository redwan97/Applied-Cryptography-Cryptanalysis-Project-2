from cryptography.fernet import Fernet
import socket
import keyGen

s = socket.socket()
host = socket.gethostname()
port = 8000
s.bind((host,port))
s.listen(1)
print("Waiting for any incoming connections ... ")
conn, addr = s.accept()
print(addr, " Has connected to the network")

secret_key = keyGen.generateKey()
clientOption = conn.recv(1024).decode()                                                                                 # Server recieves clients option of sending or recieving

if (clientOption == 's' or clientOption == 'S' or clientOption == 'send' or clientOption == 'Send'):                    
    print(addr, " is sending a file.")                                                                                  # The client is sending a file
    filename = input(str("Please enter a filename for the incoming file: "))                                            # Name the file to be recived  (something.txt), make sure to put .txt
    file_data = conn.recv(1024)                                                                                         # Recieved 1024 bytes, needs to be updated for larger files
    file = open(filename,'wb')                                                                                          # Open the named filed to be written into
    file.write(file_data)                                                                                               # Write into the opened file the recieved data
    file.close()                                                                                                        # Close file
    print("File has been received successfully")                                                                        # Let server know that file has been received

elif (clientOption == 'r' or clientOption == 'R' or clientOption == 'recieve' or clientOption == 'Recieve'):            
    print(addr, " is requesting a file.")                                                                               # The client wants to recieve a file
    filename = input(str("filename : "))                                                                                # Select the filename to send to client, include .txt
    file = open(filename,'rb')                                                                                          # Open file for reading
    filedata = file.read(1024)                                                                                          # Read the opened file 
    conn.send(filedata)                                                                                                 # Send the read file contents to client
    print("The file has been sent successfully")                                                                        # Let server know that file has been sent
    
else:
    print("Invalid option. Terminating program ...")


