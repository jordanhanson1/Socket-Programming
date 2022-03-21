import socket            
 


while True:
    command = input()

    firstWord=command.partition(' ')[0]
    secondWord=''
    if firstWord == "download":
        secondWord=command.partition(' ')[2]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    udpSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

 
    port = 32601             
 
    sock.connect(('127.0.0.1', port))
    
    if command=='listallfiles': 
        sock.send("listallfiles".encode())
        print (sock.recv(1024).decode())
        sock.close()
    elif command=='download all':
        sock.sendall("downloadall".encode())
        fileName=sock.recv(1024).decode()
        if fileName == 'DONE':
            break
        sock.sendall("OK".encode())
        fileSize=int(sock.recv(1024).decode())
        print(fileSize)
        sock.sendall("OK".encode())
        
        while fileName != "DONE":
            

            print(fileName)
            fileToDownload=open(fileName,"wb")


            
            while fileSize>0:
                chunk= 1024 if fileSize>1024 else fileSize
                data=sock.recv(chunk)
                fileSize=fileSize-chunk
                fileToDownload.write(data)

            fileToDownload.close()
            fileName=sock.recv(1024).decode()
            if fileName == 'DONE':
                break
            sock.sendall("OK".encode())
            fileSize=int(sock.recv(1024).decode())
            print(fileSize)
            sock.sendall("OK".encode())
        
        sock.close()
    elif firstWord == 'download' and secondWord != 'all':
        sock.sendall("downloadFile".encode())

        isOk= sock.recv(1024)
        if isOk != b'OK':
            print("something wrong")
        
        sock.sendall(secondWord.encode())


        isOk= sock.recv(1024)
        if isOk != b'OK':
            print("something wrong")

        sock.sendall("OK".encode())
        
        fileSize=int(sock.recv(1024).decode())
        print(fileSize)
        sock.sendall("OK".encode())
        fileToDownload=open(secondWord,"wb")

        udpSock.sendto("OK".encode(), ('127.0.0.1', 32602))
        while fileSize>0:
            chunk= 1024 if fileSize>1024 else fileSize
            data=udpSock.recvfrom(chunk)[0]
            print(data)
            fileSize=fileSize-chunk
            fileToDownload.write(data)
        
        fileToDownload.close()
        udpSock.close()
            




    elif command == 'exit':
        print("Exiting")
        sock.sendall("exit".encode())
        sock.close()
        break
    else:
        print("Command doesnt match anything")