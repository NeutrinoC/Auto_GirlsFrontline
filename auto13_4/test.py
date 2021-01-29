from auto13_4 import *

time.sleep(0.5)
img = getImage(MAIN_MENU_IMAGE_BOX)
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
#cv2.imwrite("initial_IMG/main_menu.png", img)



