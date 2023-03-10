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
    server = str(f'{Colour.grey}[{Colour.green}SERVER{Colour.grey}]{Colour.white}')
    info = f'{Colour.grey}[{Colour.cyan}INFO{Colour.grey}]{Colour.white}'
    req = f'{Colour.grey}[{Colour.purple}REQ{Colour.grey}]{Colour.purple}'
    connect = f'{Colour.grey}[{Colour.green}+{Colour.grey}]{Colour.white}'
    disconnect = f'{Colour.grey}[{Colour.red}-{Colour.grey}]{Colour.white}'
    error = f'{Colour.grey}[{Colour.red}ERROR{Colour.grey}]{Colour.white}'

def getTime():
    return str(f'{Colour.grey}[{Colour.yellow}{dt.now().strftime("%H:%M:%S")}{Colour.grey}]{Colour.white}')

def handleAddress(address):
    return f'{Colour.grey}[{Colour.red}{str(address)[14:-1]}{Colour.grey}]{Colour.white}'

def broadcast(message):
    for client in clients:
        client.send(message)

def disconnect(client):
    while True:
        try:
            broadcast(client.recv(1024))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f' {getTime()} {Status.disconnect} {nickname}')
            broadcast(f' {getTime()} {Status.server} {nickname} disconnected from IRC.'.encode('ascii'))
            nicknames.remove(nickname)
            break

def connect():
    while True:
        client, address = server.accept()
        print(f' {getTime()} {Status.connect} {handleAddress(address)}')
        print(f" {getTime()} {Status.req} {handleAddress(address)} Nickname: ...")
        client.send(f'nickname: {handleAddress(address)}'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f' {getTime()} {Status.info} {handleAddress(address)} Nickname: {nickname}.')
        broadcast(f' {getTime()} {Status.server} {nickname} connected to IRC.'.encode('ascii'))
        clientHandler = threading.Thread(target=disconnect, args=(client,))
        clientHandler.start()

if __name__ == "__main__":
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8080))
        server.listen()

        clients, nicknames = [], []

        print(f' {getTime()} {Status.server} Started successfully.')
        connect()
    except Exception as e:
        print(f' {getTime()} {Status.error} {Colour.red}Server failed to start.{Colour.white}')