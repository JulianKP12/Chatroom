from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from connection import Connection

CLIENTS = {}

host = "localhost"
port = 5432
server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
print("[DEBUG] Server started")

CLIENTS["Server"] = Connection("server", "Server", ("123.12.1.12", 69420))


def waitForCon(server):
	server.listen(5)
	print("[DEBUG] Listening for connections")

	while True:
		client, addr = server.accept()
		name = client.recv(1024).decode()

		if name in CLIENTS:
			client.send(bytes("This name is already in use, please try a different one!", "utf8"))
			print(f"[CONNECTION] Connection refused: Reason=Name in use, ip={addr[0]}")
			client.close()
			continue

		user = Connection(name, client, addr)
		CLIENTS[name] = user
		print(f"[CONNECTION] New connection from: name={name}, ip={addr[0]}")
		Thread(target=handleClient, args=(server, user)).start()


def handleClient(server, person):
	person.client.send(bytes("Server: Hi there! To leave, type \'!quit\'", "utf8"))
	broadcast(f"Server: {person.name} has joined the chat!")

	while True:
		try:
			msg = person.client.recv(1024).decode()
			if msg != "!quit":
				if msg == "":
					continue
				else:
					print(f"[RECIEVED] Recieved new message from {person.name}: {msg}")
					broadcast(f"{person.name}: {msg}")
			else:
				print(f"[CONNECTION] Connection from {person.addr[0]} closed by {person.name}")
				del CLIENTS[person.name]
				broadcast(f"Server: {person.name} has left the chat!")
				break
		except ConnectionResetError as e:
			print(f"[CONNECTION] Connection from {person.addr[0]} closed by {person.name}")
			del CLIENTS[person.name]
			broadcast(f"Server: {person.name} has left the chat!")
			break

	person.client.close()

def broadcast(message):
	print("[SENDING] Sending recieved message to all connections")
	for name in CLIENTS:
		if name != "Server":
			CLIENTS[name].client.send(bytes(message, "utf8"))
	print("[SENDING] Sent message to all connections")

if __name__ == "__main__":
	acceptThread = Thread(target=waitForCon, args=(server,))
	acceptThread.start()
	acceptThread.join()