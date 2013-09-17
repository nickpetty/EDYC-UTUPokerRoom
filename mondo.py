import serial
import time
import configparser
config = configparser.ConfigParser()

class Mondo:
	def comPort():
		config.read("config.ini")
		port = config.get("config", "port")
		port = int(port) - 1
		return int(port)

	def find_port():
		ser = serial.Serial(Mondo.comPort)  # open first serial port
		print(ser.portstr)       # check which port was really used   \
		ser.close()
	
	def get_config():
		config.read("config.ini")
		ser = serial.Serial(Mondo.comPort)
		ser.write(bytes("D" + '\r\n', encoding='ascii'))
		time.sleep(1)
		while ser.inWaiting() != 0:
			r = ser.readline()
			r = r.decode('UTF-8').replace('\r\n', '')
			r = r.split()
			if len(r) > 1:
				config.set("map", r[0], r[1].replace('V', ''))
			else:
				break
			time.sleep(0.01)

		f = open("config.ini", "w")
		config.write(f)
		ser.close()
		
	def set(o, i):
		ser = serial.Serial(Mondo.comPort)
		cmd = 'B' + o + i
		ser.write(bytes(cmd + '\r\n', encoding='ascii'))
		r = ser.readline()
		r = r.decode('UTF-8').replace('\n', '')
		if r == 'OK>':
			print("Done.")
		else:
			print(r)
		ser.close()

	def out_off(n):
		ser = serial.Serial(Mondo.comPort())
		cmd = 'B' + n + "000"
		ser.write(bytes(cmd + '\r\n', encoding='ascii'))
		r = ser.readline()
		r = r.decode('UTF-8').replace('\n', '')
		if r == 'OK>':
			print("Done.")
		else:
			print(r)
		ser.close()

	def test():
		line = []
		ser = serial.Serial(3)
		ser.write(bytes("D" + '\r\n', encoding='ascii'))
		time.sleep(1)
		while True:
			for c in ser.readline():
				line.append(c)
				if c == '\n':
					print("Line: " + line)
					line = []
					break
		ser.close()

	def route(cmd):
		ser = serial.Serial(Mondo.comPort())
		ser.write(bytes(cmd + '\r', encoding='ascii'))
		r = ser.readline()
		r = r.decode('UTF-8').replace('\n', '')
		return(r)

