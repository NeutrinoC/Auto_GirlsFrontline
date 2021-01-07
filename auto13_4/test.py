from auto13_4 import *

time.sleep(0.5)
img = getImage(RETURN_COMBAT_IMAGE_BOX)
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
#cv2.imwrite("initial_IMG/return_combat.png", img)



