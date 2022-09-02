import imp
from common import PathUtils, ConfigUtils
from common.Location import Location
from bin.StartFish import StartFish
from bin.StartRPG import StartRPG
import time


class RunApi:
    # 钓鱼
    def run_fish(adb, baits_list=[]):
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
            print('第{%d}轮钓鱼开始'%i)
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
                    if StartFish.is_new_fish(work_dir+'/temp_images/new_fish/', work_dir):
                        new_fish_stop -= 1
                        print("已经捕捉到新鱼")
                    else :
                        #print("捕捉到的不是新鱼")
                        pass
                    if new_fish_stop == 0:
                        return None
                # 若超时计时器超时，则立即进入下一轮钓鱼
                if time.time() - ring_flag >9:
                    break
            print('—————————本轮结束————————')
            
            ending_loc = Location(adb, None, 600, 600)
            ending_loc.click()
            ending_loc.click()
            ending_loc.click()
    
    # RPG
    def run_rpg(adb, RPG_map, rpg_time, times=1000):
        work_dir = PathUtils.get_work_dir()
        first_fight_flag = True
        RPG = StartRPG()
        for i in range(times):
            time.sleep(0.01)
            print('当前是第{%d}轮次'%i)
            # 刷怪
            RPG.get_new(work_dir, 0.8)
            index = 0
            open_time = time.time()
            if i == 0 and index != -1:
                for turn_index in RPG_map:
                    
                    print(turn_index)
                    pre_gray = RPG.get_pre_gray()
                    pre_gray_1 = RPG.get_pre_gray1()
                    RPG.save_pre(work_dir+'/temp_images/state/state'+str(index),pre_gray_1)
                    #time.sleep(1)
                    RPG.turn_to(turn_index)
                    if first_fight_flag:
                        time.sleep(2)
                    # 检验是否是首次战斗
                    if first_fight_flag and adb.check(work_dir+'/temp_images/battle/fast_fight.PNG',0.8):
                        RPG.first_fight(work_dir)
                    first_fight_flag = False
                    start = time.time()
                    
                    while not RPG.check_is_move(pre_gray):
                        while time.time() - start > 3:
                            RPG.turn_to(turn_index)
                            if RPG.check_is_move(pre_gray):
                                time.sleep(0.6)
                                break
                        time.sleep(0.1)
                    
                    #time.sleep(rpg_time[index])
                    index += 1
  
            else:
                
                while index < 16:
                    while adb.check(work_dir+'/temp_images/state/state'+str(index)+'.PNG', 0.82):
                        #if index <= 12:
                        RPG.turn_to(RPG_map[index], wait=0.1)
                        #else :
                          #  RPG.turn_to(RPG_map[index], wait=0.8)
                    index += 1
                
                
            print('本轮共用{%f}'%(time.time()-open_time))

            
            
                
        
            
            

            

