import socket
import threading

def handle_client(client_socket, clients, client_number):       #this function basically takes data from one client
    client_socket.send(str(client_number).encode())             #and sends it to the other client
                                                                #this function is called by a thread so each client
    while True:                                                 #has its own thread and therefore this function too
        data = client_socket.recv(1024)
        print(f"Received from client {client_number}: {data.decode('utf-8')}")

        if not data:
            break

        # Send the received data to the target client
        target_client_number = 1 if client_number == 2 else 2

        target_client = None            #loop through clients list, client is the current element in clients;
        for client, client_id in clients:       #client_id takes on the value of the 2nd element in the
            if client_id == target_client_number:
                target_client = client              #the list is basically a 2d array
                break                               #clients[]= client_info, client_id

        target_client.send(data)

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(50)  # Listen for two clients
    print("Server listening on port 8080")


    for i in range(1,26):#allows for multiple online games by looping many times; each loop gathers 2 players
        clients = []  # List to store connected clients

        for client_number in range(1, 3):  # Loops twice, first with client_number=1 and then 2
            client, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Assign number to the client
            clients.append((client, client_number)) #each element of clients will contain two elements: client info and client number

            # thread for each client
            thread = threading.Thread(target=handle_client, args=(client, clients, client_number))
            thread.start()

start_server()

