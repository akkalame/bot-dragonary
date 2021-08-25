from pynput import mouse


countPres = 0
x1, y1, x2, y2 = (3, 31, 801, 480)
def on_click(x, y, button, pressed):
    
    if button == mouse.Button.left and pressed:
    	global countPres, x1, y1, x2, y2
    	countPres += 1
    	#print('{} at {} {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y),pressed))
    	
    	if countPres > 1:
    		x2, y2 = (x, y)
    		countPres = 0
    		return False # Returning False if you need to stop the program when Left clicked.
    	else:
    		x1, y1 = (x, y)

def GetCord():
	listener = mouse.Listener(on_click=on_click)
	listener.start()
	listener.join()

	r = [x1, y1, x2, y2]
	return r


'''while True:
	key = input("quieres guardar esas coordenadas? s/n ")
	if(key == "s"):
		count += 1
		if(count < 2):
			xx, yy = pyt.position()
		else:
			xW, yH = pyt.position()
			break;
print(xx,yy,xW,yH)'''