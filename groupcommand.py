from pexpect import pxssh
import optparse
import csv

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

with open('clientList.txt', 'rb') as readlist:
    reader = csv.reader(readlist)
    clientList = list(reader)

inp = raw_input("Enter: \n1 if you want to manually submit the SSH credentials:\n2 if you want to specify a file with credentials:\n3 to run a command on your Client List:\n")

if inp == "1":
	inp1 = raw_input("Enter details in the following order - separated by commas:\nIP Address of machine,SSH username,SSH Password\n")
	ip = inp1.split(",")[0]
	username = inp1.split(",")[1]
	password = inp1.split(",")[2]
	addClient(ip, username, password)

elif inp == "2":
	inp2 = raw_input("Enter complete path to your file. Details must be in the following order - separated by commas:\nIP Address of machine,SSH username,SSH Password\nEach line in the file must have these 3 values separated by commas.\n")
	with open(inp2, 'r') as user_file:
		for line in user_file:
			ip = inp2.split(",")[0]
			username = inp2.split(",")[1]
			password = inp2.split(",")[2]
			addClient(ip, username, password)

elif inp == "3":
	inp3 = raw_input("Enter the command to run on your client list:\n")
	runCommand(inp3)

with open('clientList.txt', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in clientList:
        writer.writerow([val])
