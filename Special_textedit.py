#!D:\anaconda\envs python3
# -*- coding : utf-8 -*-
'''
Created by 24839(jinweiqiang) on 2020/4/1
Project name:--
Project Analysis:--
Communicate ways:QQ(248390697)、wx:--
last edited : 2020/4/1
'''

from PyQt5.QtWidgets import QTextEdit, QLineEdit
from PyQt5 import QtCore


class Special_sentence_textedit(QTextEdit):
    def __init__(self, description: 'str', content_edit: 'QTextEdit'):
        super().__init__(description)
        self.content_edit = content_edit

    def mouseReleaseEvent(self, qMouseEvent):
        if qMouseEvent.button() == QtCore.Qt.LeftButton:
            tc = self.textCursor()
            selectText = tc.selectedText()
            if selectText:
                origin_texts =self.content_edit.toPlainText()
                if origin_texts:
                    origin_text_list =origin_texts.split(sep=' ')
                    if selectText not in origin_text_list:
                        self.content_edit.setText(self.content_edit.toPlainText()+' '+selectText)
                else:
                    self.content_edit.setText(selectText)
        qMouseEvent.accept()

'''不应该重写flag控件，应该重写mainwindow控件'''
class Special_flag_textedit(QLineEdit):
    def __init__(self, description: 'str'):
        super().__init__(description)

    def keyPressEvent(self, qKeyEvent):
        '''
        :param qKeyEvent:  检测按下的是否为数字键
        :return: func：改变该控件下的文本为按下对应键的数字
        '''
        print(qKeyEvent.key())
        if qKeyEvent.key() ==QtCore.Qt.Key_Up:
            print('按下了')