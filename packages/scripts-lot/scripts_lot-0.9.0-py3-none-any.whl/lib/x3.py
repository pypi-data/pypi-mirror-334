import socket
import threading


def get_name():
    print("hello world")


voters = {}
try:
    with open('Voters_List.txt', 'r') as file:
        for line in file:
            if ',' in line:
                name, cnic = line.strip().split(',')
                voters[cnic] = name
            else:
                print(f"Skipping invalid line in Voters_List.txt: {line.strip()}")
except FileNotFoundError:
    print("Voters_List.txt not found.")

print(voters)

candidates = {}
try:
    with open('Candidates_List.txt', 'r') as file:
        for line in file:
            if ',' in line:
                names, symbol = line.strip().split(',')
                candidates[symbol] = names
            else:
                print(f"Skipping invalid line in Candidates_List.txt: {line.strip()}")
except FileNotFoundError:
    print("Candidates_List.txt not found.")

voted_voters = set()

lock = threading.Lock()

def handle_client(client_socket, addr):
    print(f"Connection from {addr}")

    try:

        voter_details = client_socket.recv(1024).decode()
        name, cnic = voter_details.split(',')
        if cnic in voters and voters[cnic] == name:
            with lock:
                if cnic in voted_voters:
                    client_socket.send("You have already voted.".encode())
                else:
                    client_socket.send("Welcome! Please cast your vote.".encode())

                    candidates_list = "\n".join([f"{symbol}: {name}" for symbol, name in candidates.items()])
                    client_socket.send(candidates_list.encode())

                    vote = client_socket.recv(1024).decode()

                    with open('output.txt', 'a') as file:
                        file.write(f"{name},{cnic},{vote}\n")

                    voted_voters.add(cnic)

                    client_socket.send("Vote recorded successfully.".encode())
        else:
            client_socket.send("Authentication failed. You are not a registered voter.".encode())
    except Exception as e:
        client_socket.send(f"An error occurred: {str(e)}".encode())
    finally:
        client_socket.close()
        print(f"Connection with {addr} closed")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)

print("Server listening on port 12345")

while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()