import sys, socket, select, pickle
 
def client():
    if(len(sys.argv) < 3) :
        print 'Usage : python client.py host port'
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # connect to host
    try :
        server_socket.connect((host, port))
    except :
        print 'Failed to connect :('
        sys.exit()
     
    print 'Connected :)'
     
    socket_list = [sys.stdin, server_socket]
    while True:
        sys.stdout.write('Me: ')
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
                    print '\nDisconnected :('
                    sys.exit()
            
            else :
                # send message
                mesg = sys.stdin.readline()
                server_socket.send(mesg)  
                

if __name__ == "__main__":
    sys.exit(client())

    # JSON too fixed? Pickle is python-specific but would be able to send dictionary
