import socket
import sys
import ssl
from _ssl import CERT_NONE

class SimpleClient:
   
    def __init__(self, messageFlag):
        self.messageFlag = messageFlag
    
    def connectToServer(self):
        """This function opens the socket connection to the server"""
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = ssl.wrap_socket(self.client_socket, cert_reqs=CERT_NONE)

        host  = 'cs5700sp15.ccs.neu.edu'
        port  = 27994

        remote_ip = socket.gethostbyname(host)

        try:
            self.client_socket.connect((remote_ip, port))
        except socket.error:
            print ('Connection failed')
            sys.exit()

        print ('Connection successful')
        
    
    def sendHelloMessage(self):
        """This funtion sends the initial HELLO message to the server"""
        
        nu_id = input('Enter your NUID: ')
        hello_message = 'cs5700spring2015 HELLO {}\n'.format(nu_id)
        
        try:
            self.client_socket.send(bytes(hello_message, 'ascii'))
        except socket.error:
            print ('Cannot send HELLO message')
            sys.exit()
        
    
    def receiveMessage(self):
        """This function receives the message from the server and checks whether
        the message is a STATUS message or BYE message"""
        
        try:
            self.receivedMesssage = self.client_socket.recv(1024)
        except socket.error:
            print ('Error: Message not received')
        
        self.receivedMesssage = self.receivedMesssage.decode('UTF-8')
        print (self.receivedMesssage)
        
        if 'BYE' in self.receivedMesssage:
            self.messageFlag = False
        
         
    def handleStatusMessage(self):
        """This function handles the STATUS message received from the server"""
        
        self.splitStatusMessage = self.receivedMesssage.split(' ')
        print (self.splitStatusMessage)
        
        
 
    def solveMathExpression(self):
        """This function solves the mathematical expression sent by the server"""
        
        first_number = int(self.splitStatusMessage[2])
        second_number = self.splitStatusMessage[4]
        second_number = int(second_number[:-1])
        
        if self.splitStatusMessage[3] == "+":
            self.solution = first_number + second_number
        elif self.splitStatusMessage[3] == "-":
            self.solution = first_number - second_number
        elif self.splitStatusMessage[3] == "*":
            self.solution = first_number * second_number
        else:
            self.solution = first_number / second_number
            self.solution = int(self.solution)
            
            
    def sendSolutionMessage(self):
        """This function sends the calculated value of the mathematical expression
        back to the server"""
        
        solutionMessage = 'cs5700spring2016 {}\n'.format(self.solution) 
        print (solutionMessage)
        self.client_socket.send(bytes(solutionMessage, 'ascii'))
        
        
        
    def byeMessage(self):
        """This function handles the BYE message received from the server"""
        
        if 'Unknown_Husky_ID' in self.receivedMesssage:
            print ('Incorrect NUID. Please retry by entering a valid NUID')
        else:
            splitByeMessage = self.receivedMesssage.split(' ')
            secretFlag = 'Your 64 byte secret flag is {}'.format(splitByeMessage[1])
            print (secretFlag)
        
        self.client_socket.close()


def main():
  client = SimpleClient(True)
  client.connectToServer()
  client.sendHelloMessage()
  
  while client.messageFlag == True:
      client.receiveMessage()
      if client.messageFlag == True:
          client.handleStatusMessage() 
          client.solveMathExpression()
          client.sendSolutionMessage()
        
  client.byeMessage()
      
    
if __name__ == "__main__":main()
