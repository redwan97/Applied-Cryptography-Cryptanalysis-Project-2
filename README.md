# Secure Python-FTP
![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

Simple Python FTP server-client architecture that secures connection using asymmetric 
shared key encryption and cost effective symmetric decryption through the host.   

# Requirements
  - Python3
  - Modules: Cryptography, Sockets 

# Features
  - Send files to FTP server
  - Recieve files from FTP server

  # Process of securing FTP
  - Client and Server use Asymmetric encryption to establish secret key
  - Client and Server switch to Symmetric encryption using established secret key
  - Exchange files from client to server securely
  
### Installation
Simply clone the repo

```sh
$ git clone https://github.com/redwan97/Applied-Cryptography-Cryptanalysis-Project-2.git
```

### How To Use
To use navigate to both the /ServerDirectory and /ClientDirectory from the separate windows or machines. 
Make sure you are using Python3.

In the /ServerDirectory run the server.py file
```sh
$ python server.py
```

Now in the /ClientDirectory run the client.py file
```sh
$ python client.py
```

To make requests from the the client shell to the server the client will be queried for an option value

|         Options         |                 Function                   |
|         -------         |                 --------                   |
| s [S, send, Send]       | Requests to send a file to the server      |
| r [R, recieve, Recieve] | Requests to recieve a file from the server |

When specifying file names, make sure to include file extensions

### Todos
 - Add error handling for file i/o 
 - Write MORE options
 - Allow repeating listener
 - Add checksums
 - Use CA to back public keys
 
### Authors
 - Redwanul Mutee
 - William Uchegbu


License
----

MIT




