# 记录位置信息的类
import math
import time


class Location:
    auto_adb = None
    temp_rel_path = None
    pos_x = None
    pos_y = None
    remark = None
    # 默认等待时间
    wait_time = 0.5

    def __init__(self, auto_adb, temp_rel_path, pos_x, pos_y, remark=None):
        self.auto_adb = auto_adb
        self.temp_rel_path = temp_rel_path
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.remark = remark

    def is_valuable(self):
        return self.pos_x is not None and self.pos_y is not None

    def click(self, wait_time=wait_time):
        if self.pos_x is None:
            return False

        self.auto_adb.run('shell input tap %s %s' % (self.pos_x, self.pos_y))
        #print('click [%d:%d] %s' % (self.pos_x, self.pos_y, self.temp_rel_path))
        #time.sleep(wait_time)
        return True

    # 调整打印日志
    def __str__(self):
        attrs = ", ".join("{}={}".format(k, getattr(self, k)) for k in self.__dict__.keys())
        return "[{}: {}]".format(self.__class__.__name__, attrs)

    # 从众多location中拿到最近的那个
    def get_nearest(self, loc_list):
        nearest_len = None
        nearest_loc = None
        for loc in loc_list:
            length = math.sqrt((self.pos_x - loc.pos_x) ** 2 + (self.pos_y - loc.pos_y) ** 2)
            if nearest_len is None or nearest_len > length:
                nearest_len = length
                nearest_loc = loc
        return nearest_loc
