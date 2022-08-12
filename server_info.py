import socket, select, string, sys, time

retry = 1
delay = 1
timeout = 1
	
def isOpen(ip, port, retry, delay, timeout):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(timeout)
	try:
		s.connect((ip, int(port)))
		s.shutdown(socket.SHUT_RDWR)
		return True
	except:
		return False
	finally:
		s.close()

def checkHost(ip, port, retry, delay, timeout):
	ipup = False
	for i in range(retry):
		if isOpen(ip, port,retry, delay, timeout):
			ipup = True
			break
		else:
			time.sleep(delay)
			
	return ipup  

def GetServerIP(hostname): 
	try:         
		host_ip = socket.gethostbyname(hostname) 
		return host_ip
	except: 
		return "Unable to get IP address" 


def doHost(servername, hostname, dcsport):
	serverIP = GetServerIP(hostname)
	dcsStatus = "DOWN"
	srsStatus = "DOWN"
	LotATCStatus = "DOWN"	
    
	if checkHost(hostname, dcsport, retry, delay, timeout):
		dcsStatus = "UP"
		
	if checkHost(hostname, 5002, retry, delay, timeout):
		srsStatus = "UP"
		
	if checkHost(hostname, 10310, retry, delay, timeout):
		LotATCStatus = "UP"
		
	print(servername + ", hostname: " + hostname + ", ip: " + serverIP + ", DCS (" + str(dcsport) + "): " + dcsStatus + ", SRS: " + srsStatus + ", LotATC: " + LotATCStatus)
	
if __name__ == "__main__":
    doHost('JOW Able', 'able.aggressors.ca', 10318)
    doHost('JOW Easy','easy.aggressors.ca', 10308)
    doHost('JOW Whiskey','whiskey.aggressors.ca', 10308)

	
