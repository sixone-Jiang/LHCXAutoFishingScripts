import subprocess

from common import ConfigUtils


def test_device():
    from common.AutoAdb import AutoAdb
    auto_adb = AutoAdb()

    print('ADB PATH >>>> ' + auto_adb.adb_path)
    try:
        subprocess.Popen([auto_adb.adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        print('ADB 路径错误')
        exit(1)

    check_link(auto_adb)
    check_size(auto_adb)
    check_other(auto_adb)
    print()


def check_link(auto_adb):
    adb_host_port = ConfigUtils.get('adb_host_port')
    print('检测设备连接状态 >>> %s ...' % adb_host_port)

    auto_adb.run('connect %s' % adb_host_port)
    device_list = get_devices(auto_adb)
    if len(device_list) == 0:
        print('未检测到设备，请检查ADB地址配置')
        exit(1)

    target_device = None
    print('\n设备列表：')
    for device in device_list:
        print(device)
        if adb_host_port in device:
            target_device = device

    print()
    # 设备没找到
    if target_device is None:
        print('设备列表中没找到目标连接（%s），请检查配置是否正确' % adb_host_port)
        exit(1)
    # 如果找到了设备，但是离线状态
    if 'offline' in target_device:
        print('检测到设备离线！！！')
        print('由于不同模拟器ADB实现细节不同，请尝试以下办法（没有先后顺序）：')
        print('· 重启模拟器')
        print('· 如果模拟器已经自带了ADB，则可以尝试将脚本中adb文件夹的文件拷贝至模拟器自带ADB目录。注意备份原文件')
        print('· 在adb目录下打开cmd，执行 adb kill-server 后再执行 adb start-server，然后执行 adb devices 查看是否解决')
        print('· 重启电脑')
        print('· 换个模拟器')
        exit(1)
    # 设备正常
    print('设备已连接', end='\n\n')


# 获取设备列表
def get_devices(auto_adb):
    lines = auto_adb.run('devices').splitlines()
    del (lines[0])  # 删除第一个标题行
    return lines


def check_size(auto_adb):
    output = auto_adb.run('shell wm size')
    print('屏幕分辨率: ' + output)
    if 'Physical size: 1280x720' not in output:
        print('请将分辨率设置为 1280x720 (横向 平板模式)')
        exit(1)


def check_other(auto_adb):
    output = auto_adb.run('shell wm density')
    print("像素密度: " + output)
    output = auto_adb.run('shell getprop ro.product.device')
    print("系统类型: " + output)
    output = auto_adb.run('shell getprop ro.build.version.release')
    print('系统版本: ' + output)


if __name__ == '__main__':
    test_device()
