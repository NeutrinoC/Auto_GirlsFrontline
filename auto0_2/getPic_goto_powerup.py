from auto_0_2 import *

print("截取前往强化界面判断区域")
time.sleep(0.5)
img = getImage(GOTO_POWERUP_IMAGE_BOX)
img.show()
img.save("initial_IMG/goto_powerup.png")

