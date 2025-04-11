# Alice's LHCX Auto Fishing Scripts

**特别注意**：本项目停止更新，但日常维护会继续，新的,更强力的项目位置，点[这里](https://github.com/sixone-Jiang/LHCXAutoFishingPro)

灵魂潮汐自动钓鱼脚本, 制作不易, 各位大佬下载前请先点个Star

出于需要实时监测的目的，请仔细阅读使用方法！！！

计算机小白见**Easy Fast Use**这一节，请务必详细阅读

**本脚本仅供学习交流使用! 不会在任何途径任何场合收取费用! 请勿用于非法用途! **

**本脚本遵守GPL-3.0协议, 请勿从其他任何非官方(Github)途径下载该脚本! ( ｀д′)**

需要注意:

+ 电脑需要安装python运行环境.
+ 需要配合安卓模拟器(推荐)使用.
+ 这里仅讨论windows平台的使用.
+ 默认读者已经有一定的动手能力.

功能特点:

+ [ √ ] 连续钓鱼
+ [ √ ] 自动选鱼饵（需要在代码中指定，详见main.py）
+ [ √ ] 快速处理紫鱼，金鱼（请使用迟缓鱼竿或幸运鱼竿，别的鱼竿也能钓但不保证能上）
+ [ √ ] 稳定处理彩鱼
+ [ √ ] 自动定位模拟器在主屏幕中位置
+ [ √ ] 可以在出n条新鱼后终止代码
+ [ × ] 自动处理后宅
+ [ √  ] 代码整理
+ [ × ] 自动RPG未完全实现

**更新**:

* **提醒**，现在需要配置的文件仅有config.ini, 请**仔细**阅读该文件中的一切注释
  * 但如果有自选鱼饵的要求，请按照main.py中的注释修改**baits_list** 变量
  * 记住终止条件，快速移动鼠标到屏幕左上角
* **测试性功能**：
  * 如果您是计算机小白，现今代码有极其简单的方案，请翻到“**Easy Fast Use**”这一节
  * 处于一些考虑，作者暂时决定不将该代码封装成为Windows可直接执行的EXE，请使用该代码的小白们具有一定程度的Python知识（能配置Python环境的程度），如果实在不会就向身边的人请假，放心，这不难，也不会花费太多的时间。
* 自动定位模拟器在主屏幕中位置，现在该选项是config.ini中的一个可选项
* 新增在出n条新鱼后终止代码，现在该选项是config.ini中的一个可选项
* 新增 requirements 文档
* 更新了一个已知问题
* 增强了算法效能，但是没有足够量的算法样本
* 修改了代码运行结构，如果当前版本出现异常请使用之前版本
* 新增了miniconda在windows下的安装教程

## 使用方法

原理是通过ADB对手机屏幕截图, 对比模板图片判断当前游戏情况, 然后通过ADB模拟点击/拖拽等操作.

但对于**实时钓鱼**操作，ADB处理延迟至少为0.7s, 这样的延迟会无限空军；因此作者这里引入Pyautogui通过电脑外部点击来实现实时监控

### 环境搭建

#### 安装python

前往 [miniconda](https://docs.conda.io/en/latest/miniconda.html) 下载 python 3.7 安装包并安装.

安装时注意配置运行环境(path).

    如何判断python安装成功?
    
    打开cmd, 执行`python --version`, 如果正确显示python版本号则说明安装成功

#### 安装python依赖

需要用户手动安装cv2,pyautogui 等.

    pip install opencv-python
    pip install pyautogui

#### 关于ADB和设备

本项目已经自带了adb.exe程序. 用户不必再手动下载.

许多安卓模拟器也会自带adb程序, 不过其自带的版本往往比较低, 一些功能残缺. 因此程序默认使用自带的adb程序。

+ 需要用户查找当前模拟器的ADB连接端口。然后修改配置文件 `config.ini` 中 `adb_host_port` 配置
+ 支持多设备在线时指定某设备连接地址进行操作。但务必配置 `adb_host_port`

##### 模拟器使用分享

不同的模拟器在ADB的实现细节上不同，游戏的体验上也不同。下表是近期（2020-03）的一些体验。欢迎体验的小伙伴贡献经验。

| 模拟器 | ADB端口 | 游戏体验 | 备注（CPU等资源占用情况）    |
| ------ | ------- | -------- | ---------------------------- |
| 雷电   | 5555    | 3.5      | 占用未注意，掉帧相对严重     |
| 逍遥   | 21503   | 4.5      | 占用相对较低，偶尔会卡死     |
| MUMU   | 7555    | 4        | 占用和逍遥接近，声称不会卡死 |
| 夜神   | 62001   |          |                              |
| 蓝叠   | 5555    |          |                              |
| 天天   | 5037    |          |                              |

> 注：游戏体验是指运行是否流畅，掉帧是否严重等情况。1~5分，分数越高体验相对越好。打分全凭个人感受。

## EASY FAST USE

* 该方法无需做任何配置，前提是你使用了MuMu模拟器（普通版本），并且已经处于钓鱼界面

1. 下载本代码，并*解压* 到一个不带中文路径的目录，下面是一个例子，具体路径以你自己配置的为准

   ![1662116269586](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/1662116269586.png)
   
2. 安装miniconda在你的电脑上：

   前往 [miniconda](https://docs.conda.io/en/latest/miniconda.html) ，选择下面的安装包，这有一篇教学请点击此并仔细阅读([点这里](https://www.quanxiaoha.com/conda/install-miniconde.html))

   ![image-20220822213925039](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/image-20220822213925039.png)
   
3. 安装好后，您在任意命令行中输入conda init,命令行会输出一些正确反馈

4. 使用管理员权限（自行百度）打开命令行（按一次win键，搜索输入“命令提示符”,并点击，以管理员身份运行，并点击”是“）

   ![image-20220902185951544](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/image-20220902185951544.png)
   
5. 切换到本代码的工作目录(百度搜素如何在命令行切换工作目录（也就是你能找main.py文件的路径位置，以之前位置为例应当在命令中输入如下）)：

   ![image-20220902190105352](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/image-20220902190105352.png)

6. 之后配置环境，输入命令如下（一行一行的输入）：

```shell
conda create -n lhcx python=3.7 -y
conda activate lhcx
pip install -r requirements.txt
```

4. 打开灵魂潮汐，并切换到钓鱼界面，执行以下命令：

   ```
   python main.py
   ```
5. 记住终止条件，快速移动鼠标到屏幕左上角，且模拟器不可以被遮挡

## 配置文件

第一次下载本项目时，项目根目录有一个 `config_temp.ini` 配置文件。

这个文件介绍了该项目可进行的配置项，但项目的运行**不会**使用此配置文件！

用户需要将该配置文件拷贝一份并重命名为 `config.ini`，然后自行修改配置。**只有 `config.ini` 文件的配置才会生效。**

请仔细阅读配置项说明。

**（如果您不想深度参与代码构建，则必须设置模拟器分辨率为1280*720，且模拟器初始位置处于默认位置，切勿移动）请自行测量模拟器启动后钓鱼框左上角的位置，确保截取的位置包括鱼的中线在内（如果您不明白，什么是中线，下面有一个截取样例）**

**样例**：

图像很细，仅仅是一个600+ * 3 的图像

![haha-green](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/haha-green.jpg)

**您应当将所测量的参数用于 /bin/StartFish.py类的初始化参数中:**

现今代码见修改位置迁移到了config.ini

需要填入的参数包括：

* 自行测量屏幕中钓鱼显示框左边界和上边界位置

  mumu_left = 950（需要自行寻找）

  mumu_top = 605（需要自行寻找）
* 自行找一个屏幕中方便点击的初始点（要位于模拟器内）

  click_x_origin = 1000（需要自行寻找）

  click_y_origin = 1000（需要自行寻找）

此外，**如果您有个性化需求，请仔细阅读main.py中的代码注释**

## 运行代码

* 请务必使用带有**管理员权限**的命令行运行代码，在主目录下(工作目录请不要带**中文路径**)，运行

  ```shell
  conda activate you-env
  python main.py
  ```
* 效果展示：

  见[bilibili](https://www.bilibili.com/video/BV1Qg41167C2/?vd_source=fd58b54cc00f8fdcc9c5eb4422b3eefd),如果失效请搜索个人主页：**ET丨Alice**
* 钓鱼妙法：**建议图鉴哥必看**

  见[Bwiki](https://wiki.biligame.com/lhcx/%E5%AE%B6%E5%9B%AD%E9%92%93%E9%B1%BC%E6%95%B0%E6%8D%AE%E4%B8%80%E8%A7%88)
* 附上我的钓鱼图鉴

  ![image-20220821131023412](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/image-20220821131023412.png)

## 代码逻辑

* 时间关系，如果您对代码逻辑感兴趣或有更好的看法，整理好您的意见，请发送到这里:[邮箱](skblu_alice@foxmail.com)

## 已知问题

* 当前使用win32ui API （用于屏幕截图）在代码运行10分钟左右概率抛出异常，该异常不属于BUG，使用try捕获后直接抛出执行下一轮可解决，现代码提供了另一种实时方案
* 使用win32gui 定位异常，目前已经解决
* 请保证您的窗口如下所示（不要拖动，拉扯导致窗口大小变化）

  ![image-20220822220250582](https://raw.githubusercontent.com/sixone-Jiang/Picgo/main/img/image-20220822220250582.png)
