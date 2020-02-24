from auto_0_2 import *

print("截取主菜单判断区域")
time.sleep(0.5)
img = getImage(MAIN_MENU_IMAGE_BOX)
img.show()
img.save("initial_IMG/main_menu.png")

