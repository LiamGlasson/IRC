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
    server = str(f'{COLOUR.grey}[{COLOUR.green}SERVER{COLOUR.grey}]{COLOUR.white}')
    info = f'{COLOUR.grey}[{COLOUR.cyan}INFO{COLOUR.grey}]{COLOUR.white}'
    req = f'{COLOUR.grey}[{COLOUR.purple}REQ{COLOUR.grey}]{COLOUR.purple}'
    connect = f'{COLOUR.grey}[{COLOUR.green}+{COLOUR.grey}]{COLOUR.white}'
    disconnect = f'{COLOUR.grey}[{COLOUR.red}-{COLOUR.grey}]{COLOUR.white}'
    error = f'{COLOUR.grey}[{COLOUR.red}ERROR{COLOUR.grey}]{COLOUR.white}'

def getTime():
    return str(f'{COLOUR.grey}[{COLOUR.yellow}{dt.now().strftime("%H:%M:%S")}{COLOUR.grey}]{COLOUR.white}')

def handleAddress(address):
    return f'{COLOUR.grey}[{COLOUR.red}{str(address)[14:-1]}{COLOUR.grey}]{COLOUR.white}'

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
            print(f' {getTime()} {STATUS.disconnect} {nickname}')
            broadcast(f' {getTime()} {STATUS.server} {nickname} disconnected from IRC.'.encode('ascii'))
            nicknames.remove(nickname)
            break

def connect():
    while True:
        client, address = server.accept()
        print(f' {getTime()} {STATUS.connect} {handleAddress(address)}')
        print(f" {getTime()} {STATUS.req} {handleAddress(address)} Nickname: ...")
        client.send(f'nickname: {handleAddress(address)}'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f' {getTime()} {STATUS.info} {handleAddress(address)} Nickname: {nickname}.')
        broadcast(f' {getTime()} {STATUS.server} {nickname} connected to IRC.'.encode('ascii'))
        clientHandler = threading.Thread(target=disconnect, args=(client,))
        clientHandler.start()

if __name__ == "__main__":
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8080))
        server.listen()

        clients, nicknames = [], []

        print(f' {getTime()} {STATUS.server} Started successfully.')
        connect()
    except Exception as e:
        print(f' {getTime()} {STATUS.error} {COLOUR.red}Server failed to start.{COLOUR.white}')