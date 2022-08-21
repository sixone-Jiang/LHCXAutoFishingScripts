import time
import win32gui, win32ui, win32con, win32api
import cv2
import pyautogui

class StartFish:
    base_rate = 1.0
    # 自行测量屏幕中钓鱼显示框左边界和上边界位置
    mumu_left = 950
    mumu_top = 605
    # 自行找一个屏幕中方便点击的初始点（要位于模拟器内）
    click_x_origin = 1000
    click_y_origin = 1000

    def window_capture(filename, mumu_left=mumu_left, mumu_top=mumu_top):
        img = pyautogui.screenshot(region=[mumu_left,mumu_top, 650, 3]) # x,y,w,h
        img.save(filename)
        # 一下代码存在未处理异常（一般在执行10-40次时出现，但算法效率为0.02秒）， 暂时替换 
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

    def Stage(region, fish, ring_flag, duration_rate=base_rate, click_x_origin=click_x_origin, click_y_origin=click_y_origin):
        
        currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
        pyautogui.moveTo(click_x_origin, click_y_origin, duration=0.015)
        #print(currentMouseX, currentMouseY)
        # 长点屏幕
        # 可以新增增量算法进行优化
        if region < fish -400:
            pyautogui.dragTo(100+click_x_origin, click_x_origin, duration=duration_rate*1.2)
            print('向右运动')
            return time.time()
        elif region < fish -300:
            pyautogui.dragTo(100+click_x_origin, click_x_origin, duration=duration_rate*1.05)
            print('向右运动')
            return time.time()
        elif region < fish -200:
            pyautogui.dragTo(100+click_x_origin, click_x_origin, duration=duration_rate*0.85)
            print('向右运动')
            return time.time()
        elif region < fish -150:
            pyautogui.dragTo(100+click_x_origin, click_x_origin, duration=duration_rate*0.75)
            print('向右运动')
            return time.time()
        elif region < fish:
            pyautogui.dragTo(100+click_x_origin, click_x_origin, duration=duration_rate*0.62)
            print('向右运动')
            return time.time()
        else:
            print('向左运动')
            return ring_flag