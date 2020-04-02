#!D:\anaconda\envs python3
# -*- coding : utf-8 -*-
'''
Created by 24839(jinweiqiang) on 2020/3/27
Project name:--
Project Analysis:--
Communicate ways:QQ(248390697)、wx:--
last edited : 2020/3/27
'''
import json
from Special_textedit import Special_sentence_textedit, Special_flag_textedit
from pathlib import Path
from random import choice
from sys import argv, exit
from Select_Index_Dialog import Select_Index_Dialog
from File_resovle import File_resovle
from PyQt5.QtWidgets import QApplication, QWidget, \
    QToolTip, QAction, QPushButton, QMainWindow, QMessageBox, \
    QDesktopWidget, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QInputDialog, QTextEdit, QLineEdit, QLabel, QSplitter
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtCore

class Main_Frame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data: 'list' = None
        self.file_path: 'str' = None
        self.file_sheetname: 'str' = None
        self.file_length: 'int' = None
        self.file_index: 'int' = None
        self.col_count = None
        self.row_count = None
        self.recept_index_info = None
        self.is_stored = True  # 当打开文件后但没保存时，更改为false
        self.information = '\n' \
                           'Created by 24839(jinweiqiang) on 2020/3/25\n' \
                           'Project name:最简单的数据标注工具\n' \
                           'Project Analysis:这是一款神奇的能让你快乐标注数据的软件！\n' \
                           'Communicate ways:QQ(248390697)、wx:--\n' \
                           'last edited : 2020/3/27\n'
        QToolTip.setFont(QFont('SansSerif', pointSize=8))
        # 初始化的模式 mode:-1
        # 标注句子的分类 mode：0
        # 标注句子中特定位置token mode：1
        # 以上两者都标注 mode：2
        self.mode = -1  # Todo
        self.index = -1
        self.SID = None  # 为了防止子窗口瞬间消失
        self.setToolTip('主窗口')
        self.setWindowTitle('最简易的数据标准软件')
        self.resize(765, 520)
        self.setWindowIcon(QIcon('图片集合/猪头.PNG'))
        self.set_menu()
        self.central_panel = None
        self.btn_open = None
        self.btn_next = None
        self.btn_last = None
        self.laoba_label = None
        self.laoba = None
        self.sentence_title = None
        self.sentence_edit = None
        self.contents_title = None
        self.contents_edit = None
        self.progress_label = None
        self.flag_title = None
        self.flag_edit = None
        self.vbox = None
        self.hbox0 = None
        # self.hbox1 = None 用可缩放代替，更加人性化！
        self.hbox1_2_spliter = None
        self.hbox2 = None
        self.change_view()
        self.make_center()
        self.show()

    # 保存到excel文件
    def save_file_2excel(self):
        try:
            print('保存文件2excel')
            excel_filepath, file_type = QFileDialog.getSaveFileName(self, '保存标注到excel...',
                                                                    directory=r'C:\Users\24839\Desktop', \
                                                                    filter='new_Excel Files(*.xlsx);;old_Excel Files(*xls)')
            print(excel_filepath)
            if not excel_filepath:
                return
            else:
                self.excel_store(excel_filepath)
        except Exception as e:
            print('保存标注到excel出错，原因：', e.args)
        else:
            self.is_stored = True  # 修改标志为成功保存
            self.data = None
            self.mode = -1  # 初始化窗口排布
            self.change_view()

    def excel_store(self, excel_filepath):  # TODO
        pass

    # 保存到json文件
    def save_file_2json(self):
        try:
            if not self.data:
                QMessageBox.warning(self, '保存失败', '你还未打开文件,无数据！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)
                return
            json_filepath, file_type = QFileDialog.getSaveFileName(self, '保存标注到json...',
                                                                   directory=r'C:\Users\24839\Desktop',
                                                                   filter='json Files(*.json)')
            if not json_filepath:
                return
            else:
                print('将data保存2json', json_filepath)
                info = self.json_store(json_filepath)
        except Exception as e:
            print('保存标注到json出错，原因：', e.args)
        else:
            QMessageBox.information(self, 'json保存成功', info + '\n' + '之后可以继续打开文件并进行标注...', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)
            self.is_stored = True
            self.data = None
            self.mode = -1  # 初始化窗口排布
            self.change_view()

    def json_store(self, json_filepath):  # (1)如果文件已存在，将标注内容新增进去，否则创建新文件
        '''data means[{'sentence':__,<'flag':__,'content':__>},.....]'''
        if Path.exists(Path(json_filepath)):
            with Path(json_filepath).open(mode='r', encoding='utf-8') as inf:
                origin_data = json.load(inf)
                change_count = 0
                add_count = 0
                for new_item in self.data:
                    if 'sentence' in new_item:
                        flag = True
                        for index in range(len(origin_data)):
                            if 'sentence' in origin_data[index]:
                                if new_item['sentence'] == origin_data[index]['sentence']:
                                    flag = False
                                    change_count += 1
                                    origin_data[index] = new_item
                                    break
                        if flag == True:
                            origin_data.append(new_item)
                            add_count += 1
                info0 = '修改了{}项,新增了{}项'.format(change_count, add_count)
                print(info0)
            with Path(json_filepath).open(mode='w', encoding='utf-8') as outf:
                json.dump(origin_data, outf, ensure_ascii=False)
                info1 = '往新文件{}共写入{}项'.format(json_filepath, len(self.data))
            print(info1)
            return info0 + '\n' + info1
        else:
            with Path.open(Path(json_filepath), mode='w', encoding='utf-8') as outf:
                json.dump(self.data, outf, ensure_ascii=False)
                info = '往新文件{}共写入{}项'.format(json_filepath, len(self.data))
                print(info)
            return info

    def choose_file(self):
        # QFileDialog.setWindowIcon(self,QIcon('图片集合/尴尬.PNG'))  #TODO 如何设置对话框图片
        '''选择某个文件'''
        try:
            if self.mode in [0, 1, 2]:
                QMessageBox.warning(self,'警告', '还未保存当前工作,请保存后在尝试！', buttons=QMessageBox.Yes, defaultButton=QMessageBox.Yes)
                return
            print('打开文件！')
            file_path = \
                QFileDialog.getOpenFileName(self, caption='请选择一个excel文件...', directory=r'C:\Users\24839\Desktop',
                                            filter='new_Excel Files(*.xlsx);;old_Excel Files(*xls);;Txt Files(*.txt)',
                                            options=QFileDialog.DontUseNativeDialog)[0]
            if file_path is None or len(file_path) == 0 or '.xls' not in file_path:  # TODO 这里限制了只pick  excel
                return
            else:
                self.file_path = file_path
        except Exception as e:
            print('选择文件失败', e.args)
            return

        '''若是excel，则选择其中一个表格'''
        try:
            if '.xls' in self.file_path:
                sheet_names = File_resovle.excel_sheet_names(self.file_path)
                choosed_item, okPressed = QInputDialog.getItem(self, '选择需要读取的表格...', '请选择其一：', sheet_names, 0, False)
                if okPressed:
                    self.file_sheetname = choosed_item
                    self.col_count, self.row_count = File_resovle.excel_col_row_count(file_path=self.file_path,
                                                                                      file_sheetname=self.file_sheetname)
                else:
                    return
        except Exception as e:
            print('excel选择sheet失败,', e.args)
            return
        '''选择标注的模式，标注什么样的内容'''
        try:
            mode_items = ('1.标注(or 修正)句子的分类', '2.标注(or 修正)句子中特定位置token', '3.以上两者都标注')
            choosed_item, okPressed = QInputDialog.getItem(self, '选择标注模式..', '模式：', mode_items, 0, False)
            if okPressed:
                if '1.标注(or 修正)句子的分类' == choosed_item:
                    self.mode = 0
                    print('设置模式{}'.format(self.mode))
                elif '2.标注(or 修正)句子中特定位置token' == choosed_item:
                    self.mode = 1
                    print('设置模式{}'.format(self.mode))
                else:
                    self.mode = 2
                    print('设置模式{}'.format(self.mode))
            else:
                return
        except Exception as e:
            print('设置模式失败,原因', e.args)
            return

        '''选择表格中的begin-row,end-row,sentence-col-idx,flag-col-idx,content-col-index'''
        try:
            self.SID = Select_Index_Dialog(self)
        except Exception as e:
            print('索引子窗口创建失败,原因:', e.args)
            return
        else:
            print('索引子窗口创建成功')

    def receive_info(self):
        self.recept_index_info = self.SID.get_info()
        print('主窗体已接受到子窗体的信息', self.recept_index_info)
        if not self.recept_index_info[0]:
            QMessageBox.warning(self, '操作失败！', '你未输入sentence所在index！', buttons=QMessageBox.Yes,
                                defaultButton=QMessageBox.Yes)
            return
        elif not self.recept_index_info[0].isdigit():
            QMessageBox.warning(self, '操作失败！', '你输入的sentence下标不是数字！', buttons=QMessageBox.Yes,
                                defaultButton=QMessageBox.Yes)
            return
        elif int(self.recept_index_info[0]) >= self.col_count or int(self.recept_index_info[0]) < 0:
            QMessageBox.warning(self, '操作失败！', '你输入的sentence下标不在合适区间！', buttons=QMessageBox.Yes,
                                defaultButton=QMessageBox.Yes)
            return
        elif self.recept_index_info[1]:
            if not self.recept_index_info[1].isdigit():
                QMessageBox.warning(self, '操作失败！', '你输入的content下标不是数字！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)
                return
            if int(self.recept_index_info[1]) >= self.col_count or int(self.recept_index_info[1]) < 0:
                QMessageBox.warning(self, '操作失败！', '你输入的content下标不在合适区间！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)
                return
        elif self.recept_index_info[2]:
            if not self.recept_index_info[2].isdigit():
                QMessageBox.warning(self, '操作失败！', '你输入的flag下标不是数字！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)
                return
            if int(self.recept_index_info[2]) >= self.col_count or int(self.recept_index_info[2]) < 0:
                QMessageBox.warning(self, '操作失败！', '你输入的flag下标不在合适区间！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)
                return
        elif self.recept_index_info[3]:
            if not self.recept_index_info[3].isdigit():
                QMessageBox.warning(self, '操作失败！', '你输入的开始行下标不是数字！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)  # begin不是数字
                return
            if not 0 < int(self.recept_index_info[3]) < self.row_count:
                QMessageBox.warning(self, '操作失败！', '你输入开始行的数字不合理！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)  # begin数字不合理
                return
            if self.recept_index_info[4]:
                if not self.recept_index_info[4].isdigit():
                    QMessageBox.warning(self, '操作失败！', '你输入的结束行下标不是数字！', buttons=QMessageBox.Yes,
                                        defaultButton=QMessageBox.Yes)  # begin&end都存在 但end不是数字
                    return
                if not 0 <= int(self.recept_index_info[3]) < int(self.recept_index_info[4]) < self.row_count:
                    QMessageBox.warning(self, '操作失败！', '你输入开始&结束行区间不合理！', buttons=QMessageBox.Yes,
                                        defaultButton=QMessageBox.Yes)  # begin&end都存在 但end数字不合理
                    return
        elif self.recept_index_info[4]:
            if not self.recept_index_info[4].isdigit():
                QMessageBox.warning(self, '操作失败！', '你输入的结束行下标不是数字！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)  # 没有begin，end不是数字
                return
            if not 0 < int(self.recept_index_info[4]) < self.row_count:
                QMessageBox.warning(self, '操作失败！', '你输入结束行的数字不合理！', buttons=QMessageBox.Yes,
                                    defaultButton=QMessageBox.Yes)  # 没有begin，end数字不合理
                return
        self.data = File_resovle.read_excel(file_path=self.file_path, choose_sheet=self.file_sheetname, \
                                            sentence_index=int(self.recept_index_info[0]), \
                                            content_index=self.recept_index_info[1] if self.recept_index_info[
                                                1] else None, \
                                            flag_index=self.recept_index_info[2] if self.recept_index_info[2] else None, \
                                            begin_index=int(self.recept_index_info[3]) if self.recept_index_info[
                                                3] else None, \
                                            end_index=int(self.recept_index_info[4]) if self.recept_index_info[
                                                4] else None
                                            )
        if not self.data:
            QMessageBox.warning(self, '读取excel错误', '读出的内容为空！！', buttons=QMessageBox.Yes, defaultButton=QMessageBox.Yes)
            return
        print('数据查找到', len(self.data), '项,可视化前五项:', self.data[0:5])  # 只是为了验证数据合理性
        self.index = -1
        self.change_view()
        self.is_stored = False

    def keyPressEvent(self,qkeyevent):
        '''
        检测按键是否是数字键，有条件的改变flag控件的内容
        '''
        try:
            if self.mode == -1 or self.mode ==1:
                return
            if  48<=qkeyevent.key()<=57:
                self.flag_edit.setText(str(qkeyevent.key()-48))
        except Exception as e:
            print(e.args)
        finally:
            qkeyevent.accept()

    def change_view(self):
        if self.mode == 0:  # 只标注句子分类
            self.progress_label = QLabel('目前您正处于[未开始{}/{}]'.format(self.index + 1, len(self.data)))
            self.btn_next = self.my_create_Button(name='下一页(Alt+&S)', icon=QIcon('图片集合/竖大拇指反向.PNG'),
                                                  trigger_function=self.next_sentence)
            self.btn_last = self.my_create_Button(name='上一页(Alt+&W)', icon=QIcon('图片集合/竖大拇指.PNG'),
                                                  trigger_function=self.last_sentence)
            self.flag_title = QLabel('标注的类别：')
            self.flag_edit = QLineEdit('点击下方“下一页(Alt+S)”按钮开始标注...')
            self.sentence_title = QLabel('需标注的句子：')
            self.sentence_edit = QTextEdit('点击下方“下一页(Alt+S)”按钮开始标注...')
            self.sentence_edit.setReadOnly(True)
            self.central_panel = QWidget()
            self.setCentralWidget(self.central_panel)

            self.hbox0 = QHBoxLayout()
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.sentence_title)
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.flag_title)
            self.hbox0.addStretch()

            # self.hbox1 = QHBoxLayout()
            # self.hbox1.addStretch()
            # self.hbox1.addWidget(self.sentence_edit)
            # self.hbox1.addStretch()
            # self.hbox1.addWidget(self.flag_edit)
            # self.hbox1.addStretch()
            self.hbox1_2_spliter = QSplitter()
            self.hbox1_2_spliter.addWidget(self.sentence_edit)
            self.hbox1_2_spliter.addWidget(self.flag_edit)

            self.hbox2 = QHBoxLayout()
            self.hbox2.addWidget(self.btn_last)
            self.hbox2.addStretch(1)
            self.hbox2.addWidget(self.btn_next)
            self.hbox2.addStretch(3)
            self.hbox2.addWidget(self.progress_label)

            self.vbox = QVBoxLayout()
            self.vbox.addLayout(self.hbox0)
            self.vbox.addStretch()
            # self.vbox.addLayout(self.hbox1)
            self.vbox.addWidget(self.hbox1_2_spliter)
            self.vbox.addStretch()
            self.vbox.addLayout(self.hbox2)

            self.central_panel.setLayout(self.vbox)
            self.statusBar().showMessage('正在模式0（flag）...')

        elif self.mode == 1:  # 只标注content
            self.progress_label = QLabel('目前您正处于[未开始{}/{}]'.format(self.index + 1, len(self.data)))
            self.sentence_title = QLabel('需标注的句子：')
            self.contents_title = QLabel('选中的子串：')
            self.contents_edit = QTextEdit('点击下方“下一页(Alt+S)”按钮开始标注...')
            self.sentence_edit = Special_sentence_textedit('点击下方“下一页(Alt+S)”按钮开始标注...',content_edit=self.contents_edit)
            self.sentence_edit.setReadOnly(True)
            self.btn_next = self.my_create_Button(name='下一页(Alt+&S)', icon=QIcon('图片集合/竖大拇指反向.PNG'),
                                                  trigger_function=self.next_sentence)
            self.btn_last = self.my_create_Button(name='上一页(Alt+&W)', icon=QIcon('图片集合/竖大拇指.PNG'),
                                                  trigger_function=self.last_sentence)
            self.central_panel = QWidget()
            self.setCentralWidget(self.central_panel)

            self.hbox0 = QHBoxLayout()
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.sentence_title)
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.contents_title)
            self.hbox0.addStretch()
            # self.hbox1 = QHBoxLayout()
            # self.hbox1.addStretch()
            # self.hbox1.addWidget(self.sentence_edit)
            # self.hbox1.addStretch()
            # self.hbox1.addWidget(self.contents_edit)
            # self.hbox1.addStretch()
            self.hbox1_2_spliter = QSplitter()
            self.hbox1_2_spliter.addWidget(self.sentence_edit)
            self.hbox1_2_spliter.addWidget(self.contents_edit)

            self.hbox2 = QHBoxLayout()
            self.hbox2.addWidget(self.btn_last)
            self.hbox2.addStretch(1)
            self.hbox2.addWidget(self.btn_next)
            self.hbox2.addStretch(3)
            self.hbox2.addWidget(self.progress_label)

            self.vbox = QVBoxLayout()
            self.vbox.addLayout(self.hbox0)
            self.vbox.addStretch()
            # self.vbox.addLayout(self.hbox1)
            self.vbox.addWidget(self.hbox1_2_spliter)
            self.vbox.addStretch()
            self.vbox.addLayout(self.hbox2)

            self.central_panel.setLayout(self.vbox)
            self.statusBar().showMessage('正在模式1（content）...')
        elif self.mode == 2:  # 两个都标注
            self.progress_label = QLabel('目前您正处于[未开始{}/{}]'.format(self.index + 1, len(self.data)))
            self.sentence_title = QLabel('需标注的句子：')
            self.contents_title = QLabel('选中的子串：')
            self.contents_edit = QTextEdit('点击下方“下一页(Alt+S)”按钮开始标注...')
            self.sentence_edit = Special_sentence_textedit('点击下方“下一页(Alt+S)”按钮开始标注...',content_edit=self.contents_edit)
            self.sentence_edit.setReadOnly(True)
            self.flag_title = QLabel('标注的类别：')
            self.flag_edit = QLineEdit('点击下方“下一页(Alt+S)”按钮开始标注...')
            self.btn_next = self.my_create_Button(name='下一页(Alt+&S)', icon=QIcon('图片集合/竖大拇指反向.PNG'),
                                                  trigger_function=self.next_sentence)
            self.btn_last = self.my_create_Button(name='上一页(Alt+&W)', icon=QIcon('图片集合/竖大拇指.PNG'),
                                                  trigger_function=self.last_sentence)
            self.central_panel = QWidget()
            self.setCentralWidget(self.central_panel)

            self.hbox0 = QHBoxLayout()
            self.hbox0.addWidget(self.sentence_title)
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.contents_title)
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.flag_title)

            # self.hbox1 = QHBoxLayout()
            # self.hbox1.addWidget(self.sentence_edit)
            # self.hbox1.addStretch()
            # self.hbox1.addWidget(self.contents_edit)
            # self.hbox1.addStretch()
            # self.hbox1.addWidget(self.flag_edit)
            self.hbox1_2_spliter = QSplitter()
            self.hbox1_2_spliter.addWidget(self.sentence_edit)
            self.hbox1_2_spliter.addWidget(self.contents_edit)
            self.hbox1_2_spliter.addWidget(self.flag_edit)

            self.hbox2 = QHBoxLayout()
            self.hbox2.addWidget(self.btn_last)
            self.hbox2.addStretch(1)
            self.hbox2.addWidget(self.btn_next)
            self.hbox2.addStretch(3)
            self.hbox2.addWidget(self.progress_label)

            self.vbox = QVBoxLayout()
            self.vbox.addLayout(self.hbox0)
            self.vbox.addStretch()
            # self.vbox.addLayout(self.hbox1)
            self.vbox.addWidget(self.hbox1_2_spliter)
            self.vbox.addStretch()
            self.vbox.addLayout(self.hbox2)

            self.central_panel.setLayout(self.vbox)

            self.statusBar().showMessage('正在模式2（content&flag）...')
        else:
            self.btn_open = self.my_create_Button(name='老八提醒您，请打开一个excel文件',
                                                  icon=QIcon('图片集合/小劳府.PNG'),
                                                  trigger_function=self.choose_file)
            self.laoba_label = QLabel()
            self.laoba = QPixmap('图片集合/奥里给，淦了，兄弟萌.jpg')
            self.laoba_label.setPixmap(self.laoba)
            self.central_panel = QWidget()
            self.setCentralWidget(self.central_panel)
            self.vbox = QVBoxLayout()
            self.hbox0 = QHBoxLayout()
            self.hbox0.addStretch()
            self.hbox0.addWidget(self.laoba_label)
            self.hbox0.addStretch()
            self.vbox.addStretch()
            self.vbox.addLayout(self.hbox0)
            self.vbox.addStretch()
            self.vbox.addWidget(self.btn_open)

            self.central_panel.setLayout(self.vbox)

            self.statusBar().showMessage('待选择文件...')

    def last_sentence(self):  # TODO 事件触发保存此时的内容进self.data,并加入is_stored 的事件,修改progress_label
        print('点击了上一个')
        # 将上一个标注写入data
        if self.mode ==-1:
            return
        try:
            if self.mode != 0:  # 设置content
                self.data[self.index]['content'] = self.contents_edit.toPlainText()
            if self.mode != 1:  # 设置flag
                self.data[self.index]['flag'] = self.flag_edit.text()

            if self.index <= 0:
                QMessageBox.warning(self, '温馨提示..', '您已经在标注位置最前了,不能再往前回退了！', buttons=QMessageBox.Yes)
                return
            self.index -= 1
            self.sentence_edit.setReadOnly(False)
            self.sentence_edit.setText(str(self.data[self.index]['sentence']))
            self.sentence_edit.setReadOnly(True)
            if self.mode != 0:
                if 'content' in self.data[self.index]:
                    self.contents_edit.setText(str(self.data[self.index]['content']))
                else:
                    self.contents_edit.setText('')
            if self.mode != 1:   # 就为了将0.0转为0，俺太难了
                if 'flag' in self.data[self.index]:
                    if isinstance(self.data[self.index]['flag'],(float,int)):
                        self.flag_edit.setText(str(int(self.data[self.index]['flag'])))
                    else:
                        if self.data[self.index]['flag'].replace('.','',1).isdigit():
                            self.flag_edit.setText(str(int(eval(self.data[self.index]['flag']))))
                        else:
                            self.flag_edit.setText(self.data[self.index]['flag'])
                else:
                    self.flag_edit.setText('')
            self.progress_label.setText('目前您正在标注,进度：[{}/{}]'.format(self.index + 1, len(self.data)))
        except Exception as e:
            QMessageBox.warning(self, '错误！', '翻上一页时遇到错误,原因：{}'.format(e.args))

    def next_sentence(self):  # TODO 同上
        print('点击了下一个')
        # 将上一个标注写入data
        if self.mode == -1:
            return
        try:
            if self.index >= 0:
                if self.mode != 0:
                    self.data[self.index]['content'] = self.contents_edit.toPlainText()
                if self.mode != 1:
                    self.data[self.index]['flag'] = self.flag_edit.text()

            if self.index + 1 >= len(self.data):
                QMessageBox.warning(self, '温馨提示..', '您太努力了,居然成功标注完了！\n接下来可以选择保存（建议<json>---Ctrl+S）', \
                                    buttons=QMessageBox.Yes, defaultButton=QMessageBox.Yes)
                return
            self.index += 1
            self.sentence_edit.setReadOnly(False)
            self.sentence_edit.setText(str(self.data[self.index]['sentence']))
            self.sentence_edit.setReadOnly(True)
            if self.mode != 0:
                if 'content' in self.data[self.index]:
                    self.contents_edit.setText(str(self.data[self.index]['content']))
                else:
                    self.contents_edit.setText('')
            if self.mode != 1:
                if 'flag' in self.data[self.index]:  # 就为了将0.0转为0，俺太难了
                    if isinstance(self.data[self.index]['flag'],(float,int)):
                        self.flag_edit.setText(str(int(self.data[self.index]['flag'])))
                    else:
                        if self.data[self.index]['flag'].replace('.','',1).isdigit():
                            self.flag_edit.setText(str(int(eval(self.data[self.index]['flag']))))
                        else:
                            self.flag_edit.setText(self.data[self.index]['flag'])
                else:
                    self.flag_edit.setText('')
            self.progress_label.setText('目前您正在标注,进度：[{}/{}]'.format(self.index + 1, len(self.data)))
        except Exception as e:
            QMessageBox.warning(self, '错误！', '翻下一页时遇到错误,原因：{}'.format(e.args))

    def show_information(self):
        try:
            QMessageBox.about(self, '关于我们的基本信息', self.information if self.information else '暂无信息')

        except Exception as e:
            print(e.args)

    def set_menu(self):
        '''
        配置菜单栏属性
        :return: None
        '''
        menuBar = self.menuBar()

        # 菜单栏 --文件
        first_menu = menuBar.addMenu('&文件 file')
        ##选择原文件
        self.choose_Action = self.my_create_Action(name='打开原文件 excel', icon=QIcon('图片集合/企鹅大叫.PNG'), shortcut='Ctrl+O',
                                                   trigger_function=self.choose_file)
        first_menu.addAction(self.choose_Action)
        ##保存原文件到excel
        self.save_Action0 = self.my_create_Action(name='保存标注到excel（可修改原excel）', icon=QIcon('图片集合/狗头.PNG'),
                                                  shortcut='Ctrl+E',
                                                  trigger_function=self.save_file_2excel)
        first_menu.addAction(self.save_Action0)
        ##保存原文件到json
        self.save_Action1 = self.my_create_Action(name='保存标注到json (推荐)', icon=QIcon('图片集合/树懒.PNG'), shortcut='Ctrl+S', \
                                                  trigger_function=self.save_file_2json)
        first_menu.addAction(self.save_Action1)
        # 菜单栏 --工具
        second_menu = menuBar.addMenu('&工具 tools')
        ##居中主窗口
        self.choose_Action = self.my_create_Action(name='居中主窗口', icon=QIcon('图片集合/重拳出击.PNG'), shortcut='Ctrl+G',
                                                   trigger_function=self.make_center)
        second_menu.addAction(self.choose_Action)
        ##翻到上一页
        self.last_page_Action = self.my_create_Action(name='转到上一个', icon=QIcon('图片集合/竖大拇指.PNG'), shortcut='Esc',
                                                      trigger_function=self.last_sentence)
        second_menu.addAction(self.last_page_Action)
        ##翻到下一页
        self.next_page_Action = self.my_create_Action(name='转到下一个', icon=QIcon('图片集合/竖大拇指反向.PNG'), shortcut='Space',
                                                      trigger_function=self.next_sentence)
        second_menu.addAction(self.next_page_Action)
        ##切换背景图片
        self.change_background_Action = self.my_create_Action(name='切换随机背景', icon=QIcon('图片集合/rose.PNG'),
                                                              trigger_function=self.change_background)
        second_menu.addAction(self.change_background_Action)

        # 菜单栏 --帮助
        third_menu = menuBar.addMenu('&帮助 help')
        ##查看基本信息
        self.show_information_Action = self.my_create_Action(name='关于我们', icon=QIcon('图片集合/鬼怪.PNG'),
                                                             shortcut='Alt+O',
                                                             trigger_function=self.show_information)
        third_menu.addAction(self.show_information_Action)
        ##查看教程
        self.show_guide_Action = self.my_create_Action(name='查看帮助文档', icon=QIcon('图片集合/蒙蔽脸.PNG'),
                                                       shortcut='Ctrl+H',
                                                       trigger_function=self.show_guide)
        third_menu.addAction(self.show_guide_Action)

    # 帮助文档显示
    def show_guide(self):
        try:
            QMessageBox.information(self, '帮助信息', '1.初版的软件只加了读excel&写入json的功能,暂时够用就好,以后持续扩充'
                                                  '\n2.可能有些依赖库冲突|缺失问题，本人未能完全顾及，可联系小金解决'
                                                  '\n还未写使用文档,要提醒的是，多帮我找些bug出来,谢谢！')
        except Exception as e:
            print(e.args)

    # 切换背景图片
    def change_background(self):
        image_list = ['background-image:url(图片集合/背景_绿.PNG)', 'background-image:url(图片集合/哆啦A梦.PNG)', '图片集合/纯白背景图.PNG']
        self.setStyleSheet(choice(image_list))

    # 重写关闭窗口事件处理函数
    def closeEvent(self, close_event):
        '''
        触发退出工作流功能
        :return:
        '''
        try:
            if self.is_stored == False:
                query = QMessageBox.warning(self, '警告', '注意！你尚未保存最近一次修改，是否保存？\n（声明:__不保存导致的后果自负，作者不承担__）',
                                            buttons=QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.Yes)
                if query == QMessageBox.Yes:
                    self.save_file_2json()
            query = QMessageBox.question(self, '温馨提示', self.tr('你确定终止该工作流吗？'), buttons= \
                QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.No)
            if query == QMessageBox.Yes:
                close_event.accept()
            else:
                close_event.ignore()
        except Exception as e:
            print(e.args)

    def make_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 返回空代表create event 失败，成功返回event 实例
    def my_create_Action(self, name: 'str', shortcut: 'str' = None, icon: 'QIcon' = None,
                         trigger_function: 'function' = None):
        try:
            if not icon:
                Action_instance = QAction(text=name, parent=self)
            else:
                Action_instance = QAction(text=name, icon=icon, parent=self)
            if shortcut:
                Action_instance.setShortcut(shortcut)
            if trigger_function:
                Action_instance.triggered.connect(trigger_function)
        except Exception as e:
            print(name + '动作创建失败，失败原因：{}'.format(str(e.args)))
            return None
        else:
            return Action_instance

    # 返回空代表create button 失败，成功返回button 实例
    def my_create_Button(self, name: 'str', icon: 'QIcon' = None, parent=None, button_size=None,
                         trigger_function: 'function' = None):
        '''
        Attention:parent 默认不是self，默认没有parent
        '''
        try:
            if not parent and not icon:
                btn = QPushButton(text=name)
            elif parent and icon:
                btn = QPushButton(icon=icon, text=name, parent=parent)
            elif not parent and icon:
                btn = QPushButton(icon=icon, text=name)
            else:
                btn = QPushButton(text=name, parent=parent)
            if button_size:
                btn.resize(button_size)
            else:
                btn.resize(btn.sizeHint())
            if trigger_function:
                btn.clicked.connect(trigger_function)
                # btn.move(self.width() - btn.size().width(), self.height() - btn.size().height())  位置后续由窗格Layout设置
            return btn
        except Exception as e:
            print(name + '按钮创建失败，失败原因：{}'.format(str(e.args)))
            return None


if __name__ == '__main__':
    app = QApplication(argv)
    main_frame = Main_Frame()
    exit(app.exec_())
