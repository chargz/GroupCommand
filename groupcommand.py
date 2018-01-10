import pxssh
import optparse

class Client:

	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password
		self.session = self.connect()

	def connect(self):
		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password)
			return s
		except Exception, e:
			print e
			print 'Error Connecting'

	def send_command(self, cmd):
		self.session.sendline(cmd)
		self.session.prompt()
		return self.session.before

def runCommand(command):
	for client in clientList:
	output = client.send_command(command)
	print 'Output from ' + client.host
	print output + '\n'

def addClient(host, user, password):
	client = Client(host, user, password)
	clientList.append(client)

clientList = []

addClient('10.10.10.110', 'root', 'toor')


runCommand('top')
runCommand('cat /etc/issue')