# import pandas as pd
# df = pd.read_excel('../data/materials.xlsx')
# print(df['content'])

import openpyxl
wb = openpyxl.load_workbook('../data/materials.xlsx')
sh = wb.get_sheet_by_name('Sheet1')
case_rows = list(sh.rows)
for case in case_rows[1:]:
    data = []
    for cell in case[1:]:
        print(cell.value)
        data.append(cell.value)
print(data)
    #
    # def read_case_line(self):
    #     '''
    #         读取数据，存入列表中
    #     :return: list
    #     '''
    #     # 按行读取数据，转化为列表
    #     case_rows = list(self.sh.rows)
    #     print("按行读取数据：",case_rows)
    #     #  获取表头
    #     titles = []
    #     for title in case_rows[0]:
    #         titles.append(title.value)
    #     # print("获取表头：",titles)
    #     # 存贮用例的空列表
    #     cases = []
    #     for case in case_rows[1:]:
    #         # print("查看列表1：",case)
    #         # 获取第一条测试用例数据
    #         data = []
    #         for cell in case:
    #             data.append(cell.value)
    #             '''
    #                 判断单元格是否为字符串，
    #                 如果是，则用eval()
    #                 否，则不用eval()
    #             '''
    #             if isinstance(cell.value,str):
    #                 data.append(eval(cell.value))
    #             else:
    #                 data.append(cell.value)
    #             # 将数据存放到cases中
    #             # 将该条数据和表头进行打包组合 dict(list(zip(titles,cases))))
    #         cases_data = dict(list(zip(titles,data)))
    #         cases.append(cases_data)
    #     return cases
    #
    #
    #
