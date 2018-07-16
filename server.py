import socket
import time


host = ''
port = 1234
host=raw_input("Enter server host(leave blank if you host on current IP Address): ")
port=raw_input("Enter host's open port: ")

clients = []
alias=[]
pending=[]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,int(port)))
s.setblocking(0)

quitting = False
adminArrive=False
passSend=False
serverAdminPass=raw_input("Please enter server administrator password: ")
serverPass=raw_input("Please enter server password: ")
if host=="":
    host1="Public IP Address"
else:
    host1=host
print "Server Started at %s:%s" %(host1,port)
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        arr=str(data).split(': ')
        if arr[0].upper()=="ADMIN" and adminArrive==False:
            s.sendto(serverAdminPass, addr)
            if arr[1]=="Admin Confirm":
                adminArrive=True
                clients.append(addr)
                alias.append(arr[0])
        else:
            #admin commands and atributes
            if "/stopserver"==arr[1] and arr[0].upper()=="ADMIN":   #closing server
                quitting = True
                
            if arr[0].upper()=="ADMIN":     #admin recognizing color
                adminAtr="\033[32m\033[01m"
            else:
                adminAtr=""
                
            if "/kick" in arr[1] and arr[0].upper()=="ADMIN":
                x=alias.index(arr[1].split('--')[1])
                s.sendto("You have been kicked!",clients[x])
                clients.remove(clients[x])
                alias.remove(alias[x])
                data="Client with alias %s has been kicked from session" %(arr[1].split('--')[1])
                
            #clients commands
            if arr[1]=="/quit":                 #quit session
                clients.remove(addr)
                alias.remove(arr[0])
            
            
                
            #adding new client
            if arr[0] not in alias and arr[0].upper()!="ADMIN":
                if (arr[0] not in pending):
                    pending.append(arr[0])
                    s.sendto(serverPass, addr)
                    continue
                else:
                    if (arr[1]=="Login Confirm"):
                        clients.append(addr)
                        alias.append(arr[0])
                        pending.remove(arr[0])
                        continue
                    else:
                        continue
                
            #server temp log
            if arr[1]!='!~legit1~1Name~!':
                print time.ctime(time.time()) + str(addr) + ">==> " +str(data)
            else:
                continue
            
            #sending to other clients
            i=0
            data=adminAtr+str(data)
            for al in alias:
                if (al!=arr[0]):
                    s.sendto(data, clients[i])
                i+=1
        
    except:
        pass
s.close()
