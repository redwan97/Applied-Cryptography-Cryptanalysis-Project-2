import socket

s = socket.socket()
host = socket.gethostname() 
#host = input(str("Please enter host address of the sender: "))                                                
port = 8000
s.connect((host,port))
print("Connected ...")

option = input("Send or recieve file? (s/r) : ")                                                    # Client specifies whether to send or recieve file
s.send(option.encode())                                                                             # Sends this information to server 

if (option == 's' or option == 'S' or option == 'send' or option == 'Send'):                        # The client is sending a file
    filename = input(str("filename : "))                                                            # Select the filename to send to server, include .txt
    file = open(filename,'rb')                                                                      # Open file for reading
    filedata = file.read(1024)                                                                      # Read the opened file
    s.send(filedata)                                                                                # Send the read file contents to client
    print("The file has been sent successfully")                                                    # Let client know that file has been sent

elif (option == 'r' or option == 'R' or option == 'recieve' or option == 'Recieve'):                # The client wants is recieving a file
    filename = input(str("Please enter a filename for the incoming file: "))                        # Name the file to be recived  (something.txt), make sure to put .txt
    file_data = s.recv(1024)                                                                        # Recieved 1024 bytes, needs to be updated for larger files
    file = open(filename,'wb')                                                                      # Open the named filed to be written into
    file.write(file_data)                                                                           # Write into the opened file the recieved data
    file.close()                                                                                    # Close file
    print("File has been received successfully")                                                    # Let client know that file has been received

else:
    print("Invalid option. Terminating program ...")




