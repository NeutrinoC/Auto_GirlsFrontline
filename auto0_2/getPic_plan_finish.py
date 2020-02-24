from auto_0_2 import *

print("截取计划完成判断区域")
time.sleep(0.5)
img = getImage(PLAN_FINISH_IMAGE_BOX)
img.show()
img.save("initial_IMG/plan_finish.png")

