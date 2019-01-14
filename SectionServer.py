#Dallas McGroarty
import sys
import socket as sock
import hashlib

PORT = 7037

MAX_UDP_PAYLOAD = 65507

def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

def get_file_info():
    file_name = sys.argv[1]
    send_output = ''
    section_digest = [] #list holding checksums
    section = []    #list holding bytes of each section
    file_contents = bytearray()     #byte array to hold all of file contents

    with open(file_name, 'rb') as file_by_chunks:
        while True:
            chunk = file_by_chunks.read(32768)
            chunk_size = len(chunk) #get size of the chunk
            if chunk_size != 0:
                chunk_size = len(chunk) #get size of the chunk
                md5_chunk = md5(chunk)  #checksum chunk
                section.append(chunk_size)  #add size to section list
                section_digest.append(md5_chunk)    #add checksum of chunk to section digest list
                file_contents.extend(chunk)
            else:
                break

        send_output += md5(file_contents) + '\n' #add the checksum of the total file contents
            
        #loop through sections and add section info to the ouput string
    for i in range(len(section)):
        if (i == len(section)):
            send_output += str(i) + ' ' + str(section[i]) + ' ' + section_digest[i]
        else:
            send_output += str(i) + ' ' + str(section[i]) + ' ' + section_digest[i] + '\n'

    return send_output, section

def main():

    serverSocket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    serverSocket.bind(('', PORT))
    print("Server is ready")
    #call get_file_info so all requests can be served in any order
    send_list, section = get_file_info()


    while True:
        message, clientAddress = serverSocket.recvfrom(MAX_UDP_PAYLOAD)
        recvData = message.decode()
        #check if LIST message was received
        if(recvData == 'LIST'):  
            serverSocket.sendto(send_list.encode(), clientAddress)    #send message to client
            print('Sent List:')
            print(send_list)
        
        #split the string received to access the n section number
        recvData = recvData.split()

        #check if SECTION message was received
        if(recvData[0] == 'SECTION'):
            n = recvData[1]
            n = int(n)
            send_section_size = section[n]
            send_section_size = bytes(send_section_size)
            serverSocket.sendto(send_section_size, clientAddress)
            print('Size of Section ' + str(n) + ' Sent')

main()