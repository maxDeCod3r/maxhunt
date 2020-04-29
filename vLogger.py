#!/usr/bin/python3

import serial
import syslog
from datetime import datetime
import time
import csv
import serial.tools.list_ports


while True:

	myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
	port1 = '/dev/ttyUSB0'
	port2 = '/dev/ttyUSB1'
	ports = [port1, port2]
	collecting = False

	for x in myports:
		for port in ports:
			if port in x:
				try:
					print("Trying port " + str(port))
					ser = serial.Serial(port,9600,timeout=5)
					print("Running on port: " + str(port))
					collecting = True
				except:
					print("Failed to open " + str(port))

				while collecting:
					try:
						ser.reset_input_buffer()
						raw_msg = ser.readline()
						msg = raw_msg.rstrip().decode('utf-8')
						with open('test.csv', 'a+', newline='') as csvfile:
							spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
							if msg != "":
								now = datetime.now()
								dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
								spamwriter.writerow([dt_string, msg])
						if msg != "":
							time.sleep(2)
					except:
						print("Error on port " + str(port)+ " ,terminating")
						collecting = False
						time.sleep(2)
								
print("Stopped.")

# caffeine.off()
