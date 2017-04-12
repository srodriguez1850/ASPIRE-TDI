import sys, socket, select
try: 
    # for Python2
    from Tkinter import Tk, Label, Button
except ImportError:
    # for Python3
    from tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master, server_socket):
        self.master = master
        self.server = server_socket
        master.title("GUI")

        self.label = Label(master, text="Click to send command!")
        self.label.pack()

        self.greet_button = Button(master, text="Send Command", command=self.sendCommand)
        self.greet_button.pack()

    def sendCommand(self):
        self.server.send(b"bring_obj_to_user")

 
def client():
    if(len(sys.argv) < 3) :
        print('Usage : python client.py host port')
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # connect to host
    try :
        server_socket.connect((host, port))
    except :
        print('Failed to connect :(')
        sys.exit()
     
    print('Connected :)')

    root = Tk()
    my_gui = MyFirstGUI(root, server_socket)
    root.mainloop()
     
    socket_list = [sys.stdin, server_socket]
    while True:
        sys.stdout.flush()
         
        # Get readable sockets
        reads, writes, exceptions = select.select(socket_list , [], [])
         
        for sock in reads:            
            if sock == server_socket:
                mesg = sock.recv(4096)
                if mesg :
                    # print message
                    sys.stdout.write(mesg) 
                else :
                    # disconnected
                    print('\nDisconnected :(')
                    sys.exit()
            
            else :
                # send message
                mesg = sys.stdin.readline()
                server_socket.send(mesg.encode())  
                

if __name__ == "__main__":
    sys.exit(client())

    # JSON too fixed? Pickle is python-specific but would be able to send dictionary
