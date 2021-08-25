from PIL import Image, ImageGrab
import cv2
import numpy as np
import pyautogui as pyt
import sys, time, os
import TemplateMatch as tm
import constants as c

xx, yy, xW, yH = (3, 31, 801, 480)
count = 0
showIt = False
runIt = False
prevStep = ""
haveEnergy = True
msg = ""

doId = 0 #0: misiones; 1: embers
typeId = 0 #0: mision 1; 1: mision 2...
diffucultId = 0

energys = [c.ENERGY_0, c.ENERGY_1, c.ENERGY_2, c.ENERGY_3, c.ENERGY_4, c.ENERGY_5, c.ENERGY_6, c.ENERGY_7, c.ENERGY_8, c.ENERGY_9]
screens = [c.MAIN_SCREEN, c.MISIONS_SCREEN, c.STORY_SCREEN, c.EMBER_SCREEN]

#doList = [c.c.BTN_STORY, c.BTN_EMBERS] # 0: hacer las misiones; 1: hacer las ember
typeMisionList = [c.BTN_MISION_1, c.BTN_MISION_2, c.BTN_MISION_3, c.BTN_MISION_4] 
typeEmberList = [c.BTN_FUEGO, c.BTN_TIERRA, c.BTN_AIRE, c.BTN_TRUENO, c.BTN_PLANTA, c.BTN_AGUA, c.BTN_HIELO]
typeDifficult = [c.BTN_EASY, c.BTN_MEDIUM, c.BTN_HARD]

errors = [c.BTN_RETRY]


#typeIdFalse = 1 if 1 != typeId else 0
toDo = []
#doMision = [screens[0], c.BTN_MISIONES, screens[1], c.c.BTN_STORY, screens[2], typeMisionList[typeId], c.BTN_JUGAR, c.BTN_INICIAR, c.BTN_MANUAL, c.BTN_1X, c.BTN_RECLAMAR, c.BTN_CONTINUAR, c.BTN_SALIR]

#doEmber = [screens[0], c.BTN_MISIONES, screens[1], c.BTN_EMBERS, screens[3], typeEmberList[typeIdFalse], typeEmberList[typeId], c.BTN_JUGAR, c.BTN_INICIAR, c.BTN_MANUAL, c.BTN_1X, c.BTN_RECLAMAR, c.BTN_CONTINUAR, c.BTN_SALIR]







def cls(): #Definimos la función estableciendo el nombre que queramos
	if os.name == "posix":
	   os.system ("clear")
	elif os.name == "ce" or os.name == "nt" or os.name == "dos":
	   os.system ("cls")

def WhereAmI(frame):
	place = ""
	for screen in screens:
		matc = tm.match(frame, screen)
		if matc["exist"]:
			place = screen;
	return place

def WhereDoIGo(frame):
	# = 0

	for i in range(0, len(toDo)):
		#isScreen = False
		#print("la i es {}".format(i))
		matc = tm.match(frame, toDo[i])
		
		if matc["exist"] and matc["path"] != prevStep:
			break

	if matc["exist"] == False:
		for error in errors:
			matcError = tm.match(frame, error)
			if matcError["exist"]:
				matc = matcError
	return matc

def GetEnergy(frame):
	haveEnergy = True

	for energy in energys:
		matc = tm.match(frame, energy)
		if matc["exist"]:
			haveEnergy = False
			break

	return haveEnergy

def GetDoList(idDo):
	if(idDo == 0):
		#misiones
		r = [c.BTN_MISIONES, c.BTN_STORY, typeMisionList[typeId], c.BTN_JUGAR, c.BTN_INICIAR, c.BTN_MANUAL, c.BTN_1X, c.BTN_RECLAMAR, c.BTN_CONTINUAR, c.BTN_SALIR]
	else:
		#embers
		r = [c.BTN_MISIONES, c.BTN_EMBERS, typeEmberList[typeId], c.BTN_JUGAR_EMBER, c.BTN_INICIAR, c.BTN_MANUAL, c.BTN_1X, c.BTN_RECLAMAR, c.BTN_CONTINUAR, c.BTN_SALIR]

	return r

#doList = [doMision, doEmber] # 0: hacer las misiones; 1: hacer las ember

def runBot():
	global toDo, haveEnergy, prevStep, msg
	toDo = GetDoList(doId)

	while True:

		if(runIt == False):
			#print(runIt)
			#cv2.destroyAllWindows()
			break

		frame = np.array(ImageGrab.grab(bbox=[xx,yy,xW,yH]))
		
		match = WhereDoIGo(frame.copy())
		
		if showIt:
			frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			cv2.imshow("Capture", frameRGB)

		if(doId == 1): 
			haveEnergy = GetEnergy(frame.copy())
			if(haveEnergy == False):
				#print("No hay energia")
				msg = "No energy"
				break

		
		if(match["exist"]):
			time.sleep(1)
			prevStep = match["path"]

			#print("se encontró {}".format(match["path"]))

			frameMatch = match["img"]
			frameRGB = cv2.cvtColor(frameMatch, cv2.COLOR_BGR2RGB)
			
			pyt.moveTo(match["x"] + xx, match["y"] + yy)
			pyt.click()

			if(showIt):
				cv2.imshow("Capture", frameRGB)

			#if(toDo[len(toDo) - 1] == match["path"]):
				#index = 0
				#cv2.waitKey(0)
				#cls()
			
		
		if cv2.waitKey(1) & 0xFF == ord("s"):
			break
	if(showIt):
		cv2.destroyAllWindows()
	#return False


	
