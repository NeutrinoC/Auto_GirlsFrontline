from auto4_6 import *


time.sleep(0.5)
#img = getImage([0.45,0.60,0.65,0.66])
#img.show()
#img.save("initial_IMG/enemy.png")
initImage = cv2.imread("initial_IMG/enemy.png")
capImage  = getImage(ENEMY_IMAGE_BOX)
capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
gray_img1 = cv2.cvtColor(initImage, cv2.COLOR_BGR2GRAY)
gray_img2 = cv2.cvtColor(capImage, cv2.COLOR_BGR2GRAY)
(score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
print(score)


