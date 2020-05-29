# standardSitting
> 基于Openpose的开源的坐姿检测与播报矫正软件

![](4.png)

项目从前期调查开始，采集了大量的数据，通过人工标注的形式定义标准坐姿和错误坐姿，同时标注错误姿势的要点，将错误坐姿定义为三类主要问题：头部不正，身体不直，腰背弯曲。

收集的数据进行归类后开始分析，通过身体部位节点计算，总结出几类问题置信度较高的参数。考虑到设备的问题和计算量，采用单目视觉摄像的方式，可以通过移动端和PC端进行设计，在学习的正前方放置摄像头。

通过openpose采集人体上身节点数据，经过分析后得到判断标准坐姿的参量，通过比较这些参量输出相应的显示，这里我们通过语音提示的方法来提示用户坐姿的错误，当用户姿势标准后停止错误提示。

![](3.png)

## Installation(**Windows Only**)

Windows:

```
download the latest release ver
extract the app folder to anywhere in your disk
```

## Usage

double click the poseestimation.exe in the folder,then the initial period takes up abount ten seconds,when the label ```正在初始化``` turn to ```程序未运行```,you can click the ```开始检测``` botton to start the program.

![](1.png)
![](2.png)

for more information on usage,please go to [standardSitting文档](https://docs.google.com/document/d/1aBZUWWjfnGENfG-lLUxR1-8BpfNQt6iH_GTdcd2GyyI/edit?usp=sharing) and [standardSitting演示文稿](https://docs.google.com/presentation/d/13BfF1TiJzeDX3NLtctPy5Vxs7LAVo-6Reb912g-ofNE/edit?usp=sharing) for more detailed doc.

## Release History

* v1.05
    ### 主界面图标更新
    ### 精简合并文件
  * 抽离源代码文件与其他不必要资源，发布供运行的程序版本
* v1.0
    ### 实现基本功能
    * 检测坐姿是否标准
    * 当检测到持续不标准坐姿时进行语音播报
    * 更换背景图片
    ### Issue
    * 必须点击“关闭程序”退出运行，否则直接关闭程序会导致json缓存遗留

## Meta
* #### ZJUT&nbsp;&nbsp;&nbsp;计算机实验班1801

    王佳  – galliumwang199@gmail.com<br>
    王百城<br>
    陈力<br>
    郑逸伦<br>
    李响<br>

```人工智能```课程自主实验项目<br>
基于GPL-3.0许可. See ``LICENSE`` for more information.


## Contributing
1. Open new Issue or pull request to the master branch
2. For more help or info,please contact ```galliumwang199@gmail.com```

<!-- Markdown link & img dfn's -->