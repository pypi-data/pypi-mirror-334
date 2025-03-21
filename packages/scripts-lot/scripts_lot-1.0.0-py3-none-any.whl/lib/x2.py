import socket

def get_name():
    print("hello world")


def client():
    server_address = ('127.0.0.1', 8080)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        print("Connected to the Restaurant Booking System\n")

        while True:
            # Receive messages from the server
            message = client_socket.recv(1024).decode()
            print(message)

            # If server indicates to disconnect, break the loop
            if "Disconnecting" in message or "Goodbye" in message:
                break

            # User input to interact with the server
            user_input = input("Enter your response: ")
            client_socket.send(user_input.encode())

            # If the user decides to exit
            if user_input.lower() == 'exit':
                print("Exiting the system.")
                break

    except ConnectionError:
        print("Connection to the server was lost.")
    finally:
        client_socket.close()

if __name__ == "_main_":
    client()