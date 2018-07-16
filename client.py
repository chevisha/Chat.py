import socket
import threading
import time
import sys
import msvcrt
from colorama import init, Fore, Style

tLock = threading.Lock()
shutdown = False
interupted=False 
message = ''
lastMessage = ''
tempMessage = ''
alias=''
adminPass=''
serverPass=''
legitName=False
kicked=False
legitLogin=False

def receving(name, sock):
    global lastMessage
    global alias
    global tempMessage
    global adminPass
    global legitName
    global message
    global kicked
    global legitLogin
    global serverPass
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                if (legitName==False):
                    adminPass=str(data)
                else:
                    if (legitLogin==False):
                        serverPass=str(data)
                    else:
                        if ("You have been kicked!"==str(data)):
                            kicked=True
                        sys.stdout.write(Style.RESET_ALL+'\r' + str(data)+(len(lastMessage+tempMessage)+len(addr))*'           ')
                        print ''
                        if (interupted==True):
                            sys.stdout.write(Fore.RED+Style.BRIGHT+alias + "-> "+lastMessage+tempMessage)
        except:
            pass
        finally:
            tLock.release()
            
 
def readInput( caption, timeout = 5):
    global interupted
    start_time = time.time()
    if (interupted==False):
        sys.stdout.write('%s'%(caption))
    input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13: # enter_key
                break
            elif ord(chr) >= 32: #space_char
                input += chr
            elif (chr=='\b') : #backspace_char
                inputTemp=''
                sys.stdout.write(' ')
                sys.stdout.write('\b')
                for i in range(len(input)-1):
                    inputTemp+=input[i]
                input=inputTemp
        if (time.time() - start_time) > timeout:
            interupted=True
            break
        else:
            interupted=False

    if (interupted==False):
        print ''  # needed to move to next line
    #if len(input) > 0:
        #return input
    return input

host = ''
port = 0

serverHost=raw_input("Enter server's IP address: ")
serverPort=raw_input("Enter server's port: ")

server = (serverHost,int(serverPort))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

init(convert=True)




while legitName!=True:
    alias = raw_input('Name: ')
    if alias.upper()=="ADMIN":
        s.sendto(alias+': '+'!~legit1~1Name~!',server)
        adminPassTry=raw_input('Enter administator password: ')
        if (adminPass!='') and (adminPass==adminPassTry):
             s.sendto(alias+': '+'Admin Confirm',server)
             legitName=True
             legitLogin=True
            
        else:
            print "Administrator login failed, try different login"
    else:
        legitName=True

while legitLogin!=True:
    s.sendto(alias+': ',server)
    serverPassTry=raw_input('Enter server password: ')
    if (serverPass!='') and (serverPass==serverPassTry):
        s.sendto(alias+': '+'Login Confirm',server)
        legitLogin=True
    else:
        print "Server login failed, try again"
            

while message!='/quit' and kicked==False:
    if (tempMessage+lastMessage != ''):
        if (interupted==False):
            message = lastMessage+tempMessage
            s.sendto(alias + ": " + message, server)
            lastMessage=''
        else:
            lastMessage+=tempMessage
    tLock.acquire()
    tempMessage = readInput(Fore.RED+Style.BRIGHT+alias + "-> "+lastMessage)
    tLock.release()
    time.sleep(0.2)
    
s.sendto(alias+": "+"/quit",server)
shudown = True
rT.join()
s.close()
