from tkinter import ttk
from tkinter import *
import cv2
from PIL import Image, ImageGrab
import numpy as np
import threading
import getCord
import Main as bot

class BotDragonary():
	def __init__(self, window):
		self.wind = window
		self.wind.geometry("260x290")
		self.wind.title('Bot Dragonary v1.0.0')

		self.cord = [3, 31, 801, 480]
		self.run = False
		self.wind.resizable(False, True)

		#creating a frame container
		frame = LabelFrame(self.wind, text = "Select what do you want i do for you")
		frame.grid(row = 0, column = 0, columnspan = 3, pady = 10, padx= 20)

		#radio buttom mission/ember
		self.embMis = IntVar()
		R1 = Radiobutton(frame, text="Missions", variable=self.embMis, value=0, command=self.SwitchType)
		R1.grid(row=1, column=0)
		R2 = Radiobutton(frame, text="Embers", variable=self.embMis, value=1, command=self.SwitchType)
		R2.grid(row=1, column=1)

		#this contain a value of id type misions
		self.frameMis = LabelFrame(self.wind, text = "Select Mission")
		self.frameMis.grid(row = 2, column = 0, pady=5, padx=5, rowspan=8)

		self.typeId = IntVar()

		misionText = ["Mision 1", "Mision 2", "Mision 3", "Mision 4"]#, "Mision 5", "Mision 6", "Mision 7", "Mision 8"]

		for i in range(0, len(misionText)):
			Radiobutton(self.frameMis, text=misionText[i], variable=self.typeId, value=i).grid(row=i+3, column=0)

		#this contain a value of id type ember
		self.frameEmb = LabelFrame(self.wind, text = "Select Ember")
		#self.frameEmb.grid(row = 2, column = 0, pady=5)

		embText = ["Fuego", "Tierra", "Aire", "Trueno", "Planta", "Agua", "Hielo"]

		for i in range(0, len(embText)):
			Radiobutton(self.frameEmb, text=embText[i], variable=self.typeId, value=i).grid(row=i+3, column=0, sticky=W)

		#Put a checkbox to show or not record
		self.wantShow = BooleanVar()
		self.checkBtn = Checkbutton(self.wind, text='Show Graph', command=self.ShowGraph, variable=self.wantShow,
			onvalue=True, offvalue=False)
		#self.checkBtn.grid(row=2, column=1, columnspan=3, sticky=N+W)
		
		#set cord
		self.xyText = StringVar()
		self.xyText.set("({}, {})".format(self.cord[0], self.cord[1]))
		#Label(self.wind, text="(x1, y1)").grid(row=3, column=1, sticky=N+W)
		Label(self.wind, textvariable=self.xyText).grid(row=3, column=1, sticky=N)
		
		self.xyText2 = StringVar()
		self.xyText2.set("({}, {})".format(self.cord[2], self.cord[3]))
		Label(self.wind, textvariable=self.xyText2).grid(row=3, column=2, sticky=N)
		

		Button(self.wind, text="Set Cord", command=self.SetCord, width=17).grid(row=5, column=1, columnspan=2, sticky=N+W)

		self.runText = StringVar()
		self.runText.set("Run")

		self.btnRun = Button(self.wind, textvariable=self.runText,
			command=lambda:[threading.Thread(target=self.Run).start(), threading.Thread(target=self.GetMsg).start()], width=17)
		self.btnRun.grid(row=6, column=1, pady=10, columnspan=2, sticky=N+W)
		
		#label to show msg
		self.lbMsg = StringVar()
		self.lbMsg.set("")
		Label(self.wind, textvariable=self.lbMsg, fg="Red", font=("Verdana", 12, "bold")).grid(row=7,
			column=1, columnspan=2)

		#Put my sign
		Label(self.wind, text="Discord: 3n7rada#0702", fg="#3F41AB", font=("Verdana", 8, "bold")).grid(row=8,
			column=1, columnspan=2)

	#switch between ember and mission
	def SwitchType(self):
		if(self.embMis.get() == 0):
			self.frameEmb.grid_remove()
			self.frameMis.grid(row = 2, column = 0, pady=5, padx=5, rowspan=8)
			
			#print()
		else:
			self.frameMis.grid_remove()
			self.frameEmb.grid(row = 2, column = 0, pady=5, padx=5, rowspan=8)


	#muestra graficamente lo que ve el bot
	def ShowGraph(self):
		if self.wantShow.get():
			bot.showIt = self.wantShow.get()

			xx, yy, xW, yH = (self.cord[0], self.cord[1], self.cord[2], self.cord[3])
			frame = np.array(ImageGrab.grab(bbox=[xx,yy,xW,yH]))
			preFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			cv2.imshow("Capture", preFrame)
		else:
			bot.showIt = self.wantShow.get()
			cv2.destroyAllWindows()

	#Set the cordinates of window to read
	def SetCord(self):
		cord = getCord.GetCord()

		for i in range(0,4):
			self.cord[i] = cord[i]
		self.xyText.set("({}, {})".format(self.cord[0], self.cord[1]))
		self.xyText2.set("({}, {})".format(self.cord[2], self.cord[3]))

	def GetMsg(self):
		self.lbMsg.set(bot.msg)

	#Run the bot
	def Run(self):
		
		self.lbMsg.set("")

		#set cordinates to read
		bot.xx, bot.yy, bot.xW, bot.yH = (self.cord[0], self.cord[1], self.cord[2], self.cord[3])

		

		if self.run: # Stop
			self.run = False
			self.runText.set("Run")
			
			if self.wantShow:
				self.checkBtn.deselect()
				self.wantShow.set(False)

				#bot.showIt = self.wantShow.get()
				cv2.destroyAllWindows()
				#self.ShowGraph()

		else: #Run
			self.run = True
			self.runText.set("Stop")
			#bot.runIt = True
			
		
		#set config to do
		bot.doId = self.embMis.get()
		bot.typeId = self.typeId.get()
		
		bot.runIt = self.run

		if self.run:
			bot.runBot()





if __name__ == '__main__':
	window = Tk()
	app = BotDragonary(window)
	window.mainloop()