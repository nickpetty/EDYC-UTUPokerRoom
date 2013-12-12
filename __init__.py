from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from directv import DirecTV
import configparser
config = configparser.ConfigParser()
from PIL import ImageTk
from mondo import Mondo
import os
import time
import threading

master = Tk()
master.geometry("1600x480")
master.configure(background='black')
master.overrideredirect(1)
master.bind('<Escape>', quit)

#Logos
horseshoe_logo = PhotoImage(file="logos/logo.gif")
logo = Label(master, image=horseshoe_logo, bg="black")
logo.place(x=20, y=2)

edyc_logo = ImageTk.PhotoImage(file='logos/edyc.png')
elogo = Label(master, image=edyc_logo, bg='black')
elogo.place(x=1100, y=400)

tvcontrol = ImageTk.PhotoImage(file='logos/tvcontrollogo.png')
tvcontrolLogo = Label(master, image=tvcontrol, bg='black')
tvcontrolLogo.place(x=300, y=2)

directvImg = ImageTk.PhotoImage(file='logos/directv.png')
directvLogo = Label(master, image=directvImg, bg='black')
directvLogo.place(x=880, y=2)

#Button Images
genButtonImg = ImageTk.PhotoImage(file='buttons/blackButton.png')
clearButtonImg = ImageTk.PhotoImage(file='buttons/yellowButtonClear.png')
goButtonImg = ImageTk.PhotoImage(file='buttons/orangeButtonGo.png')
clockButtonImg = ImageTk.PhotoImage(file='buttons/blackButtonClock.png')
waitlistButtonImg = ImageTk.PhotoImage(file='buttons/blackButtonWaitList.png')
slideshowButtonImg = ImageTk.PhotoImage(file='buttons/blackButtonSlideShow.png')
dtvButtonImg = ImageTk.PhotoImage(file='buttons/blackButtonDTV.png')
blueButtonImg = ImageTk.PhotoImage(file='buttons/blueButton.png')
redButtonImg = ImageTk.PhotoImage(file='buttons/redButton.png')

#Functions and Callbacks
outputPressed=[]
config.read("config.ini")
selectedBoxIP = StringVar()
selectedBoxIP.set("0")
outputAddr = StringVar()
outputAddr.set("000")

if open('log.txt') == False:
	f = open('log.txt', 'w')
	f.close()

def addToLog(n):
	log = open('log.txt', 'a')
	log.write(time.ctime() + ": " + n + '\n')
	log.close()

def mondoControl(cmd):
	if outputAddr.get() == "000":
		messagebox.showinfo("INFO", "You must select a TV (output) first!")
	else:
		try:
			Mondo.route(cmd)
			addToLog("Set route to " + cmd)
		except IOError:
			messagebox.showinfo("Error", "Could not connect to Mondo.  Please contact the Audio Visual department: Ext. 33341")

def outputSelected(event, name):
	z = 0
	for each in outputButton:
		originalImg = outputButtonImgs[z]
		each.configure(image=originalImg)
		z+=1

	if event in outputPressed:
		number = int(name) - 1
		originalImg = outputButtonImgs[number]
		event.configure(image=originalImg)
		selectedBoxIP.set("0")
		outputAddr.set("000")
		outputPressed[:] = []
	
	selectedBoxIP.set(config.get("ip", name))
	outputAddr.set(name)
	event.configure(image=blueButtonImg)
	outputPressed.append(event)
	mondoControl("B016"+name) #Route selected DTV box (output button) to preview screen on port 16

def inputSelected(event, name):
	mondoControl("B" + outputAddr.get() + name)

def dtvSelected():
	mondoControl("B" + outputAddr.get() + outputAddr.get())

def dtvControl(ip, cmd):
	if ip == "0":
		messagebox.showinfo("INFO:", "You must select a TV (output) first!")
	else:
		try:
			DirecTV.keyInput(ip, cmd)
			print(ip, cmd)
		except:
			messagebox.showinfo("Error", "Could not connect to DirecTV box.  Please contact the Audio Visual department: Ext. 33341")
			addToLog("Error connecting to " + ip + " with command " + cmd)
		waiting.destroy()

#Generate Output Buttons

outputButtons=['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015']
outputButton = []
outputButtonImgs = []
commands = []
x=140
y=70
num = 0
n = 1
trackRow = 1
for button in outputButtons:
	name = "buttonImg" + str(n)
	outputButtonImgs.append(name)
	button = Button(master, width=90, height=90)
	button.place(x=x, y=y)
	imgLoc = "buttons/blackButton" + str(num+1) +".png"
	outputButtonImgs[num] = ImageTk.PhotoImage(file=imgLoc)
	button.configure(image=outputButtonImgs[num], bg='black', bd=0)
	outputButton.append(button)

	#Layout all buttons
	x+=100
	if trackRow == 5:
		x= 140
		y=170
	if trackRow == 10:
		x= 140
		y=270
	num+=1
	n += 1
	trackRow+=1

outputButton[0].configure(command=lambda: outputSelected(outputButton[0], "001"))
outputButton[1].configure(command=lambda: outputSelected(outputButton[1], "002"))
outputButton[2].configure(command=lambda: outputSelected(outputButton[2], "003"))
outputButton[3].configure(command=lambda: outputSelected(outputButton[3], "004"))
outputButton[4].configure(command=lambda: outputSelected(outputButton[4], "005"))
outputButton[5].configure(command=lambda: outputSelected(outputButton[5], "006"))
outputButton[6].configure(command=lambda: outputSelected(outputButton[6], "007"))
outputButton[7].configure(command=lambda: outputSelected(outputButton[7], "008"))
outputButton[8].configure(command=lambda: outputSelected(outputButton[8], "009"))
outputButton[9].configure(command=lambda: outputSelected(outputButton[9], "010"))
outputButton[10].configure(command=lambda: outputSelected(outputButton[10], "011"))
outputButton[11].configure(command=lambda: outputSelected(outputButton[11], "012"))
outputButton[12].configure(command=lambda: outputSelected(outputButton[12], "013"))
outputButton[13].configure(command=lambda: outputSelected(outputButton[13], "014"))
outputButton[14].configure(command=lambda: outputSelected(outputButton[14], "015"))

