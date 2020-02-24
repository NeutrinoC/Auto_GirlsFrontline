from auto_0_2 import *

print("截取0-2地图判断区域")
time.sleep(0.5)
img = getImage(MAP_0_2_IMAGE_BOX)
img.show()
img.save("initial_IMG/map.png")

