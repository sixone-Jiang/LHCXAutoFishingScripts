import re
from common.AutoAdb import AutoAdb
import time

from common import PathUtils, ConfigUtils
from common.Location import Location
from bin.StartFish import StartFish

AutoAdb(test_device=True)
adb = AutoAdb()
# 鱼饵选择
# 例如填入 baits_list = [1, 2]将自动钓蚯蚓，蚯蚓掉完后钓骨渣，不填入默认第一个
baits_list = [7]
# 对照表：
#       蚯蚓    骨渣    青虫    白虫    红虫    蟋蟀    肉团    虫蛹    碎肉    虾米
#        1      2       3       4       5       6       7       8       9      10
# 掉落范围：
# 绿色 1-5 蓝色 51-53 紫色 81-83 橙色 111-113, 按顺序递推
# 具体概率见wiki.biligame/lhcx

# 开始程序
def run(baits_list=baits_list):
    work_dir = PathUtils.get_work_dir()
    times = int(ConfigUtils.get('end_times'))
    new_fish_stop = int(ConfigUtils.get('new_fish_stop'))
    title_name = ConfigUtils.get('title_name')
    auto_loc = int(ConfigUtils.get('auto_loc'))
    # 自行测量屏幕中钓鱼显示框左边界和上边界位置950-605
    mumu_left = ConfigUtils.get('mumu_left')
    mumu_top = ConfigUtils.get('mumu_top')
    # 自行找一个屏幕中方便点击的初始点（要位于模拟器内）
    click_x_origin = ConfigUtils.get('x_origin')
    click_y_origin = ConfigUtils.get('y_origin')

    # Auto_loc
    if auto_loc == 1:
        mumu_loc =StartFish.AuTo_loc(title_name)
        mumu_left, mumu_top, click_x_origin, click_y_origin = mumu_loc[0], mumu_loc[1],mumu_loc[2], mumu_loc[3]
        print(mumu_loc)
    for i in range(times):
        adb.click(work_dir + '/temp_images/fish.png')
        time.sleep(3)
        StartFish.choice_rod_bait(baits_list,work_dir + '/temp_images/baits/', adb=adb)
        adb.click(work_dir +'/temp_images/start2.png')
        # 等待钓鱼开始 5-10s
        time.sleep(5)
        now = time.time()
        ring_flag = now 
        while time.time() - now <60*5:
            StartFish.window_capture(filename=work_dir+'/temp_images/screen_fish.jpg',mumu_left=mumu_left,mumu_top=mumu_top)
            x, y = StartFish.get_position(image_path=work_dir+'/temp_images/screen_fish.jpg')
            ring_flag = StartFish.Stage(x, y, ring_flag, click_x_origin, click_y_origin)
            # 判断是否为新鱼
            if new_fish_stop > 0:
                # 该参数如果异常请自行测定
                StartFish.window_capture(filename=work_dir+'/temp_images/screen_fish_2.jpg',mumu_left=mumu_left+500-320,mumu_top=mumu_top+593-204-30, mumu_width=160+40+120, mumu_h=40+60)
                if StartFish.is_new_fish(work_dir+'/temp_images/new_fish/'):
                    new_fish_stop -= 1
                    print("已经捕捉到新鱼")
                else :print("捕捉到的不是新鱼")
                if new_fish_stop == 0:
                    return None
            # 若超时计时器超时，则立即进入下一轮钓鱼
            if time.time() - ring_flag >9:
                break
        
        
        ending_loc = Location(adb, None, 600, 600)
        ending_loc.click()
        ending_loc.click()
        ending_loc.click()

run()