#Input Buttons
clockButton = Button(master, image=clockButtonImg, width=90, height=90, bd=0, bg='black', command=lambda: inputSelected(clockButton, "016"))
clockButton.place(x=190, y=370)
waitlistButton = Button(master, image=waitlistButtonImg, width=90, height=90, bd=0, bg='black', command=lambda: inputSelected(waitlistButton, "017"))
waitlistButton.place(x=290, y=370)
slideshowButton = Button(master, image=slideshowButtonImg, width=90, height=90, bd=0, bg='black', command=lambda: inputSelected(slideshowButton, "018"))
slideshowButton.place(x=390, y=370)
dtvButton = Button(master, image=dtvButtonImg, width=90, height=90, bd=0, bg='black', command=lambda: dtvSelected())
dtvButton.place(x=490, y=370)

#DirecTV Control Buttons
guideImg = ImageTk.PhotoImage(file='buttons/directv/guide.png')
guide = Button(master, text="Guide", image=guideImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "guide"))
guide.place(x=910, y=100)
exitImg = ImageTk.PhotoImage(file='buttons/directv/exit.png')
exit = Button(master, text="Exit", image=exitImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "exit"))
exit.place(x=1090, y=100)
upImg = ImageTk.PhotoImage(file='buttons/directv/up.png')
up = Button(master, text="Up", image=upImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "up"))
up.place(x=1000, y=100)
leftImg = ImageTk.PhotoImage(file='buttons/directv/left.png')
left = Button(master, text="Left", image=leftImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "left"))
left.place(x=910, y=180)
rightImg = ImageTk.PhotoImage(file='buttons/directv/right.png')
right = Button(master, text="Right", image=rightImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "right"))
right.place(x=1090, y=180)
downImg = ImageTk.PhotoImage(file='buttons/directv/down.png')
down = Button(master, text="Down", image=downImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "down"))
down.place(x=1000, y=260)
selectImg = ImageTk.PhotoImage(file='buttons/directv/select.png')
select = Button(master, text="Select", image=selectImg, width=100, height=100, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "select"))
select.place(x=982, y=153)
backImg = ImageTk.PhotoImage(file='buttons/directv/back.png')
back = Button(master, text="Back", image=backImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "back"))
back.place(x=910, y=260)
infoImg = ImageTk.PhotoImage(file='buttons/directv/info.png')
info = Button(master, text="Info", image=infoImg, width=65, height=45, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "info"))
info.place(x=1090, y=260)

ch_upImg = ImageTk.PhotoImage(file='buttons/directv/ch_up.png')
ch_up = Button(master, text="Ch Up", image=ch_upImg, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "chanup"))
ch_up.place(x=1195, y=90)

ch_dnImg = ImageTk.PhotoImage(file='buttons/directv/ch_dn.png')
ch_dn = Button(master, text="Ch Down", image=ch_dnImg, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "chandown"))
ch_dn.place(x=1195, y=180)

prevImg = ImageTk.PhotoImage(file='buttons/directv/prev.png')
prev = Button(master, text="Prev", image=prevImg, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "prev"))
prev.place(x=1195, y=270)

num1Img = ImageTk.PhotoImage(file='Buttons/directv/1.png')
num1 = Button(master, text="1", image=num1Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "1"))
num1.place(x=1295, y=100)
num2Img = ImageTk.PhotoImage(file='Buttons/directv/2.png')
num2 = Button(master, text="2", image=num2Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "2"))
num2.place(x=1370, y=100)
num3Img = ImageTk.PhotoImage(file='Buttons/directv/3.png')
num3 = Button(master, text="3", image=num3Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "3"))
num3.place(x=1445, y=100)
num4Img = ImageTk.PhotoImage(file='Buttons/directv/4.png')
num4 = Button(master, text="4", image=num4Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "4"))
num4.place(x=1295, y=155)
num5Img = ImageTk.PhotoImage(file='Buttons/directv/5.png')
num5 = Button(master, text="5", image=num5Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "5"))
num5.place(x=1370, y=155)
num6Img = ImageTk.PhotoImage(file='Buttons/directv/6.png')
num6 = Button(master, text="6", image=num6Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "6"))
num6.place(x=1445, y=155)
num7Img = ImageTk.PhotoImage(file='Buttons/directv/7.png')
num7 = Button(master, text="7", image=num7Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "7"))
num7.place(x=1295, y=210)
num8Img = ImageTk.PhotoImage(file='Buttons/directv/8.png')
num8 = Button(master, text="8", image=num8Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "8"))
num8.place(x=1370, y=210)
num9Img = ImageTk.PhotoImage(file='Buttons/directv/9.png')
num9 = Button(master, text="9", image=num9Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "9"))
num9.place(x=1445, y=210)
num0Img = ImageTk.PhotoImage(file='Buttons/directv/0.png')
num0 = Button(master, text="0", image=num0Img, bg='black', bd=0, command=lambda: dtvControl(selectedBoxIP.get(), "0"))
num0.place(x=1370, y=265)

master.mainloop()