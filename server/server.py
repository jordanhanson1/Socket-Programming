import socket   
import os         
 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udpPort= 32602

port = 32601               
host = "127.0.0.1" 


sock.bind((host, port))  
udpSock.bind((host,udpPort))    
sock.listen(1)
print("server running")

while True:
  client, address = sock.accept()   

  command = client.recv(1024).decode()
  if not command:
    break
  

  if command=='listallfiles':
    files=os.listdir('./')
    msg=''
    for fil in files:
      msg+=fil+' '
    client.send(msg.encode())
    
  
  if command == 'downloadFile':

    client.sendall('OK'.encode())
    fileName=client.recv(1024).decode()
    

    if not os.path.exists(fileName):
      client.sendall("no file".encode())
      
    else: 
      client.sendall("OK".encode())
      isOk=client.recv(1024)
      if isOk != b'OK':
        print("something wrong")
      

      toSend=open(fileName, "rb")
      fileSize=str(os.path.getsize(fileName))+' '
      client.sendall(fileSize.encode())
      isOk=client.recv(1024)
      if isOk != b'OK':
        print("something wrong")

      msg=udpSock.recvfrom(1024)
      isOk=msg[0]
      if isOk != b'OK':
        print(isOk)
        print("here something wrong")

      bits=toSend.read(1024)
      while bits:
        udpSock.sendto(bits, msg[1])
        bits=toSend.read(1024)
        
      
      toSend.close()
     

    
    

  
  if command == 'downloadall':
    files=os.listdir('./')

    for fileName in files:
      toSend=open(fileName, "rb")


      client.sendall(fileName.encode())
      isOk=client.recv(1024)
      if isOk != b'OK':
        print("something wrong")


      fileSize=str(os.path.getsize(fileName))+' '
      client.sendall(fileSize.encode())
      isOk=client.recv(1024)
      if isOk != b'OK':
        print("something wrong")
      
      bits=toSend.read(1024)
      while bits:
        client.sendall(bits)
        bits=toSend.read(1024)

      

      toSend.close()

    client.sendall('DONE'.encode())
    
    


  if command == 'exit':
    client.close()
    udpSock.close()
    break

  
  


sock.close()
udpSock.close()
   