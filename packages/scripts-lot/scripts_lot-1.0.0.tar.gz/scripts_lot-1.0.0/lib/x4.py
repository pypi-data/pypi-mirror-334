import socket


def get_name():
    print("hello world")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

name = input("Enter your name: ")
cnic = input("Enter your CNIC: ")
client.send(f"{name},{cnic}".encode())

response = client.recv(1024).decode()
print(response)

if "Welcome" in response:
    candidates_list = client.recv(1024).decode()
    print(candidates_list)

    vote = input("Enter the poll symbol of the candidate you want to vote for: ")
    client.send(vote.encode())

    confirmation = client.recv(1024).decode()
    print(confirmation)

client.close()