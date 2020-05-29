from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

import json
import time
import threading
import win32console 
import win32gui
import win32con
from math import *
import pyttsx3
from pyttsx3 import driver
from pyttsx3 import drivers
from pyttsx3.drivers import sapi5

initialed=False
global_points_list=None
#global_points_list=[[(0,0),(50,50)],[(0,50),(50,50)]]

def start_openpose():
    os.system("start /min cmd /k start.bat")



folder = './json'

def clear_cache():
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        os.remove(file_path)





def qualified(x,y):
    if( 0.12<x<0.88 and 0.12<y<0.88):
        return True
    else:
        return False

reader=pyttsx3.init()


def no():
    try:
        reader.say("姿势不标准")
        reader.runAndWait()
    except RuntimeError as rt:
        reader.endLoop()
        reader.say("不标准")
        reader.runAndWait()



class DrawCircle(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFixedSize(800,450)
        self.frame_path=QPainterPath()
        self.frame_path.addRoundedRect(QRectF(800*0.12,450*0.12,600,350),50,50)
        #####################
        ###########

    def paintEvent(self,event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.blue,5,Qt.SolidLine))
        qp.begin(self)
        self.paint(qp)
        qp.end()


    def paint(self,qp):
        qp.setRenderHint(qp.Antialiasing)
        qp.fillPath(self.frame_path,QColor(204,204,255))
        qp.drawPath(self.frame_path)
        if(global_points_list==None):
            cover=QPixmap('./image/sitting_ico.png')
            qp.drawPixmap(120,0,cover)
        elif(global_points_list==[]):
            cover=QPixmap('./image/danger.png')
            cover=cover.scaled(QSize(200,200))
            qp.drawPixmap(300,135,cover)
        else:
            qp.setPen(QPen(Qt.black,10,Qt.DashDotLine))
            for i,j in global_points_list:
                qp.drawLine(i[0]*800,i[1]*450,j[0]*800,j[1]*450)

    #def sizeHint(self):
    #    return QSize(800, 450)


