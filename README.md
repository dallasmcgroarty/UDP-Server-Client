# UDP-Server-Client
program to send data from client to server via UDP

Language: Python

Server sets up and holds a file and waits for client to send a LIST message, the server responds to the client with a list of available sections of the file, the client then requests sections of the file that the server holds, the server services the requests back to the client. The client verifies the file contents to ensure no errors.

Ran on linux or windows machine, python in windows, python3 on linux. 

Run server in terminal: python3 SectionServer.py testfile.gz

Run client in terminal: python3 SectionClient.py localhost testfile.gz

