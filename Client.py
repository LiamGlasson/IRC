import socket, threading
from datetime import datetime as dt

class Colour:
    white = '\033[1;37;40m'
    green = '\033[1;32;40m'
    yellow = '\033[1;33;40m'
    red = '\033[1;31;40m'
    cyan = '\033[1;36;40m'
    grey = '\033[1;30;40m'
    purple = '\033[1;35;40m'

    # If you want to disable colours, uncomment the following line:
    # white, green, yellow, red, cyan, grey, purple = '', '', '', '', '', '', ''

class Status:
    local = f'{Colour.grey}[{Colour.cyan}LOCAL{Colour.grey}]{Colour.white}'
    server = f'{Colour.grey}[{Colour.green}SERVER{Colour.grey}]{Colour.white}'
    error = f'{Colour.grey}[{Colour.red}ERROR{Colour.grey}]{Colour.white}'

def getTime():
    return f'{Colour.grey}[{Colour.yellow}{dt.now().strftime("%H:%M:%S")}{Colour.grey}]{Colour.white}'

def handleName(client):
    return f'nickname: {Colour.grey}[{Colour.red}{str(client).split(", ")[5][:-1]}{Colour.grey}]{Colour.white}'

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == handleName(client):
                client.send(nickname.encode('ascii'))
            else:
                print(message) 
        except:
            print(f' {getTime()} {Status.error} {Colour.red}Server Closed.{Colour.white}')
            client.close()
            break

def send():
    while True:
        content = input("")
        message = f' {getTime()} {Colour.grey}[{Colour.green}{nickname}{Colour.grey}] {Colour.white}{content}'
        client.send(message.encode('ascii'))

if __name__ == "__main__":
    try:
        nickname = input(f' {getTime()} {Status.local} Enter Nickname{Colour.grey}> {Colour.yellow}')
        print(f' {getTime()} {Status.local} Attempting to connect...\n')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8080))
    
        receiveMessages = threading.Thread(target=receive)
        receiveMessages.start()

        sendMessages = threading.Thread(target=send)
        sendMessages.start()
    except:
        print(f' {getTime()} {Status.error} {Colour.red}Invalid host and/or port.{Colour.white}')