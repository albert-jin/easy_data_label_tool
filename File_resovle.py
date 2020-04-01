#!D:\anaconda\envs python3
# -*- coding : utf-8 -*-
'''
Created by 24839(jinweiqiang) on 2020/3/28
Project name:--
Project Analysis:--
Communicate ways:QQ(248390697)、wx:--
last edited : 2020/3/28
'''
from xlrd import  open_workbook


class File_resovle():
    @classmethod
    def excel_col_row_count(cls,file_path:'str',file_sheetname:'str'):
        excel =open_workbook(file_path)
        return excel.sheet_by_name(file_sheetname).ncols,excel.sheet_by_name(file_sheetname).nrows

    @classmethod
    def excel_sheet_names(cls, file_path: 'str'):
        excel = open_workbook(file_path)
        return excel.sheet_names()

    @classmethod
    def read_csv(cls):
        pass

    @classmethod
    # 读取某excel的某表单sentence必读字段内容+sentence,flag可选字段 可指定读取区域
    def read_excel(cls, file_path: 'str', choose_sheet: 'str' = None, begin_index: 'int' = None,
                   end_index: 'int' = None, sentence_index: 'int' = None, **params):
        '''

        :param file_path:
        :param choose_sheet:
        :param begin_index: default is the first( sentence legth>5) sentence index
        :param end_index: default is the last row index
        :param params:抽取sentence+{flag_index，content_index}的子集的序号
        :return: wanted_data represents success ,string(wrong info) represents failure
        wanted_data means[{'sentence':__,<'flag':__,'content':__>},.....]
        '''
        try:
            if 'flag_index' in params and  params['flag_index']:
                flag_index = int(params['flag_index'])
            else:
                flag_index =None
            if 'content_index' in params and  params['content_index']:
                content_index = int(params['content_index'])
            else:
                content_index =None
            excel = open_workbook(file_path)
            if choose_sheet.isdigit():
                # sheet = excel.sheet_by_index(int(choose_sheet))   更换的原因是，目前功能只支持name寻找比较稳定
                sheet = excel.sheet_by_name(sheet_name=choose_sheet)
            else:
                sheet = excel.sheet_by_name(sheet_name=choose_sheet)
            # 寻找句子开始位置
            real_begin_index = 0
            stop_flag = False
            while real_begin_index < 100:
                sentence = sheet.row_values(real_begin_index)[sentence_index]
                if '，' in sentence:
                    break
                else:
                    for char_ in sentence:
                        if u'\u4e00' <= char_ <= u'\u9fff' and len(sentence) > 10:
                            stop_flag = True
                            break
                    if stop_flag:
                        break
                real_begin_index += 1
            if not begin_index:
                begin_index = real_begin_index
            elif begin_index < real_begin_index:
                begin_index = real_begin_index

            # 寻找句子结束位置
            real_end_index = begin_index
            while real_end_index < sheet.nrows:
                if (not sheet.row_values(real_end_index)[sentence_index]) or len(
                        sheet.row_values(real_end_index)[sentence_index]) == 0:
                    break
                real_end_index += 1
            if end_index:
                if end_index > real_end_index:
                    end_index = real_end_index
            if not end_index:
                end_index = real_end_index
            wanted_date = []
            for row_idx in range(begin_index, end_index):
                row_data = sheet.row_values(row_idx)
                item = dict()
                item['sentence'] = row_data[sentence_index]
                if flag_index is not None:
                    item['flag'] = row_data[flag_index]
                if content_index is not None:
                    item['content'] = row_data[content_index]
                wanted_date.append(item)
        except Exception as e:
            print('读取excel表格出错，原因:%s' % (str(e.args)))
            return
        else:
            return wanted_date

    @staticmethod
    def read_txt():
        pass

    @staticmethod
    def read_json():
        pass

    @staticmethod
    # 更新excel的数据，更新方式：对出现在excel的sentence更新，未出现的sentence后面添加进去
    def write_excel(cls, data: 'dict', file_path: 'str', choose_sheet: 'str' = None, sentence_index: 'int' = None,
                    set_flag_index: 'int' = None, \
                    set_content_index: 'int' = None):
        pass

if __name__ == '__main__':
    data = File_resovle.read_excel(file_path=r'C:\Users\24839\Desktop\作业\标注作业\20年寒假在家标注任务0.xlsx', choose_sheet='Sheet1', \
                                   begin_index=3, sentence_index=5, flag_index=7, content_index=0)
    print(len(data), data[1:10])
    print(File_resovle.excel_col_row_count(r'C:\Users\24839\Desktop\作业\标注作业\20年寒假在家标注任务0.xlsx','Sheet1'))