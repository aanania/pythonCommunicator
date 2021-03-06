from ICommunicator import ICommunicator
import socket

NOERROR = 0
ERROR = -1

class TcpClient(ICommunicator):
	"""Class to handle TCP connection
	----------
	address : ``string``
		Address of the TCP server
	port : `int` 
		Port to connect to the TCP Server
	connectTimeout : `int` 
		Timeout to connect to the TCP server
	readTimeout : `int` 
		Timeout to read messages from the TCP server
	sendTimeout : `int` 
		Timeout to send messages to the TCP server
	Notes """
	def __init__(self, address, port, connectTimeout=2, readTimeout=2, sendTimeout=2):
		self.address = address
		self.port = port
		self.connectTimeout = connectTimeout
		self.readTimeout = readTimeout
		self.sendTimeout = sendTimeout
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = False 

	def connect(self):
		"""Class to handle TCP connection
		"""
		try:
			self.clientSocket.settimeout(self.connectTimeout)
			self.clientSocket.connect((self.address, self.port))
			self.connected = True 
			return NOERROR, ""
		except socket.error as e:
			#print("Couldn't connect with the socket-server: "+str(e))
			return ERROR, e

	def disconnect(self):
		self.connected = False
		self.clientSocket.close()
		
	def getMessage(self):
		self.clientSocket.settimeout(self.readTimeout)

		
	def sendMessage(self, message):
		self.clientSocket.settimeout(self.sendTimeout)
		
	def reconnect(self):
		"""Reconnect tcp connection
		"""
		self.disconnect()
		errorCode, errorMsg = self.connect()
		return errorCode, errorMsg
		
	def isConnected(self):
		return self.connected
		
class TcpClienEndChar(TcpClient):

	def __init__(self, address, port, connectTimeout=2, readTimeout=2, sendTimeout=2, endStr="\n", maxLength = 1024):
		super().__init__(address, port, connectTimeout, readTimeout, sendTimeout)
		self.endStr = endStr
		self.maxLength = maxLength
		
	def getMessage(self):
		"""Placeholder to get message"""
		super().getMessage()
		endStrLen = len(self.endStr)
		print(endStrLen)
		message = ""
		OK = ERROR
		try:
			
			for i in range(self.maxLength):
				lastMsg = self.clientSocket.recv(endStrLen).decode("utf-8") 
				message += lastMsg
				if(lastMsg == self.endStr):
					OK = NOERROR
					break
			if(OK == ERROR):
				return OK, message, "Message not ended"
			if(OK == NOERROR):
				return NOERROR, message, ""
				
		except socket.error as e:
			return ERROR, "", e
			
		return ERROR, message, "Message not ended"
			
	def sendMessage(self, message):
		"""Placeholder to send message"""
		internalMessage = message.encode('utf8')
		super().sendMessage(internalMessage)
		try:
			self.clientSocket.send(internalMessage)
			return NOERROR, ""
		except socket.error as e:
			self.connected = False #if the message couldn't be sent, it will assume that the device is not connected
			return ERROR, e
			
			
class TcpServer(ICommunicator):
	"""Class to handle TCP Server connection, connect will listen (connectionTimeout seconds) until connects to the server
	----------
	address : ``string``
		Address of the TCP server
	port : `int` 
		Port to connect to the TCP Server
	connectTimeout : `int` 
		Timeout to connect to the TCP server
	readTimeout : `int` 
		Timeout to read messages from the TCP server
	sendTimeout : `int` 
		Timeout to send messages to the TCP server
	Notes """
	def __init__(self, address, port, connectTimeout=600, readTimeout=2, sendTimeout=2):
		self.address = address
		self.port = port
		self.connectTimeout = connectTimeout
		self.readTimeout = readTimeout
		self.sendTimeout = sendTimeout
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection = 0
		self.client_address = ""
		self.connected = False 

	def connect(self):
		"""Class to handle TCP connection
	
		Returns error code:
		NOERROR: Successfully connected
		ERROR: Couldn't connect 
		"""
		try:
			self.serverSocket.settimeout(self.connectTimeout)
			self.serverSocket.bind((self.address, self.port))
			self.serverSocket.listen(1)
			self.connection, self.client_address = self.serverSocket.accept()
			self.connected = True
			return NOERROR, ""
		except connection.error as e:
			#print("Couldn't connect with the socket-server: "+str(e))
			return ERROR, e

	def disconnect(self):
		"""Disconnect from server"""
		self.connected = False
		self.connection.close()
		
	def getMessage(self):
		"""Placeholder to get message"""
		self.connection.settimeout(self.readTimeout)

		
	def sendMessage(self, message):
		"""Placeholder to send message"""
		self.connection.settimeout(self.sendTimeout)
		
	def reconnect(self):
		self.disconnect()
		errorCode, errorMsg = self.connect()
		return errorCode, errorMsg

	def isConnected(self):
		return self.connected
		
class TcpServerEndChar(TcpServer):

	def __init__(self, address, port, connectTimeout=600, readTimeout=2, sendTimeout=2, endStr="\n", maxLength = 1024):
		super().__init__(address, port, connectTimeout, readTimeout, sendTimeout)
		self.endStr = endStr
		self.maxLength = maxLength
		
	def getMessage(self):
		""""""
		super().getMessage()
		endStrLen = len(self.endStr)
		print(endStrLen)
		message = ""
		OK = ERROR
		try:
			
			for i in range(self.maxLength):
				lastMsg = self.connection.recv(endStrLen).decode("utf-8") 
				message += lastMsg
				if(lastMsg == self.endStr):
					OK = NOERROR
					break
			if(OK == ERROR):
				return OK, message, "Message not ended"
			if(OK == NOERROR):
				return NOERROR, message, ""
				
		except connection.error as e:
			return ERROR, "", e
			
		return ERROR, message, "Message not ended"
			
	def sendMessage(self, message):
		internalMessage = message.encode('utf8')
		super().sendMessage(internalMessage)
		try:
			self.connection.send(internalMessage)
			return NOERROR, ""
		except connection.error as e:
			self.connected = False #if the message couldn't be sent, it will assume that the device is not connected
			return ERROR, e			