class gui(QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        #self.resize(1200, 800)
        self.setFixedSize(1500, 800)
        self.tabs=QTabWidget()
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.palette = QPalette()
        #self.palette.setBrush(QPalette.Background, QBrush(QPixmap('background1.jpg')))
        #self.setPalette(self.palette)#初始化窗口并设置背景图片
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('./image/background3.jpg')))
        self.setPalette(self.palette)
        self.tabs.setFont(QFont("楷体", 20, QFont.Bold) )
        self.crFTab()
        self.crCTab()
        self.tabs.addTab(self.FTab,'功能')
        self.tabs.addTab(self.CTab,'设置')
        mainlayout=QGridLayout()
        mainlayout.addWidget(self.tabs,0,0)
        self.setLayout(mainlayout)
        self.setWindowTitle("标准坐姿检测")

        self.voice_cache=None
        self.current_status=0
        clear_cache()
        cache_timer = QTimer(self)
        cache_timer.timeout.connect(clear_cache)
        cache_timer.start(10000)
        t = threading.Thread(target=self.prepare)
        t.setDaemon(True)
        t.start()
    def prepare(self):
        start_openpose()
        wndtitle = 'OpenPose 1.5.1'
        wndclass = None
        while True:
            wnd=win32gui.FindWindow(wndclass, wndtitle)
            if(wnd!=0):
                win32gui.ShowWindow(win32gui.FindWindow(wndclass, wndtitle), win32con.SW_MINIMIZE)

                break
        while(True):
            if(len(os.listdir(folder))==0):
                global initialed
                initialed=True
                self.status.setText("程序未运行")
                break


    

    def crFTab(self):
        self.FTab=QWidget()
        Tablayout=QGridLayout()
        self.start_botton=QPushButton("开始检测")
        self.start_botton.setCheckable(True)
        self.start_botton.clicked.connect(self.start)
        #self.start_botton.clicked.connect(self.repaint)
        self.quit_button=QPushButton("退出程序")
        self.quit_button.setFlat(True)
        self.quit_button.clicked.connect(self._quit)
        self.start_botton.setFixedSize(200,80)
        self.start_botton.setFont(QFont("华文新魏",20))
        self.quit_button.setFixedSize(100,40)

        self.quit_button.setFont(QFont("华文新魏",15))
        self.coverlabel=QLabel()
        cover_pixmap = QPixmap('./image/cov.png')
        self.coverlabel.setPixmap(cover_pixmap)
        self.status=QLabel("正在初始化")##################################################
        self.status.setAlignment(Qt.AlignCenter)

        self.status.setStyleSheet("QLabel { background-color : white;border-radius: 30px;border-style: outset;\
    border-width: 2px;\
    border-color: bule;}")
        self.status.setFixedSize(700,160)
        self.status.setFont(QFont("隶书",35, QFont.Bold) )
        
        button_layout=QVBoxLayout()
    
        button_layout.addWidget(self.start_botton)
        button_layout.addWidget(self.quit_button,0,Qt.AlignCenter)
        self.pose_drawing=DrawCircle()
        #self.pose_drawing.setStyleSheet("background-color : white;")

        Tablayout.addLayout(button_layout,0,0,1,1,Qt.AlignCenter)
        Tablayout.addWidget(self.coverlabel,1,0,Qt.AlignCenter)
        Tablayout.addWidget(self.status,0,1,Qt.AlignCenter)
        Tablayout.addWidget(self.pose_drawing,1,1,Qt.AlignCenter)


        self.FTab.setLayout(Tablayout)
        palette=QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.FTab.setPalette(palette)

    def repaint(self):
        self.pose_drawing.setColor('green')

    def start(self):
        if(not initialed):
            self.start_botton.setChecked(False)
            warnning_message=QMessageBox()
            warnning_message.setText("程序尚未初始化")
            warnning_message.setIcon(QMessageBox.Warning)
            warnning_message.setWindowTitle("警告")
            warnning_message.setFont(QFont("微软雅黑", 20, QFont.Bold))
            warnning_message.exec()

        elif(self.start_botton.isChecked()):
            #self.CTab.setDisabled(True)
            self.CTabG_1.setDisabled(True)
            self.CTabG_2.setDisabled(True)
            self.start_botton.setText("停止检测")
            self.running_timer = QTimer(self)
            self.running_timer.timeout.connect(self.running)
            self.running_timer.start(30)
        else:
            #self.CTab.setEnabled(True)
            self.CTabG_1.setEnabled(True)
            self.CTabG_2.setEnabled(True)
            self.start_botton.setText("开始检测")
            self.running_timer.stop()
            self.current_status=0
            self.voice_cache=None
            self.status.setText("程序未运行")
            global global_points_list
            global_points_list=None
            self.pose_drawing.update()


    def running(self):

        self.status.setText(self.out())

        if(self.voice_on.isChecked()):
            if(self.status.text()=="不标准"):
                if(self.current_status==0):
                    self.voice_cache=time.time()
                    self.current_status=1
            else:
                if(self.current_status==1):
                    self.current_status=0
                    self.voice_cache=None
            
            if(self.voice_cache!=None and time.time()-self.voice_cache>=3.0):
                threading.Thread(target=no, daemon=True).start()
                self.voice_cache=time.time()

        if(self.scene_on.isChecked()):
            self.pose_drawing.update()
        
                    



    def _quit(self):
        os.system('TASKKILL /F /T /FI "WINDOWTITLE eq running_openpose*"')
        clear_cache()
        self.close()


    #def crFTabG(self):
    #    self.CTabG_4=QGroupBox("关于")
    #    self.CTabG_4.setFont(QFont("Times", 25, QFont.Bold) )
    #    temp_layout=QGridLayout()
