from graphics import *
from socket import AF_INET, socket, SOCK_STREAM
from time import sleep

def main():
	win = GraphWin("Chat client", 600, 600)
	win.setBackground(color_rgb(108, 86, 120))

	welcomeText = Text(Point(300, 75), "Chatroom Client")
	welcomeText.setSize(28)
	welcomeText.setStyle("bold")
	welcomeText.setTextColor("white")
	welcomeText.setFace("arial")
	welcomeText.draw(win)

	nameEntry = Entry(Point(300, 325), 16)
	nameEntry.setFill("white")
	nameEntry.draw(win)

	nameText = Text(Point(265, 300), "Name:")
	nameText.setSize(18)
	nameText.setTextColor("white")
	nameText.setFace("arial")
	nameText.draw(win)

	submitBtn = Rectangle(Point(377, 313), Point(430, 336))
	submitBtn.setFill("white")
	submitBtn.draw(win)

	submitText = Text(Point(403, 325), "Submit")
	submitText.draw(win)
	
	while True:
		key = win.checkKey()

		if key == "Return":
			name = nameEntry.getText()
			if len(name) == 0 or len(name) >= 16:
				continue
			else:
				win.close()
				chatWin(name)
				break

		mouse = win.checkMouse()
		if mouse:
			if mouse.getX() <= 430 and mouse.getX() >= 377 and mouse.getY() <= 336 and mouse.getY() >= 313:
				name = nameEntry.getText()
				if len(name) == 0 or len(name) >= 16:
					continue
				else:
					win.close()
					chatWin(name)
					break


def chatWin(username):
	host = "localhost"
	port = 5432
	server = socket(AF_INET, SOCK_STREAM)
	server.connect((host, port))
	server.send(bytes(username, "utf8"))
	returnMsg = server.recv(1024).decode()

	win = GraphWin("Chat client", 600, 600)
	win.setBackground(color_rgb(108, 86, 120))

	msgBox = Rectangle(Point(50, 50), Point(550, 500))
	msgBox.setFill("white")
	msgBox.setOutline("black")
	msgBox.draw(win)

	msgEntry = Entry(Point(232, 520), 40)
	msgEntry.setFill("white")
	msgEntry.draw(win)

	msgSend = Rectangle(Point(415, 508), Point(470, 531))
	msgSend.setFill("white")
	msgSend.draw(win)

	msgSendText = Text(Point(443, 519), "Send")
	msgSendText.draw(win)

	


	server.close()



if __name__ == "__main__":
	main()







# from socket import AF_INET, socket, SOCK_STREAM

# name = str(input("What name do you want to use? "))

# host = "localhost"
# port = 5432
# server = socket(AF_INET, SOCK_STREAM)
# server.connect((host, port))
# server.send(bytes(name, "utf8"))
# print(f"Recieved from server: {server.recv(1024).decode()}")

# while True:
# 	msg = str(input(">> "))
# 	server.send(bytes(msg, "utf8"))
# 	if msg == "!quit":
# 		break

# server.close()