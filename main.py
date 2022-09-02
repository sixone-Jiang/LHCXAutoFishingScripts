from common.AutoAdb import AutoAdb
from bin.RunApi import RunApi

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

RunApi.run_fish(adb, baits_list)
#RunApi.run_rpg(adb,RPG_map=rpg_map, rpg_time=rpg_map2)