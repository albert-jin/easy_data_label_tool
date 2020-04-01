#!D:\anaconda\envs python3
# -*- coding : utf-8 -*-
'''
Created by 24839(jinweiqiang) on 2020/3/28
Project name:--
Project Analysis:--
Communicate ways:QQ(248390697)、wx:--
last edited : 2020/3/28
'''
from sys import argv,exit
from PyQt5.QtWidgets import QApplication, \
    QLineEdit,QHBoxLayout,QGridLayout,QDialog,QLabel,QPushButton
from PyQt5.QtGui import QIcon

class Select_Index_Dialog(QDialog):
    def __init__(self,father):
        super().__init__()
        self.isOK =False
        self.stop =False
        self.father_menthod =father.receive_info
        self.setWindowIcon(QIcon('图片集合/サンタお年寄り.PNG'))
        self.setWindowTitle('请输入导入内容在excel的列情况：')
        self.title_sentence_idx =QLabel('请输入sentence所在列的下标（必填）:')
        self.line_txt_sentence_idx =QLineEdit('',parent=self)
        self.title_content_idx =QLabel('该行暂不能输入!' if father.mode ==0 else '请输入picked_content所在列的下标(可选):')
        self.line_txt_contents_idx =QLineEdit('',parent=self)
        if father.mode == 0:
            self.line_txt_contents_idx.setReadOnly(True)
        self.title_flag_idx =QLabel('该行暂不能输入!' if father.mode ==1 else '请输入flag所在列的下标（可选）:')
        self.line_txt_flag_idx =QLineEdit('',parent=self)
        if father.mode ==1:
            self.line_txt_flag_idx.setReadOnly(True)
        self.title_begin_idx =QLabel('请指定需要开始标注的行位置（默认智能查找首个）：')
        self.line_txt_begin_idx =QLineEdit('',parent=self)
        self.title_end_idx =QLabel('请指定需要结束标注的行位置（默认智能查找末尾）：')
        self.line_txt_end_idx =QLineEdit('',parent=self)
        btn_submit =QPushButton(icon=QIcon('图片集合/六小灵童.PNG'),text='提交',parent=self)
        btn_submit.clicked.connect(self.click_submit)

        hbox1 =QHBoxLayout()
        hbox1.addWidget(self.title_sentence_idx)
        hbox1.addStretch()
        hbox1.addWidget(self.line_txt_sentence_idx)
        hbox2 =QHBoxLayout()
        hbox2.addWidget(self.title_content_idx)
        hbox2.addStretch()
        hbox2.addWidget(self.line_txt_contents_idx)
        hbox3 =QHBoxLayout()
        hbox3.addWidget(self.title_flag_idx)
        hbox3.addStretch()
        hbox3.addWidget(self.line_txt_flag_idx)
        hbox4 =QHBoxLayout()
        hbox4.addStretch()
        hbox4.addWidget(btn_submit)
        hbox4.addStretch()
        hbox5 =QHBoxLayout()
        hbox5.addStretch(1)
        hbox5.addWidget(self.title_begin_idx)
        hbox5.addWidget(self.line_txt_begin_idx)
        hbox5.addStretch(2)
        hbox5.addWidget(self.title_end_idx)
        hbox5.addWidget(self.line_txt_end_idx)
        hbox5.addStretch(1)

        grid =QGridLayout()
        grid.setSpacing(15)
        grid.addLayout(hbox1,0,0)
        grid.addLayout(hbox2,1,0)
        grid.addLayout(hbox3,2,0)
        grid.addLayout(hbox4,4,0)
        grid.addLayout(hbox5,5,0)
        self.setLayout(grid)
        self.resize(self.sizeHint())
        self.move_father_center(father=father)
        self.show()

    def move_father_center(self,father):
        qr =self.frameGeometry()
        cp =father.frameGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def click_submit(self):
        self.hide()
        self.isOK =True
        print('选择下标控件将提交')
        self.father_menthod()
    def closeEvent(self, QCloseEvent):
        self.stop=True
        self.hide()
        print('选择下标控件关闭')
        QCloseEvent.ignore()
    def get_info(self):
        return self.line_txt_sentence_idx.text(),self.line_txt_contents_idx.text(),self.line_txt_flag_idx.text(), \
               self.line_txt_begin_idx.text(),self.line_txt_end_idx.text()
if __name__ == '__main__':
    app =QApplication(argv)
    class Father():
        def __init__(self,mode):
            self.mode =mode
    SID =Select_Index_Dialog(Father(1))
    exit(app.exec_())