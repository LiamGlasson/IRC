import socket, threading
from datetime import datetime as dt

class COLOUR:
    white = '\033[1;37;40m'
    green = '\033[1;32;40m'
    yellow = '\033[1;33;40m'
    red = '\033[1;31;40m'
    cyan = '\033[1;36;40m'
    grey = '\033[1;30;40m'
    purple = '\033[1;35;40m'

    # If you want to disable colours, uncomment the following line:
    # white, green, yellow, red, cyan, grey, purple = '', '', '', '', '', '', ''

class STATUS:
    local = f'{COLOUR.grey}[{COLOUR.cyan}LOCAL{COLOUR.grey}]{COLOUR.white}'
    server = f'{COLOUR.grey}[{COLOUR.green}SERVER{COLOUR.grey}]{COLOUR.white}'
    error = f'{COLOUR.grey}[{COLOUR.red}ERROR{COLOUR.grey}]{COLOUR.white}'

def getTime():
    return f'{COLOUR.grey}[{COLOUR.yellow}{dt.now().strftime("%H:%M:%S")}{COLOUR.grey}]{COLOUR.white}'

def handleName(client):
    return f'nickname: {COLOUR.grey}[{COLOUR.red}{str(client).split(", ")[5][:-1]}{COLOUR.grey}]{COLOUR.white}'

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == handleName(client):
                client.send(nickname.encode('ascii'))
            else:
                print(message) 
        except:
            print(f' {getTime()} {STATUS.error} {COLOUR.red}Server Closed.{COLOUR.white}')
            client.close()
            break

def send():
    while True:
        content = input("")
        message = f' {getTime()} {COLOUR.grey}[{COLOUR.green}{nickname}{COLOUR.grey}] {COLOUR.white}{content}'
        client.send(message.encode('ascii'))

if __name__ == "__main__":
    try:
        nickname = input(f' {getTime()} {STATUS.local} Enter Nickname{COLOUR.grey}> {COLOUR.yellow}')
        print(f' {getTime()} {STATUS.local} Attempting to connect...\n')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8080))
    
        receiveMessages = threading.Thread(target=receive)
        receiveMessages.start()

        sendMessages = threading.Thread(target=send)
        sendMessages.start()
    except:
        print(f' {getTime()} {STATUS.error} {COLOUR.red}Invalid host and/or port.{COLOUR.white}')