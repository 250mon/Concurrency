import socket

class UDPserver:
    def __init__(self, parent= None):
        self.localIP = "127.0.0.1"
        self.localPort = 20002
        self.bufferSize = 1024

        self.UDPServerSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_DGRAM)  # Create a socket object
        self.UDPServerSocket.bind((self.localIP, self.localPort))
        print("UDP server up and listening")
        self.counter = 1

    @staticmethod
    def mainLoopUDPserver():
            serv = UDPserver()

        #while(True):
            bytesAddressPair = serv.UDPServerSocket.recvfrom(serv.bufferSize)                     # Receive data from the socket
            message = bytesAddressPair[0]                                               # The output of the recvfrom() function is a 2-element array
            address = bytesAddressPair[1]                                               # Second element is the address of the sender
            newMsg = "{}".format(message)
            serv.counter = serv.counter + 1
            NumMssgReceived = "#Num of Msg Received:{}".format(serv.counter)

            newMsg = newMsg.replace("'", "")
            newMsg = newMsg.replace("b", "")
            newMsg = newMsg.split("/")

            eastCoord = float(newMsg[0])
            northCoord = float(newMsg[1])
            vehSpeed = float(newMsg[2])
            agYaw = float(newMsg[3])

            eastCoordStr = "East Coordinate:{}".format(newMsg[0])
            northCoordStr = "North Coordinate:{}".format(newMsg[1])
            vehSpeedStr = "Vehicle Speed:{}".format(newMsg[2])
            agYawStr = "Yaw Angle:{}".format(newMsg[3])

            print(NumMssgReceived)
            print(vehSpeedStr)