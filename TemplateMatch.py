import cv2
import numpy as np

def match(imgIn, imgTm):
	threshold = 0.9
	image = imgIn
	template = cv2.imread(imgTm)
	#cv2.imshow("tm", template)
	#cv2.waitKey(0)

	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

	res = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	#print(min_val, max_val, min_loc, max_loc)

	x1, y1 = max_loc
	x2, y2 = max_loc[0] + template.shape[1], max_loc[1] + template.shape[0]

	#print("pos rectangle",x1, x2, y1, y2)
	
	
	
	
	flag = False
	if np.amax(res) > threshold:
		flag = True
		cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3) # Just draw rectangle when match is true

	#print(flag)
	r = {"x": (x2 - x1)/2 + x1,
		"y": (y2 - y1)/2 + y1,
		"img": image,
		"exist": flag,
		"path": imgTm}

	
	return r
	#cv2.imshow("imagen", image)
	#cv2.imshow("template", template)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()