#
    #    self.CTabG_4.setLayout(temp_layout)






    def crCTab(self):

        self.crCTabG_1()
        self.crCTabG_2()
        self.crCTabG_3()
        self.crCTabG_4()
        self.CTab=QWidget()
        Tablayout=QGridLayout()
        Tablayout.addWidget(self.CTabG_1,0,0)
        Tablayout.addWidget(self.CTabG_2,0,1)
        Tablayout.addWidget(self.CTabG_3,1,0)
        Tablayout.addWidget(self.CTabG_4,1,1)
        self.CTab.setLayout(Tablayout)



    def crCTabG_1(self):

        self.CTabG_1=QGroupBox("语音提示")
        self.CTabG_1.setFont(QFont("汉仪尚巍手书W",20, QFont.Bold) )
        self.voice_on = QPushButton("开启")
        self.voice_on.setCheckable(True)
        self.voice_on.setFixedHeight(55)
        self.voice_on.setFixedWidth(185)
        #self.voice_on.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.voice_on.clicked.connect(self.voice_switch)
        self.voice_on.setFont(QFont("Times", 15))
        

        #self.voice_label=QLabel("未开启")
        #self.voice_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        #self.voice_label.setFont(QFont("Times", 30, QFont.Bold) )
        #self.resize(pixmap.width(),pixmap.height())
        self.bglabel_speaker=QLabel()
        self.bglabel_speaker.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        pixmap = QPixmap('./image/mute.png')
        #pixmap = QPixmap('sitting_ico.png')
        pixmap=pixmap.scaled(200,200)

        self.bglabel_speaker.setPixmap(pixmap)
        #self.bglabel_speaker.resize(pixmap.width(),pixmap.height())


        temp_layout=QGridLayout()
        #temp_layout.addWidget(self.voice_label,0,0,1,1)
        temp_layout.addWidget(self.bglabel_speaker,0,0,1,1)
        temp_layout.addWidget(self.voice_on,1,0,1,1)


        self.CTabG_1.setLayout(temp_layout)



    def scene_switch(self):
        if(self.scene_on.isChecked()):
            self.scene_on.setText("关闭")
            pixmap = QPixmap('./image/eye_on.ico')
            pixmap=pixmap.scaled(200,200)
            self.bglabel_scene.setPixmap(pixmap)
        else:
            self.scene_on.setText("开启")
            pixmap = QPixmap('./image/eye_off.png')
            pixmap=pixmap.scaled(200,200)
            self.bglabel_scene.setPixmap(pixmap)


    def voice_switch(self):
        if(self.voice_on.isChecked()):
            #self.voice_label.setText("开启中")
            self.voice_on.setText("关闭")
            pixmap = QPixmap('./image/sound.png')
            pixmap=pixmap.scaled(200,200)
            self.bglabel_speaker.setPixmap(pixmap)
        else:
            #self.voice_label.setText("未开启")
            self.voice_on.setText("开启")
            pixmap = QPixmap('./image/mute.png')
            pixmap=pixmap.scaled(200,200)
            self.bglabel_speaker.setPixmap(pixmap)

    





    def crCTabG_2(self):
        self.CTabG_2=QGroupBox("姿态回显")
        self.CTabG_2.setFont(QFont("汉仪尚巍手书W",20, QFont.Bold) )
        self.scene_on = QPushButton("开启")
        self.scene_on.setCheckable(True)
        self.scene_on.setFixedHeight(55)
        self.scene_on.setFixedWidth(185)
        self.scene_on.clicked.connect(self.scene_switch)
        self.scene_on.setFont(QFont("Times", 15))
        

        #self.voice_label=QLabel("未开启")
        #self.voice_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        #self.voice_label.setFont(QFont("Times", 30, QFont.Bold) )
        #self.resize(pixmap.width(),pixmap.height())
        self.bglabel_scene=QLabel()
        self.bglabel_scene.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        pixmap = QPixmap('./image/eye_off.png')
        pixmap=pixmap.scaled(200,200)

        self.bglabel_scene.setPixmap(pixmap)
        #self.bglabel_speaker.resize(pixmap.width(),pixmap.height())


        temp_layout=QGridLayout()
        #temp_layout.addWidget(self.voice_label,0,0,1,1)
        temp_layout.addWidget(self.bglabel_scene,0,0,1,1)
        temp_layout.addWidget(self.scene_on,1,0,1,1)


        self.CTabG_2.setLayout(temp_layout)

    def crCTabG_3(self):
        self.CTabG_3=QGroupBox("主题设置")
        self.CTabG_3.setFont(QFont("汉仪尚巍手书W",20, QFont.Bold) )
        temp_layout=QGridLayout()
        self.bgcontroler=QDial()
        self.bgcontroler.setMinimum(1)
        self.bgcontroler.setMaximum(360)
        self.bgcontroler.setValue(320)
        self.bgcontroler.valueChanged.connect(self._changebg)

        topleft=QLabel("主题八")
        top=QLabel("主题一")
        topright=QLabel("主题二")
        right=QLabel("主题三")
        bottomright=QLabel("主题四")
        bottom=QLabel("主题五")
        bottomleft=QLabel("主题六")
        left=QLabel("主题七")
        
        

        topleft.setFont(QFont("华文彩云", 25, QFont.Bold) )
        topright.setFont(QFont("华文彩云", 25, QFont.Bold) )
        bottomleft.setFont(QFont("华文彩云", 25, QFont.Bold) )
        bottomright.setFont(QFont("华文彩云", 25, QFont.Bold) )
        top.setFont(QFont("华文彩云", 25, QFont.Bold) )
        right.setFont(QFont("华文彩云", 25, QFont.Bold) )
        left.setFont(QFont("华文彩云", 25, QFont.Bold) )
        bottom.setFont(QFont("华文彩云", 25, QFont.Bold) )

        self.bgcontroler.setFixedSize(160,160)
    
        topleft.setAlignment(Qt.AlignCenter)
        topright.setAlignment(Qt.AlignCenter)
        bottomleft.setAlignment(Qt.AlignCenter)
        bottomright.setAlignment(Qt.AlignCenter)
        left.setAlignment(Qt.AlignCenter)
        top.setAlignment(Qt.AlignCenter)
        bottom.setAlignment(Qt.AlignCenter)
        right.setAlignment(Qt.AlignCenter)

        temp_layout.addWidget(self.bgcontroler,1,1)
        temp_layout.addWidget(topleft,0,0)
        temp_layout.addWidget(topright,0,2)
        temp_layout.addWidget(bottomleft,2,0)
        temp_layout.addWidget(bottomright,2,2)
        temp_layout.addWidget(top,0,1)
        temp_layout.addWidget(right,1,2)
        temp_layout.addWidget(left,1,0)
        temp_layout.addWidget(bottom,2,1)
        self.CTabG_3.setLayout(temp_layout)


    def crCTabG_4(self):
        self.CTabG_4=QGroupBox("关于")
        self.CTabG_4.setFont(QFont("汉仪尚巍手书W",20, QFont.Bold) )
        temp_layout=QGridLayout()

        self.CTabG_4.setLayout(temp_layout)



    def createConfigTab(self):
        pass
    
        
    def _changebg(self):
        #self.changebg(self.bgcontroler.value())
        #print(self.bgcontroler.value())

        if(self.bgcontroler.value()>=344):
            self.changebg(4)
        else:
            for i,j in enumerate([(130,230),(230,266),(266,308),(308,344),(1,19),(19,53),(53,93),(93,130)]):
                if(self.bgcontroler.value()>=j[0] and self.bgcontroler.value()<j[1]):
                    self.changebg(i)
                    break

        

    def changebg(self,value):
        if(value==0):
            self.setPalette(QPalette())
        else:
            self.palette.setBrush(QPalette.Background, QBrush(QPixmap('./image/'+'background'+str(value)+'.jpg')))
            self.setPalette(self.palette)


    def out(self):
        if(self.scene_on.isChecked()):
            global global_points_list
            global_points_list=[]
            jsonlist=os.listdir(folder)
            if(len(jsonlist)==0):
                return ("开始监测")

            chosedfile=max(jsonlist)
            with open(folder+'\\'+chosedfile,'r') as jsonfile:
                    data = json.load(jsonfile)
            if(len(data['people'])==0):
                return("未检测到人体")


            key_point_array=data['people'][0]['pose_keypoints_2d']
            middlex,middley=key_point_array[3],key_point_array[4]
            leftx,lefty=key_point_array[6],key_point_array[7]
            rightx,righty=key_point_array[15],key_point_array[16]
            nosex,nosey=key_point_array[0],key_point_array[1]

            needed_points=[middlex,middley,leftx,lefty,rightx,righty,nosex,nosey]


            for i in range(0,7,2):
                if(not qualified(needed_points[i],needed_points[i+1])):
                    return("图像不完整")


            for i,j in [(0,1),(0,15),(0,16),(15,17),(16,18),(1,2),(1,5),(2,3),(3,4),(5,6),(6,7)]:
                    if(qualified(key_point_array[3*i],key_point_array[3*i+1]) and qualified(key_point_array[3*j],key_point_array[3*j+1])):
                        #global_points_list.append([( key_point_array[3*i]  ,  key_point_array[3*j]  ),(key_point_array[3*i+1],key_point_array[3*j+1])])
                        global_points_list.append([( key_point_array[3*i]  ,  key_point_array[3*i+1]  ),(key_point_array[3*j],key_point_array[3*j+1])])

            heady=nosey-middley
            headx=nosex-middlex
            if(headx!=0):
                if(abs(headx/heady)>0.13):
                    return("不标准")


            lsy,lsx=middley-lefty,middlex-leftx
            rsy,rsx=middley-righty,rightx-middlex
            lk=lsy/lsx
            rk=rsy/rsx


            if(not ((abs(lk)<0.25 and abs(rk)<0.25 and lk*rk>0) or (abs(lk)<0.1 and abs(rk)<0.1)) ):
                return("不标准")


            if(1.2>abs(lsx/rsx)>0.8 and abs(heady)>1.3*(abs(lsx)+abs(rsx))/2):
                return("标准")
            else:
                return("不标准")

        else:
            jsonlist=os.listdir(folder)
            if(len(jsonlist)==0):
                return ("开始监测")

            chosedfile=max(jsonlist)
            with open(folder+'\\'+chosedfile,'r') as jsonfile:
                    data = json.load(jsonfile)
            if(len(data['people'])==0):
                return("未检测到人体")


            key_point_array=data['people'][0]['pose_keypoints_2d']
            middlex,middley=key_point_array[3],key_point_array[4]
            leftx,lefty=key_point_array[6],key_point_array[7]
            rightx,righty=key_point_array[15],key_point_array[16]
            nosex,nosey=key_point_array[0],key_point_array[1]

            needed_points=[middlex,middley,leftx,lefty,rightx,righty,nosex,nosey]


            for i in range(0,7,2):
                if(not qualified(needed_points[i],needed_points[i+1])):
                    return("图像不完整")

            heady=nosey-middley
            headx=nosex-middlex
            if(headx!=0):
                if(abs(headx/heady)>0.13):
                    return("不标准")


            lsy,lsx=middley-lefty,middlex-leftx
            rsy,rsx=middley-righty,rightx-middlex
            lk=lsy/lsx
            rk=rsy/rsx


            if(not ((abs(lk)<0.25 and abs(rk)<0.25 and lk*rk>0) or (abs(lk)<0.1 and abs(rk)<0.1)) ):
                return("不标准")


            if(1.2>abs(lsx/rsx)>0.8 and abs(heady)>1.3*(abs(lsx)+abs(rsx))/2):
                return("标准")
            else:
                return("不标准")
    










appctxt = ApplicationContext()
appctxt.app.setStyle('Fusion')
gui_example= gui()
gui_example.show()
sys.exit(appctxt.app.exec_())
    