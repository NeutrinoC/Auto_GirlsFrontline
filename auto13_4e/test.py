from auto13_4e import *

mouseClick(AIRPORT_2_CLICK_BOX,0,0)
exit(0)

time.sleep(0.5)
img = getImage(COMBAT_START_IMAGE_BOX)
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
#cv2.imwrite("initial_IMG/combat_finish.png", img)



