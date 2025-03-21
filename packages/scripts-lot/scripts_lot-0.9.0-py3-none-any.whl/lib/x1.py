import socket
import threading
import json
import time

# Constants
MAX_CLIENTS = 5
ADMIN_CREDENTIALS = {"username": "admin", "password": "HotelManager"}
RESERVATIONS_FILE = "reservations.json"
TIME_SLOTS = ["4:00 PM", "6:00 PM", "8:00 PM", "10:00 PM"]

# Global variables
clients = []
waiting_queue = []
reservations = []

# Load reservations from file
def load_reservations():
    global reservations
    try:
        with open(RESERVATIONS_FILE, "r") as file:
            reservations = json.load(file)
    except FileNotFoundError:
        reservations = []

# Save reservations to file
def save_reservations():
    with open(RESERVATIONS_FILE, "w") as file:
        json.dump(reservations, file, indent=4)

# Client handler function
def handle_client(client_socket, address):
    global clients, waiting_queue
    
    try:
        client_socket.send("Welcome to the Restaurant Booking System!\n".encode())
        time.sleep(1)
        client_socket.send(f"Available Time Slots: {', '.join(TIME_SLOTS)}\n".encode())
        time.sleep(1)
        client_socket.send("Enter your preferred time slot or type 'exit' to disconnect: ".encode())

        # Handle client interaction
        preferred_time = client_socket.recv(1024).decode().strip()
        
        if preferred_time.lower() == 'exit':
            client_socket.send("Goodbye!\n".encode())
            client_socket.close()
            return

        if preferred_time not in TIME_SLOTS:
            client_socket.send("Invalid time slot. Disconnecting.\n".encode())
            client_socket.close()
            return

        reservation = {"client": address, "time_slot": preferred_time}
        reservations.append(reservation)
        save_reservations()

        client_socket.send(f"Your reservation for {preferred_time} has been confirmed!\n".encode())
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)
        if waiting_queue:
            next_client = waiting_queue.pop(0)
            clients.append(next_client)
            threading.Thread(target=handle_client, args=(next_client[0], next_client[1])).start()

# Admin handler function
def handle_admin():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
        print("\nReservations:")
        for idx, reservation in enumerate(reservations):
            print(f"{idx + 1}. Client: {reservation['client']}, Time Slot: {reservation['time_slot']}")
    else:
        print("Invalid credentials.")

# Main server function
def server():
    load_reservations()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(MAX_CLIENTS)
    print("Server started and listening on port 8080")

    while True:
        client_socket, address = server_socket.accept()

        if len(clients) < MAX_CLIENTS:
            clients.append(client_socket)
            print(f"Client {address} connected.")
            threading.Thread(target=handle_client, args=(client_socket, address)).start()
        else:
            waiting_queue.append((client_socket, address))
            client_socket.send("Server busy. You have been added to the waiting queue.\n".encode())

if __name__ == "_main_":
    threading.Thread(target=server).start()

    while True:
        print("\n1. View Reservations (Admin)")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            handle_admin()
        elif choice == "2":
            break


def get_name():
    print("hello world")