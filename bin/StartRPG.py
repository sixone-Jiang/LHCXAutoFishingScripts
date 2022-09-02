import imp
from tabnanny import check
import time
import ctypes
from common.AutoAdb import AutoAdb
import os
from common.Location import Location
import cv2
class StartRPG:
    base_rate = 1.0
    # 一次自动战斗后等待
    # 定位当前位置，使用adb
    # 定位4个角位置，使用adb，并计算获取最小判定框
    # 左上右下
    def __init__(self) -> None:
        self.width, self.height = [120, 80]
        self.first_left_top = [393, 309]
        self.second_left_top = [790, 309]
        self.third_left_top = [393, 500]
        self.forth_left_top = [790, 500]
        self.adb = AutoAdb()

    def click_first(self, wait=1):
        loc = Location(self.adb, None, self.first_left_top[0]+self.width/2, self.first_left_top[1]+self.height/2)
        loc.click()
        time.sleep(wait)

    def click_second(self, wait=1):
        loc = Location(self.adb, None, self.second_left_top[0]+self.width/2, self.second_left_top[1]+self.height/2)
        loc.click()
        time.sleep(wait)
    
    def click_third(self,  wait=1):
        loc = Location(self.adb, None, self.third_left_top[0]+self.width/2, self.third_left_top[1]+self.height/2)
        loc.click()
        time.sleep(wait)
    
    def click_forth(self, wait=1):
        loc = Location(self.adb, None, self.forth_left_top[0]+self.width/2, self.forth_left_top[1]+self.height/2)
        loc.click()
        time.sleep(wait)

    def first_fight(self, work_dir, wait=0.3):
        time.sleep(4)
        loc = Location(self.adb, None, 624, 394)
        loc.click()
        time.sleep(4)
        self.adb.click(work_dir+'/temp_images/battle/fast_fight.PNG')
        time.sleep(3)

    def get_pre_gray(self):
        img = self.adb.get_imread_from_screen()
        #56:170,1091: 1244
        #0:210, 1000:1280-1
        img_crop = img[0:210, 1000:1280-1]
        print(img_crop.shape)
        return img_crop

    def get_pre_gray1(self):
        img = self.adb.get_imread_from_screen()
        #56:170,1091: 1244
        #0:210, 1000:1280-1
        img_crop = img[56:170,1091: 1244]
        print(img_crop.shape)
        return img_crop
    
    def save_pre(self, image_path, pre_image):
        cv2.imwrite(image_path+'.PNG',pre_image)

    def check_is_move(self,pre_gray, wait=0.1):
        if self.adb.compare_pre_with_now(pre_gray):
            #time.sleep(wait)
            return False
        else :
            #time.sleep(wait)
            return True

    def get_new(self,work_dir, wait=1):
        self.adb.click(work_dir+'/temp_images/re_get_monster/1-bag.PNG')
        time.sleep(wait)
        self.adb.click(work_dir+'/temp_images/re_get_monster/2-tent.PNG')
        time.sleep(wait)
        self.adb.click(work_dir+'/temp_images/re_get_monster/3-use.PNG')
        while not self.adb.check(work_dir+'/temp_images/re_get_monster/4-break_all.PNG'):
            time.sleep(0.1)
        time.sleep(wait)
        self.adb.click(work_dir+'/temp_images/re_get_monster/4-break_all.PNG')
        while not self.adb.check(work_dir+'/temp_images/re_get_monster/5-break.PNG'):
            time.sleep(0.1)
        time.sleep(wait)
        self.adb.click(work_dir+'/temp_images/re_get_monster/5-break.PNG')
        while not self.adb.check(work_dir+'/temp_images/re_get_monster/1-bag.PNG'):
            time.sleep(wait)
        
    def turn_to(self, index, wait=1):
        if index == 1:
            self.click_first(wait)
        elif index == 2:
            self.click_second(wait)
        elif index == 3:
            self.click_third(wait)
        elif index == 4:
            self.click_forth(wait)
        else :
            print("Input ERROR index {%s}" % str(index))
            return None
    # self.adb.click 处理刷怪，首次战斗，误入事件
    # 1.构建已知图，通关读入配置文件来完成刷图事件（输入运动轨迹）
    # 2.判定是否可达（用引线判定）
    #   check函数