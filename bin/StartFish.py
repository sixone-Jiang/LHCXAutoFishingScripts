import time
import win32gui
import cv2
import pyautogui
import ctypes
from common import ConfigUtils
import os

# 找mumu窗口 - 该方法在windows7以上电脑会定位不准
def find_window_by_title_outDate(title):
    try:
        hwnd = win32gui.FindWindow(None, title)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return [left, top, right, bottom]
    except Exception as ex:
        print('Error calling win32gui.FindWindow ' + str(ex))
        return None

# 获取真实的窗口 POS
def find_window_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        f(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(9), ctypes.byref(rect), ctypes.sizeof(rect))
        return rect.left, rect.top, rect.right, rect.bottom

def get_location_with_no_sc(temp_rel_path_list, threshold=0.7):
        
        sp_gray = cv2.imread('d:/learn/lhcx/temp_images/screen_fish_2.jpg', cv2.COLOR_BGR2BGRA)

        if temp_rel_path_list:
            temp_abs_path = temp_rel_path_list
            temp_gray = cv2.imread(temp_abs_path, cv2.COLOR_BGR2BGRA)

            res = cv2.matchTemplate(sp_gray, temp_gray, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val < threshold:
                return False

            return True

        return False


class StartFish:
    base_rate = 1.0

    def AuTo_loc(title_name):
        # 使用自动寻框
        if find_window_by_title(title_name):
            mumu_loc = find_window_by_title(title_name)
            mumu_left = mumu_loc[0] + 310
            mumu_top = mumu_loc[1] + 209
            click_x_origin = (mumu_loc[2] + mumu_loc[0])/2
            click_y_origin = (mumu_loc[3] + mumu_loc[1])/2
        else : 
            while not find_window_by_title(title_name):
                mumu_loc = find_window_by_title(title_name)
                mumu_left = mumu_loc[0] + 310
                mumu_top = mumu_loc[1] + 209
                click_x_origin = (mumu_loc[2] + mumu_loc[0])/2
                click_y_origin = (mumu_loc[3] + mumu_loc[1])/2 
        return [mumu_left, mumu_top, click_x_origin, click_y_origin]

    # 选择鱼饵
    def choice_rod_bait(baits_list , image_path, adb):
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

    # 判断新鱼
    def is_new_fish(image_path):
        fish_list = os.listdir(image_path)
        #adb.screen_cap()
        if fish_list:
            for fish in fish_list:
                if get_location_with_no_sc(image_path+fish):
                    return True
            return False
        else :
            return False
    

    # 屏幕抓取
    def window_capture(filename, mumu_left, mumu_top, mumu_width=650, mumu_h=3):
        img = pyautogui.screenshot(region=[mumu_left, mumu_top, mumu_width, mumu_h]) # x,y,w,h
        img.save(filename)
        # 以下代码存在未处理异常（一般在执行10-40次时出现，但算法效率为0.02秒更快）， 暂时替换 
        '''
        hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        #MoniterDev = win32api.EnumDisplayMonitors(None, None)
        #w = MoniterDev[0][2][2]
        #h = MoniterDev[0][2][3]
        # Alice 测量其位置,得知所需取的判别框为650, 3也可按照需求增大或减速，但影响速度
        w, h = 650, 3
        # print w,h　　　#图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        # Alice
        # (950 605)  -> (1600 620)   分辨率 1280x720
        # 点击点初始坐标为1000 1000
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (mumu_left, mumu_top), win32con.SRCCOPY)
        #saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)
        '''

    # 区域长160 鱼长30
    # 区域：140 - 150 连续 8 个中投6个
    # 鱼：> 210 连续 8个中5个
    def get_position(image_path, region=160, fish=30):
        sp_gray = cv2.imread(image_path,cv2.COLOR_BGR2BGRA)
        # Alice 测量其像素长宽，取第一行,该段为理想段，也可根据个人需求增减18：642
        conp = sp_gray[1][18:638+4]
        red_green_index = -1
        white_index = -1
        for index in range(0, len(conp), 8):
            red_green = 0
            white = 0
            for k in range(8):
                comp = conp[index+k]
                if white_index == -1 and comp > 210:
                    white += 1
                if red_green_index == -1 and comp > 139 and comp <150:
                    red_green += 1
            if red_green > 5:
                red_green_index = index
            if white > 4:
                white_index = index
        
        return red_green_index+region/2+10, white_index+fish/2

    def Stage(region, fish, ring_flag, click_x_origin, click_y_origin, duration_rate=base_rate):
        #currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
        pyautogui.moveTo(click_x_origin, click_y_origin, duration=0.001)
        #print(currentMouseX, currentMouseY)
        # 长点屏幕
        # 可以新增增量算法进行优化
        if region < fish:
            pyautogui.mouseDown(x=click_x_origin, y=click_y_origin, button='left')
            return time.time()
        else:
            pyautogui.mouseUp(x=click_x_origin, y=click_y_origin, button='left')
            print('向左运动')
            return ring_flag
        '''
        if region < fish -400:
            pyautogui.dragTo(100+click_x_origin, click_y_origin, duration=duration_rate*1.4)
            print('向右运动')
            return time.time()
        elif region < fish -300:
            
            pyautogui.dragTo(100+click_x_origin, click_y_origin, duration=duration_rate*1.05)
            print('向右运动')
            return time.time()
        elif region < fish -200:
            pyautogui.dragTo(100+click_x_origin, click_y_origin, duration=duration_rate*0.85)
            print('向右运动')
            return time.time()
        elif region < fish -150:
            pyautogui.dragTo(100+click_x_origin, click_y_origin, duration=duration_rate*0.75)
            print('向右运动')
            return time.time()
        elif region < fish:
            pyautogui.dragTo(100+click_x_origin, click_y_origin, duration=duration_rate*0.62)
            print('向右运动')
            return time.time()
        else:
            print('向左运动')
            return ring_flag
        '''
        '''
        if region < fish -400:
            print('向右运动')
            pyautogui.mouseDown(x=click_x_origin, y=click_y_origin, button='left')
            time.sleep(duration_rate*1.22)
            pyautogui.mouseUp(x=click_x_origin, y=click_y_origin, button='left')
            return time.time()
        elif region < fish -300:
            print('向右运动')
            pyautogui.mouseDown(x=click_x_origin, y=click_y_origin, button='left')
            time.sleep(duration_rate*1.1)
            pyautogui.mouseUp(x=click_x_origin, y=click_y_origin, button='left')
            return time.time()
        elif region < fish -200:
            print('向右运动')
            pyautogui.mouseDown(x=click_x_origin, y=click_y_origin, button='left')
            time.sleep(duration_rate*0.85)
            pyautogui.mouseUp(x=click_x_origin, y=click_y_origin, button='left')
            return time.time()
        elif region < fish -100:
            print('向右运动')
            pyautogui.mouseDown(x=click_x_origin, y=click_y_origin, button='left')
            time.sleep(duration_rate*0.75)
            pyautogui.mouseUp(x=click_x_origin, y=click_y_origin, button='left')
            return time.time()
        elif region < fish:
            print('向右运动')
            pyautogui.mouseDown(x=click_x_origin, y=click_y_origin, button='left')
            time.sleep(duration_rate*0.62)
            pyautogui.mouseUp(x=click_x_origin, y=click_y_origin, button='left')
            return time.time()
        else:
            print('向左运动')
            return ring_flag
        '''