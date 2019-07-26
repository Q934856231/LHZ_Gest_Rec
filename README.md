************************************************************************************************

接下来使用这些代码的老师学长学姐学弟学妹大家好，
我是兰大信息院2015级电信专业本科生刘洪志，这些代码是我的毕业设计，
在您使用时，请务必先阅读此文档~
部分代码来源于GitHub和CSDN，由于时间比较长忘记复制出处，
如果侵权请与我联系增加上来源出处。
我的联系方式是724776196@qq.com，或QQ724776196，需要帮助请与我联系
后续如果我对代码进行修改，我会放在我的GitHub上，
地址为https://github.com/Kimlau0811/LHZ_Gest_Rec

2019.05.15

************************************************************************************************

###极其重要###

整个项目使用Python3.6.8，TensorFlow1.2.1进行开发

使用该项目代码之前请先在Leap官网下载安装Leap Motion驱动

如果使用使用的是Python3进行开发，请务必复制Leap_Sample文件夹里的Leap.dll，Leap.lib，Leap.py，LeapPython.pyd四个文件（缺一不可）到项目目录下，这是我根据Leap官方的开发包使用SWIG重新封装的Python3版本，原有开发包只能支持Python2，但是Python2马上要停止支持了，so...总之用这个就行了

注意！！！最好使用python3.6或以下的python3环境，否则可能报错。如果安装的是python3.8及以上，请阅读###环境配置###相关内容，使用Anaconda进行多环境配置

如果是要进行手势识别项目开发，请打开code文件夹，并阅读###如何使用###其中内容


************************************************************************************************

###环境配置：写给刚刚接触开发的同学###

1.到官网安装任意版本的Anaconda（带Python3的任意版本）
写入环境变量（写PATH，百度就知道）
试一下在cmd命令提示符里输入conda -V看看会不会报错，如果输出版本就OK
打开AnacondaNavigator中的environment 新建一个python3.6环境，名字定为python36（或者你喜欢），主要是现在TensorFlow不支持Python3.8
新建好之后，在cmd（要重启）中输入activate python36（或者你起的名字），就能进入python3.6对应环境

2.下载CPU版tensorflow （TF1.2.1，Python36版）其他可在镜像链接中查找
激活环境后（activate python36）输入
pip install –i https://mirrors.tuna.tsinghua.edu.cn/tensorflow/windows/cpu/tensorflow-1.2.1-cp36-cp36m-win_amd64.whl
或 pip install –i https://pypi.tuna.tsinghua.edu.cn/simple tensorflow==1.2.1
然后缺啥pip啥就行
用展示程序还需要pip install opencv-python，用的时候也可以把opencv部分代码删掉

3.使用的时候，先激活环境，cd到目录中
输入python 文件名.py就可以运行了

************************************************************************************************

###如何使用###

*打开代码里面都有注释
通用运行方法：
在cmd中cd到目录下，激活python36环境（如果本来就安装了python3.6就不用），输入python 文件名.py

1.【采集数据集】运行GetData_Divided_Relative.py，实时采集数据集

2.【制作数据集】data文件夹里有个Add_Data.py，运行可以把该文件夹下所有数据合并为一个data.csv文件

3.【单独制作测试集的tfrecord文件】python record.py 文件名.csv，该代码会覆盖原有的val.tfrecord文件

4.【制作训练集和测试集的tfrecord文件】把data.csv放在目录下，运行record_train.py

5.【训练，评估，使用】运行training_and_val.py。
训练需要事先制作好tfrecord文件，模型保存在log文件夹下
评估是直接给出模型对val.tfrecord的准确率
使用是输入特征点，返回识别结果。可以复制走内嵌在其他程序里

6.【实时识别】运行Func_Show.py
这个是做毕设展示用的，直接运行是个锤子剪刀布
后面加个数字是精准识别模式，会有一定延迟，原理是返回这几帧内出现最多的手势
按回车退出
如 python Func_Show.py 是锤子剪刀布
python Func_Show.py 0 是实时识别
python Func_Show.py 5 是5帧为单位的精准识别

*************************************************************************************************






