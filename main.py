from common.AutoAdb import AutoAdb
import time

from common import PathUtils
from common.Location import Location
from bin.StartFish import StartFish

AutoAdb(test_device=True)
adb = AutoAdb()
work_dir = PathUtils.get_work_dir()
times = 60
baits_list = [9,8]
# 对照表：
#       蚯蚓    骨渣    青虫    白虫    红虫    蟋蟀    肉团    虫蛹    碎肉    虾米
#        1      2       3       4       5       6       7       8       9      10
# 掉落范围：
# 绿色 1-5 蓝色 51-53 紫色 81-83 橙色 111-113, 按顺序递推
# 具体概率见wiki.biligame/lhcx

# 选择鱼饵
def choice_rod_bait(baits_list , image_path, adb=adb):
    if baits_list:
        for bait in baits_list:
            if adb.check(image_path+str(2*bait-1)+'.png'):
                adb.click(image_path+str(2*bait-1)+'.png')
                time.sleep(1)
                break
            elif adb.check(image_path+str(2*bait)+'.png'):
                adb.click(image_path+str(2*bait)+'.png')
                time.sleep(1)
                break
        return True
    else :
        return False

# 开始程序
def run(baits_list=baits_list, times=times, work_dir=work_dir):
    for i in range(times):
        adb.click(work_dir + '/temp_images/fish.png')
        time.sleep(3)
        choice_rod_bait(baits_list,work_dir + '/temp_images/baits/')
        adb.click(work_dir +'/temp_images/start2.png')
        # 等待钓鱼开始 5-10s
        time.sleep(5)
        now = time.time()
        ring_flag = now 
        while time.time() - now <60*5:
            StartFish.window_capture(filename=work_dir+'/temp_images/screen_fish.jpg')
            x, y = StartFish.get_position(image_path=work_dir+'/temp_images/screen_fish.jpg')
            ring_flag = StartFish.Stage(x, y, ring_flag)
            # 若超时计时器超时，则立即进入下一轮钓鱼
            if time.time() - ring_flag >9:
                break

        ending_loc = Location(adb, None, 600, 600)
        ending_loc.click()
        ending_loc.click()
        ending_loc.click()

run()