from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.Model.PreModel import *
from src.FrequencyType import Freq
from src.ConstantType import *
from src.Method import *
from src.ConfigHeadList import *
from src.Data2Excel import *
from src.RowData import RowData

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False

import pandas as pd
import time
import itertools
import os
import sys


def main_cal(path1, path2, path3):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    #################################################################################

    # 参数输入

    df_input = pd.read_excel(path1)
    df_input = df_input.where(df_input.notnull(), None)
    num_len = len(list(df_input['序号']))

    # 检查输入格式
    # check_input(df_input)

    #################################################################################

    # # 获取时间戳
    # localtime = time.localtime()
    # timestamp = time.strftime("%Y%m%d%H%M%S", localtime)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

    #################################################################################

    # 初始化变量
    # work_path = os.getcwd()
    work_path = path3
    para = ModelParameter(workpath=work_path)

    para['MAX_CURRENT'] = {
        1700: 197,
        2000: 175,
        2300: 162,
        2600: 150,
    }

    # 钢轨阻抗
    trk_2000A_21 = ImpedanceMultiFreq()
    trk_2000A_21.rlc_s = {
        1700: [1.177, 1.314e-3, None],
        2000: [1.306, 1.304e-3, None],
        2300: [1.435, 1.297e-3, None],
        2600: [1.558, 1.291e-3, None]}

    para['Trk_z'].rlc_s = trk_2000A_21.rlc_s

    para['Ccmp_z_change_zhu'] = ImpedanceMultiFreq()
    para['Ccmp_z_change_chuan'] = ImpedanceMultiFreq()

    # para['TB_引接线_有砟'] = ImpedanceMultiFreq()
    # para['TB_引接线_有砟'].z = {
    #     1700: (8.33 + 31.4j)*1e-3,
    #     2000: (10.11 + 35.2j)*1e-3,
    #     2300: (11.88 + 39.0j)*1e-3,
    #     2600: (13.60 + 42.6j)*1e-3}
    #
    # para['Zl_rcv'] = ImpedanceMultiFreq()

    #################################################################################

    # 获取表头
    # head_list = config_headlist_ypmc()
    # head_list = config_headlist_2000A_inte()
    # head_list = config_headlist_2000A_QJ()
    # head_list = config_headlist_inhibitor_c()
    # head_list = config_headlist_hanjialing()
    # head_list = config_headlist_20200730()
    # head_list = config_headlist_V001()
    # head_list = config_headlist_optimize()
    head_list = config_headlist_QJ_20220216()

    #################################################################################

    # 初始化excel数据
    excel_data = []
    # data2excel = Data2Excel(sheet_names=[])
    data2excel = SheetDataGroup(sheet_names=[])

    #################################################################################

    # 故障状态表
    # temp_list = ['正常']
                 # '主串PT开路', '被串PT开路', '主被串PT开路',
                 # '主串PT短路', '被串PT短路', '主被串PT短路',
                 # '主串SVA1开路', '被串SVA1开路', '主被串SVA1开路',
                 # '主串SVA1短路', '被串SVA1短路', '主被串SVA1短路',
                 # '主串TB开路', '被串TB开路', '主被串TB开路',
                 # '主串TB短路', '被串TB短路', '主被串TB短路']

    #################################################################################

    BASE = 'D2K11+790 = K558+104'

    # info_line1 = [
    #     -36,
    #     ('0132AG', 2000, 475, 8),
    #     ('0132BG', 2600, 475, 6),
    #     ('0132CG', 2000, 500, 8),
    #     ('0148AG', 2600, 400, 5),
    #     ('0148BG', 2000, 600, 10),
    #     ('0148CG', 2600, 500, 6),
    #     ('0162AG', 2000, 551, 10),
    #     ('0162BG-1', 2600, 551, 7),
    #     ('0162BG-2', 2000, 400, 6),
    #     ('0178AG', 2600, 700, 8),
    # ]
    #
    # info_line2 = [
    #     -294,
    #     ('NS1LQAG', 2000, 537, 9),
    #     ('5578CG', 2600, 470, 6),
    #     ('5578BG', 2000, 625, 10),
    #     ('5578AG', 2600, 745, 9),
    #     ('5560CG', 2000, 505, 9),
    #     ('5560BG', 2600, 625, 8),
    #     ('5560AG', 2000, 760, 13),
    #     ('5542CG', 2600, 490, 6),
    #     ('5542BG', 2000, 560, 10),
    #     ('5542AG', 2600, 800, 10),
    # ]
    #
    # info_line3 = [
    #     -615,
    #     ('S1LQBG', 2600, 464, 6),
    #     ('S1LQAG', 2000, 464, 8),
    #     ('8420DG', 2600, 625, 8),
    #     ('8420CG', 2000, 745, 12),
    #     ('8420BG', 2600, 505, 7),
    #     ('8420AG', 2000, 625, 10),
    #     ('8394CG', 2600, 766, 10),
    #     ('8394BG', 2000, 490, 8),
    #     ('8394AG', 2600, 550, 7),
    #     ('8376CG', 2000, 810, 14),
    # ]

    info_line1 = [
        0,
        ('模拟2600Hz区段', 2600, 400, 0),
    ]

    info_line2 = [
        0,
        ('5578CG', 2600, 470, 6),
        ('5578BG', 2000, 625, 10),
    ]

    res_list = []
    for offset in range(0, 500, 10):
        info_line1[0] = offset
        res_list.extend(get_line_info(info_line1, info_line2))
        # res_list.extend(get_line_info(info_line2, info_line1))
    # res_list.extend(get_line_info(info_line2, info_line3))
    # res_list.extend(get_line_info(info_line3, info_line2))

    for tmp in res_list:
        print(tmp)

    #################################################################################

    # 获取循环变量
    clist1 = clist2 = clist3 = clist4 = clist5 = clist6 = [[]]

    clist1 = res_list
    clist2 = ['左发', '右发']
    clist3 = ['左发', '右发']

    clist = list(itertools.product(
        clist1, clist2, clist3, clist4, clist5, clist6))

    print('总行数：%s' % str(len(clist)))

    #################################################################################

    columns_max = 0
    counter = 1

    temp_temp = 0
    cv1, cv2, cv3, cv4, cv5, cv6 = [0] * 6

    # pd_read_flag = True
    pd_read_flag = False

    # num_len = 1

    # for temp_temp in range(num_len):
    for cv1, cv2, cv3, cv4, cv5, cv6 in clist:
    # for cv0 in res_list:

        zhu_name = cv1[0][0]
        zhu_freq = cv1[0][1]
        zhu_length = cv1[0][2]
        zhu_c_num = cv1[0][3]

        zip0 = list(zip(*cv1[1]))
        bei_name = list(zip0[0])
        bei_freq = list(zip0[1])
        bei_length = list(zip0[2])
        bei_c_num = list(zip0[3])

        print()
        #################################################################################

        # # 封装程序显示
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # if getattr(sys, 'frozen', False):
        #     print(df_input[temp_temp:(temp_temp + 1)])
        # print(temp_temp)
        print('calculating line ' + str(counter) + ' ...')

        #################################################################################

        # 数据表初始化
        data = dict()
        for key in head_list:
            data[key] = None

        # 添加数据行
        # data2excel.add_row()
        # data2excel.add_new_row()

        # 打包行数据
        df_input_row = df_input.iloc[temp_temp]
        row_data = RowData(df_input_row, para, data, pd_read_flag)

        # para['param'] = cv2

        #################################################################################

        # 载入数据
        flag = pd_read_flag

        # 序号
        row_data.config_number(counter, pd_read_flag=flag)

        # 备注
        # row_data.config_remarks('主分路被调整', pd_read_flag=False)
        row_data.config_remarks('广湛四线并行', pd_read_flag=flag)

        row_data.config_sec_name(zhu_name, bei_name, pd_read_flag=flag)

        # row_data.config_sec_length(cv2.lens_zhu[0], cv2.lens_bei[cv2.index_bei], pd_read_flag=flag)
        row_data.config_sec_length(zhu_length, bei_length, pd_read_flag=flag)
        row_data.config_offset(cv1[2], pd_read_flag=False)
        # row_data.config_offset(0, pd_read_flag=True)

        row_data.config_mutual_coeff(20, pd_read_flag=flag)
        # row_data.config_freq(cv1[0], cv1[1], pd_read_flag=flag)
        row_data.config_freq(zhu_freq, bei_freq, pd_read_flag=flag)
        # row_data.config_freq(cv1, cv2, pd_read_flag=flag)
        # row_data.config_c_num('auto', 'auto', pd_read_flag=flag)
        row_data.config_c_num(zhu_c_num, bei_c_num, pd_read_flag=flag)
        row_data.config_c_posi(None, None, pd_read_flag=False)
        # if temp_temp == 4:
        #     row_data.config_c_posi(None, [514/2], pd_read_flag=False)
        row_data.config_c2TB(False)

        # row_data.config_c_value(25, 25, pd_read_flag=flag)
        row_data.config_c_value(25, 25, pd_read_flag=flag)
        # row_data.config_c_value(cv3, cv3, pd_read_flag=flag)

        # row_data.config_c_inhibitor(pd_read_flag=flag)

        # row_data.config_c_fault_mode('无', cv2, pd_read_flag=flag)
        # row_data.config_c_fault_num([], cv3, pd_read_flag=flag)

        # row_data.config_c_fault_mode(['无'], ['无'], pd_read_flag=flag)
        # row_data.config_c_fault_num([], [], pd_read_flag=flag)
        row_data.config_c_fault_mode(['无'], ['无'], pd_read_flag=False)
        row_data.config_c_fault_num([], [], pd_read_flag=False)

        row_data.config_rd(1e10, 1e10, pd_read_flag=flag, respectively=True)

        # row_data.config_trk_z(pd_read_flag=flag, respectively=False)
        # row_data.config_trk_z(pd_read_flag=flag, respectively=True)
        # row_data.config_trk_z(pd_read_flag=False, respectively=True)
        row_data.config_trk_z(pd_read_flag=False, respectively=False)

        # TB模式
        row_data.config_TB_mode('无TB', pd_read_flag=False)
        # row_data.config_TB_mode('双端TB', pd_read_flag=flag)
        # row_data.config_TB_mode('双端TB', pd_read_flag=False)

        row_data.config_sr_mode(cv2, cv3, pd_read_flag=False)
        # row_data.config_sr_mode('右发', '左发', pd_read_flag=False)
        # row_data.config_sr_mode('', '', pd_read_flag=True)

        row_data.config_pop([], [], pd_read_flag=False)
        # if temp_temp == 1:
        #     row_data.config_pop([], [2,4,5], pd_read_flag=False)
        # elif temp_temp == 3:
        #     row_data.config_pop([2,4,5], [], pd_read_flag=False)

        row_data.config_cable_para()
        row_data.config_cable_length(7.5, 7.5, pd_read_flag=flag, respectively=True)
        # row_data.config_r_sht(1e-7, 1e-7, pd_read_flag=flag, respectively=True)
        row_data.config_r_sht(1e-7, 1e-7, pd_read_flag=False, respectively=True)
        row_data.config_power(2, '最大', pd_read_flag=flag)

        row_data.config_sp_posi()
        row_data.config_train_signal()
        row_data.config_error()

        # interval = row_data.config_interval(1, pd_read_flag=flag)
        interval = row_data.config_interval(5, pd_read_flag=False)

        if data['被串故障模式'] is None:
            print(para['freq_被'], para['被串故障模式'])
            continue
        data2excel.add_new_row()

        # 移频脉冲
        # row_data.config_ypmc_EL(pd_read_flag=flag)

        # 电码化
        # row_data.config_25Hz_coding_device(pd_read_flag=False)

        # len_posi = 0
        #################################################################################

        # # 调整计算
        # md = PreModel(parameter=para)
        # # md.lg = LineGroup(md.l3, name_base='线路组')
        # # md.lg.special_point = para['special_point']
        # # md.lg.refresh()
        # m1 = MainModel(md.lg, md=md)
        #
        # # data['主串轨入电压(调整状态)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # # data['被串轨入电压(调整状态)'] = md.lg['线路4']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # data['被串轨入电压(调整状态)'] = md.lg['线路4']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c
        # uca = md.lg['线路3']['地面']['区段1']['左调谐单元']['7CA']['U2'].value
        # ica = md.lg['线路3']['地面']['区段1']['左调谐单元']['7CA']['I2'].value
        # rca = uca/ica
        # rca1 = abs(uca/ica)

        # name_list = md.section_group3['区段1'].get_C_TB_names()
        # name_list.reverse()
        # for _, name in name_list:
        #     i_tb_zhu = md.lg['线路3']['地面']['区段1'][name]['I'].value_c
        #     v_tb_zhu = md.lg['线路3']['地面']['区段1'][name]['U'].value_c
        #
        #     data2excel.add_data(sheet_name="主串TB电流", data1=i_tb_zhu)
        #     data2excel.add_data(sheet_name="主串TB电压", data1=v_tb_zhu)
        #
        #     i_tb_bei = md.lg['线路4']['地面']['区段1'][name]['I'].value_c
        #     v_tb_bei = md.lg['线路4']['地面']['区段1'][name]['U'].value_c
        #     data2excel.add_data(sheet_name="被串TB电流", data1=i_tb_bei)
        #     data2excel.add_data(sheet_name="被串TB电压", data1=v_tb_bei)


        #################################################################################

        # # 轨面电压计算
        # # md = PreModel_25Hz_coding(parameter=para)
        # # md = PreModel_YPMC(parameter=para)
        # md = PreModel(parameter=para)
        # # md.lg = LineGroup(md.l3, name_base='线路组')
        # md.lg = LineGroup(md.l3, md.l4, name_base='线路组')
        # md.lg.special_point = para['special_point']
        # md.lg.refresh()
        #
        #
        # # flag_r = data['被串区段长度(m)'] - data['被串相对主串位置']
        # # flag_l = flag_r - data['主串区段长度(m)'] - 0.00001
        #
        #
        # posi_list = np.arange(data['主串区段长度(m)'], -0.00001, -interval)
        # # posi_list = np.arange(flag_r, flag_l, -interval)
        #
        # len_posi = max(len(posi_list), len_posi)
        #
        # for posi_zhu in posi_list:
        #     md.jumper.posi_rlt = posi_zhu
        #     md.jumper.set_posi_abs(0)
        #     m1 = MainModel(md.lg, md=md)
        #
        #     v_rail_zhu = md.lg['线路3']['地面']['区段1']['跳线']['U'].value_c
        #     data2excel.add_data(sheet_name="主串轨面电压", data1=v_rail_zhu)
        #
        # # 移频脉冲
        # # data['主串功出电压(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # # data['主串轨入电压(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['0接收器']['U'].value_c
        #
        # # 一体化
        # data['主串功出电压(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # data['主串轨入电压(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        #
        # data['主串TB1电流(A)'] = md.lg['线路3']['地面']['区段1']['TB1']['I'].value_c
        # data['主串TB2电流(A)'] = md.lg['线路3']['地面']['区段1']['TB2']['I'].value_c
        # data['被串TB1电流(A)'] = md.lg['线路4']['地面']['区段1']['TB1']['I'].value_c
        # data['被串TB2电流(A)'] = md.lg['线路4']['地面']['区段1']['TB2']['I'].value_c

        #################################################################################

        # data['调整轨入最大值'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # data['调整功出电压'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # data['调整接收轨入max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
        # data['调整功出电压max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['U2'].value_c
        # data['调整功出电流max(I)'] = md.lg['线路3']['地面']['区段1']['右调谐单元']['1发送器']['2内阻']['I2'].value_c
        # data['调整发送轨面max(V)'] = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['U2'].value_c
        # data['调整接收轨面max(V)'] = md.lg['线路3']['地面']['区段1']['左调谐单元'].md_list[-1]['U2'].value_c

        #################################################################################

        # 分路计算

        # md = PreModel(parameter=para)
        # md = PreModel_2000A_QJ(parameter=para)
        # md = PreModel_YPMC(parameter=para)
        # md = PreModel_EeMe(parameter=para)
        # md = PreModel_25Hz_coding(parameter=para)
        # md = PreModel_QJ_25Hz_coding(parameter=para)
        # md = PreModel_20200730(parameter=para)
        # md = PreModel_V001(parameter=para)
        md = PreModel_QJ_20201204(parameter=para)
        # md = PreModel_225Hz_coding(parameter=para)

        md.add_train()

        flag_l = para['offset_bei'] - 14.5
        # flag_r = para['被串区段长度'][0] + para['被串区段长度'][1] - para['offset_bei'] + 14.5
        flag_r = para['offset_bei'] + sum(para['被串区段长度']) + 14.5

        posi_list = np.arange(flag_l, flag_r + 0.0001, +interval)
        print('分路节点数：%s' % len(posi_list))

        # len_posi = max(len(posi_list), len_posi)
        columns_max = max(len(posi_list), columns_max)

        for posi_bei in posi_list:
            # print(posi_bei)
            para['分路位置'] = posi_bei

            md.train1.posi_rlt = posi_bei
            md.train1.set_posi_abs(0)

            # posi_zhu = posi_bei
            # md.train2.posi_rlt = posi_zhu
            # md.train2.set_posi_abs(0)

            m1 = MainModel(md.lg, md=md)

            # zm_sva = 2 * np.pi * freq * data["SVA'互感"] * 1e-6 * 1j
            #
            # # list_sva1_mutual = [(3, 4, '右'), (3, 4, '左') ,(4, 3, '右') ,(4, 3, '左')]
            # list_sva1_mutual = [(3, 4, '右')]
            # for sva1_mutual in list_sva1_mutual:
            #     config_sva1_mutual(m1, sva1_mutual, zm_sva)
            #
            # m1.equs.creat_matrix()
            # m1.equs.solve_matrix()

            # i_sht_zhu = md.lg['线路3']['列车2']['分路电阻1']['I'].value_c
            # u_trk_zhu = i_sht_zhu * 1e7
            i_sht_bei = md.lg['线路4']['列车1']['分路电阻1']['I'].value_c

            # rs = md.train2['分路电阻1'].z

            # u_ca = md.l3['地面']['区段1']['右调谐单元']['6CA'].varb_value['U2']
            # i_ca = md.l3['地面']['区段1']['右调谐单元']['6CA'].varb_value['I2']
            # r_ca = u_ca / i_ca

            # uj = m1['线路3'].node_dict[LENGTH - 14.5].r_track['U1'].value
            # ij = m1['线路3'].node_dict[LENGTH - 14.5].r_track['I1'].value
            # rj = uj / ij

            # ul = m1['线路3'].node_dict[LENGTH - 14.5].l_track['U2'].value
            # il = -m1['线路3'].node_dict[LENGTH - 14.5].l_track['I2'].value
            # rl = ul / il

            # rl2 = rj * r_ca / (rj + r_ca)

            # u_rcv_zhu = md.lg['线路3']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c
            #
            # i_pwr_tmp = md.lg['线路3']['地面']['区段1']['左调谐单元']['1发送器']['1电压源']['I'].value
            # i_pwr_zhu = np.abs(i_pwr_tmp)
            # i_pwr_angle = -np.angle(-i_pwr_tmp, deg=True)

            # i_trk_zhu = get_i_trk(line=m1['线路3'], posi=posi_zhu, direct='右')
            i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct=data['被串方向'][0])

            # if data['被串方向'] == '正向':
            #     i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')
            #     v_rcv_bei = md.lg['线路4']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
            #
            # else:
            #     i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='左')
            #     v_rcv_bei = md.lg['线路4']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

            # if data['被串方向'] == '右发':
            #     i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='右')
            # else:
            #     i_trk_bei = get_i_trk(line=m1['线路4'], posi=posi_bei, direct='左')

            # i1 = md.lg['线路3']['地面']['区段1']['右调谐单元']['6SVA1']['I1'].value
            # i2 = md.lg['线路3']['地面']['区段1']['右调谐单元']['6SVA1']['I2'].value
            #
            # i_sva1 = abs(i1 - i2)
            #
            # i_trk_bei_temp = i_trk_bei / i_sva1

            # i_source_fs = m1['线路3'].node_dict[length].l_track['I2'].value
            # i_source_fs = md.lg['线路3']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value
            # v_load_fs = m1['线路4'].node_dict[length].l_track['U2'].value

            # z_mm = np.inf if i_source_fs == 0 else v_load_fs / i_source_fs
            # z_mm = v_load_fs / i_source_fs
            # z_mm_abs = abs(z_mm)
            # co_mutal = z_mm_abs / 2 / np.pi / para['freq_主'] / (length-posi_tr)*1000 * 1e6 * 2
            # co_mutal = round(co_mutal, 2)

            # i_TB = md.lg['线路4']['地面']['区段1']['TB2']['I'].value_c
            # i_ca = md.lg['线路4']['地面']['区段1']['右调谐单元'].md_list[-1]['I2'].value_c
            # i_C1 = md.lg['线路4']['地面']['区段1']['C5']['I'].value_c
            # i_C2 = md.lg['线路4']['地面']['区段1']['C4']['I'].value_c
            # i_C3 = md.lg['线路4']['地面 ']['区段1']['C3']['I'].value_c
            # i_C4 = md.lg['线路4']['地面']['区段1']['C2']['I'].value_c
            # i_C5 = md.lg['线路4']['地面']['区段1']['C1']['I'].value_c

            # v_rcv_bei = md.lg['线路4']['地面']['区段1']['左调谐单元']['1接收器']['U'].value_c
            # v_rcv_bei = md.lg['线路4']['地面']['区段1']['右调谐单元']['1接收器']['U'].value_c

            #################################################################################

            # data2excel.add_data(sheet_name="主串钢轨电流", data1=i_trk_zhu)
            # data2excel.add_data(sheet_name="主串分路电流", data1=i_sht_zhu)
            # data2excel.add_data(sheet_name="主串轨入电压", data1=u_rcv_zhu)
            # data2excel.add_data(sheet_name="主串功出电流", data1=i_pwr_zhu)
            # data2excel.add_data(sheet_name="主串功率因数角", data1=i_pwr_angle)
            # data2excel.add_data(sheet_name="主串轨面电压", data1=u_trk_zhu)

            data2excel.add_data(sheet_name="被串钢轨电流", data1=i_trk_bei)
            data2excel.add_data(sheet_name="被串分路电流", data1=i_sht_bei)
            # data2excel.add_data(sheet_name="被串轨入电压", data1=v_rcv_bei)
            # data2excel.add_data(sheet_name="主串SVA'电流", data1=i_sva1)
            # data2excel.add_data(sheet_name="被串钢轨电流折算后", data1=i_trk_bei_temp)
            # data2excel.add_data(sheet_name="实测阻抗", data1=z_mm)
            # data2excel.add_data(sheet_name="阻抗模值", data1=z_mm_abs)
            # data2excel.add_data(sheet_name="耦合系数", data1=co_mutal)

            # data2excel.add_data(sheet_name="分路电流", data1=i_sht_zhu)
            # data2excel.add_data(sheet_name="分路功出电流", data1=i_pwr_zhu)

        # i_trk_list = data2excel.data_dict["主串分路电流"][-1]
        # # print(cv3, np.min(i_trk_list))
        #
        # tmp_list1 = data2excel.data_dict["分路功出电流"][-1]
        # tmp_list2 = data2excel.data_dict["分路时主轨入"][-1]
        # tmp_list3 = data2excel.data_dict["分路电流"][-1]
        #
        # data['分路时最大功出电流(A)'] = max(tmp_list1)
        # data['分路时最大主轨入(V)'] = max(tmp_list2)
        # data['分路时最小短路电流(A)'] = min(tmp_list3)

        i_trk_list = data2excel.data_dict["被串钢轨电流"][-1]
        # i_sht_list = data2excel.data_dict["被串分路电流"][-1]

        # i_sht_list_zhu = data2excel.data_dict["主串分路电流"][-1]

        data['被串最大干扰电流(A)'] = max(i_trk_list)
        # data['主串出口电流(A)'] = i_sht_list_zhu[0]
        # data['主串入口电流(A)'] = i_sht_list_zhu[-1]
        data['被串最大干扰位置(m)'] = round(i_trk_list.index(max(i_trk_list))*interval)
        # max_i = data['被串最大干扰电流(A)'] * 1000
        # MAX_I = para['MAX_CURRENT'][data['主串频率(Hz)']]

        # print('最大干扰电流：%.2f mA' % max_i)
        # if max_i > MAX_I:
        #     text = '干扰频率：' + str(data['主串频率(Hz)']) + 'Hz，'\
        #            + '干扰电流上限' + str(MAX_I) + 'mA；第' \
        #            + str(counter) \
        #            + '行数据干扰电流超上限：最大干扰电流为' \
        #            + str(round(max_i, 1)) \
        #            + 'mA，位于距离被串发送端' \
        #            + str(round(data['被串最大干扰位置(m)'], 0)) \
        #            + 'm处'
        #     for key in head_list:
        #         data[key] = None
        #
        #     data2excel.refresh_row()
        #
        #     # data['备注'] = text
        #     raise KeyboardInterrupt(text)

        # v_rcv_bei_list = data2excel.data_dict["被串轨入电压"][-1]
        # data['被串最大轨入电压(主被串同时分路状态)'] = max(v_rcv_bei_list)

        # v_rcv_bei_list = data2excel.data_dict["被串轨入电压"][-1]
        # data['被串最大轨入电压(主调整被调整)'] = max(v_rcv_bei_list)

        data_row = [data[key] for key in head_list]
        excel_data.append(data_row)
        counter += 1

        #################################################################################

        # if not getattr(sys, 'frozen', False):
        #     print(data.keys())
        #     print(data.values())
        #     print(i_sht_list)
        #
    #################################################################################

    # 修正表头
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    posi_header = list(range(columns_max))
    # posi_header[0] = '发送端'
    posi_header[0] = '主串发送端'
    # posi_header = None

    data2excel.config_header()
    # data2excel["被串钢轨电流"].header[0] = '被串发送端'
    # data2excel["被串分路电流"].header[0] = '被串发送端'
    # data2excel["主串钢轨电流"].header[0] = '被串发送端'
    # data2excel["主串分路电流"].header[0] = '被串发送端'
    # data2excel["主串轨面电压"].header[0] = '主串发送端'

    # # xx = np.arange(columns_max)
    # xx = posi_list
    # # # yy = np.array(data2excel.data_dict['主串分路电流'][0]) * 1000000
    # # yy = np.array(data2excel.data_dict['主串分路电流'][0])
    # #
    # # yy2 = np.ones(columns_max) * 0.5
    #
    # # fig = plt.figure(1, figsize=(24, 8), dpi=80)
    # fig = plt.figure(figsize=(21, 10), dpi=90)
    #
    # # fig_tittle = '电缆长度%skm-电平级%s级-道床电阻%sΩ·km-分路电阻%sΩ-电容%sμF-串联电阻%sΩ' \
    # #              % (CABLE_LENGTH, LEVEL, RD, R_SHT, C_CMP, DELTA_R)
    # fig_tittle = '加感%smH-电缆长度%skm-电平级%s级-道床电阻%sΩ·km-分路电阻%sΩ-电容%sμF' \
    #              % (DELTA_L, CABLE_LENGTH, LEVEL, RD, R_SHT, C_CMP)
    #
    # fig.suptitle(fig_tittle)
    # fig.subplots_adjust(hspace=0.3)
    #
    # row_num = 3
    #
    # number = 0
    # scale_tmp = [0.5, 0.5, 0.5, 0.46]
    # for row in range(4):
    #
    #     yy = np.array(data2excel.data_dict['主串分路电流'][3 * row + 1])
    #     yy2 = np.ones(columns_max) * 0.5
    #     yy3 = np.ones(columns_max) * scale_tmp[row]
    #
    #     number += 1
    #
    #     ax1 = fig.add_subplot(row_num, 4, number)
    #
    #     title = '分路电流-频率%sHz' % str(clist1[row])
    #     ax1.set_title(title)
    #     ax1.set_xlabel('label-position(m)')
    #     # ax1.set_ylabel('label-voltage')
    #     ax1.set_ylabel('label-current(A)')
    #
    #     ax1.yaxis.grid(True, which='major')
    #     ax1.set_ylim([0, 3])
    #
    #     tmp = np.min(yy) * 1000
    #     ax1.text(500, 0.55, '最小分路电流%.2fmA' % tmp, fontsize=8, va='bottom', ha='center')
    #
    #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #     ax1.plot(xx, yy2, linestyle='--', alpha=0.8, color='r', label='legend2')
    #     ax1.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label='legend2')
    #
    # # for row in range(4):
    # #
    # #     yy = np.array(data2excel.data_dict['主串轨入电压'][3 * row])
    # #     yy2 = np.ones(columns_max) * u_adjust[3 * row + 1]
    # #     yy3 = np.ones(columns_max) * u_adjust[3 * row + 1] / 240 * 153
    # #
    # #     number += 1
    # #
    # #     ax1 = fig.add_subplot(row_num, 4, number)
    # #
    # #     title = '轨入电压-频率%sHz' % str(clist1[row])
    # #     ax1.set_title(title)
    # #     ax1.set_xlabel('label-position(m)')
    # #     # ax1.set_ylabel('label-voltage')
    # #     ax1.set_ylabel('label-voltage(V)')
    # #
    # #     ax1.yaxis.grid(True, which='major')
    # #
    # #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    # #     ax1.plot(xx, yy2, linestyle='--', alpha=0.8, color='r', label='legend2')
    # #     ax1.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label='legend2')
    # #
    # # for row in range(4):
    # #
    # #     yy = np.array(data2excel.data_dict['主串轨入电压'][3 * row]) / u_adjust[3 * row + 1] * 240
    # #     yy2 = np.ones(columns_max) * 240
    # #     yy3 = np.ones(columns_max) * 153
    # #
    # #     number += 1
    # #
    # #     ax1 = fig.add_subplot(row_num, 4, number)
    # #
    # #     title = '轨出电压-频率%sHz' % str(clist1[row])
    # #     ax1.set_title(title)
    # #     ax1.set_xlabel('label-position(m)')
    # #     # ax1.set_ylabel('label-voltage')
    # #     ax1.set_ylabel('label-voltage(mV)')
    # #     ax1.set_ylim([0, 240])
    # #
    # #     ax1.yaxis.grid(True, which='major')
    # #
    # #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    # #     ax1.plot(xx, yy2, linestyle='--', alpha=0.8, color='r', label='legend2')
    # #     ax1.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label='legend2')
    # #
    # # for row in range(4):
    # #
    # #     yy = np.array(data2excel.data_dict['主串轨面电压'][3 * row + 2])
    # #     number += 1
    # #
    # #     ax1 = fig.add_subplot(row_num, 4, number)
    # #
    # #     title = '调整轨面电压-频率%sHz' % str(clist1[row])
    # #     ax1.set_title(title)
    # #     ax1.set_xlabel('label-position(m)')
    # #     ax1.set_ylabel('label-voltage(V)')
    # #
    # #     ax1.yaxis.grid(True, which='major')
    # #
    # #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #
    # for row in range(4):
    #
    #     yy = np.array(data2excel.data_dict['主串功出电流'][3 * row])
    #     number += 1
    #
    #     ax1 = fig.add_subplot(row_num, 4, number)
    #
    #     title = '分路功出电流-频率%sHz' % str(clist1[row])
    #     ax1.set_title(title)
    #     ax1.set_xlabel('label-position(m)')
    #     ax1.set_ylabel('label-current(A)')
    #
    #     ax1.yaxis.grid(True, which='major')
    #     ax1.set_ylim([0.3, 1])
    #
    #     tmp = np.max(yy) * 1000
    #     ax1.text(500, 0.35, '最大功出电流%.2fmA' % tmp, fontsize=8, va='bottom', ha='center')
    #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #
    # for row in range(4):
    #
    #     yy = np.array(data2excel.data_dict['主串功率因数角'][3 * row])
    #
    #     number += 1
    #
    #     ax1 = fig.add_subplot(row_num, 4, number)
    #
    #     title = '分路功率因数角-频率%sHz' % str(clist1[row])
    #     ax1.set_title(title)
    #     ax1.set_xlabel('label-position(m)')
    #     ax1.set_ylabel('label-degree(°)')
    #
    #     ax1.yaxis.grid(True, which='major')
    #     ax1.set_ylim([-90, 90])
    #
    #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #
    #
    # # fig.tight_layout()
    # plt.show()
    #
    # filename1 = '图表汇总/功率_%s_%s.png' % (fig_tittle, time.strftime("%Y%m%d%H%M%S", time.localtime()))
    # fig.savefig(filename1)
    #
    # ##################################################################
    #
    # fig = plt.figure(figsize=(21, 10), dpi=90)
    #
    # fig.suptitle(fig_tittle)
    # fig.subplots_adjust(hspace=0.3)
    #
    # row_num = 3
    #
    # number = 0
    #
    # for row in range(4):
    #
    #     yy = np.array(data2excel.data_dict['主串轨入电压'][3 * row])
    #     yy2 = np.ones(columns_max) * u_adjust[3 * row + 1]
    #     yy3 = np.ones(columns_max) * u_adjust[3 * row + 1] / 240 * 153
    #
    #     number += 1
    #
    #     ax1 = fig.add_subplot(row_num, 4, number)
    #
    #     title = '轨入电压-频率%sHz' % str(clist1[row])
    #     ax1.set_title(title)
    #     ax1.set_xlabel('label-position(m)')
    #     # ax1.set_ylabel('label-voltage')
    #     ax1.set_ylabel('label-voltage(V)')
    #
    #     ax1.yaxis.grid(True, which='major')
    #
    #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #     ax1.plot(xx, yy2, linestyle='--', alpha=0.8, color='r', label='legend2')
    #     ax1.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label='legend2')
    #
    # for row in range(4):
    #
    #     yy = np.array(data2excel.data_dict['主串轨入电压'][3 * row]) / u_adjust[3 * row + 1] * 240
    #     yy2 = np.ones(columns_max) * 240
    #     yy3 = np.ones(columns_max) * 153
    #
    #     number += 1
    #
    #     ax1 = fig.add_subplot(row_num, 4, number)
    #
    #     title = '轨出电压-频率%sHz' % str(clist1[row])
    #     ax1.set_title(title)
    #     ax1.set_xlabel('label-position(m)')
    #     # ax1.set_ylabel('label-voltage')
    #     ax1.set_ylabel('label-voltage(mV)')
    #     ax1.set_ylim([0, 240])
    #
    #     ax1.yaxis.grid(True, which='major')
    #
    #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #     ax1.plot(xx, yy2, linestyle='--', alpha=0.8, color='r', label='legend2')
    #     ax1.plot(xx, yy3, linestyle='--', alpha=0.8, color='r', label='legend2')
    #
    # for row in range(4):
    #
    #     yy = np.array(data2excel.data_dict['主串轨面电压'][3 * row + 2])
    #     number += 1
    #
    #     ax1 = fig.add_subplot(row_num, 4, number)
    #
    #     title = '调整轨面电压-频率%sHz' % str(clist1[row])
    #     ax1.set_title(title)
    #     ax1.set_xlabel('label-position(m)')
    #     ax1.set_ylabel('label-voltage(V)')
    #
    #     ax1.yaxis.grid(True, which='major')
    #
    #     ax1.plot(xx, yy, linestyle='-', alpha=0.8, color='r', label='legend2')
    #
    # plt.show()
    #
    # filename1 = '图表汇总/功率_%s_%s.png' % (fig_tittle, time.strftime("%Y%m%d%H%M%S", time.localtime()))
    # fig.savefig(filename1)

    df_data = pd.DataFrame(excel_data, columns=head_list)

    #################################################################################

    # 保存到本地excel
    # filename = '仿真输出'
    # filepath = 'src/Output/'+ filename + timestamp + '.xlsx'
    # filepath = ''+ filename + '_' + timestamp + '.xlsx'
    filepath = path2

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

    workbook = writer.book
    header_format = workbook.add_format({
        'bold': True,  # 字体加粗
        'text_wrap': True,  # 是否自动换行
        'valign': 'vcenter',  # 垂直对齐方式
        'align': 'center',  # 水平对齐方式
        'border': 1})

    if pd_read_flag:
        write_to_excel(df=df_input, writer=writer, sheet_name="参数设置", hfmt=header_format)
    write_to_excel(df=df_data, writer=writer, sheet_name="数据输出", hfmt=header_format)

    names = [
        "被串钢轨电流",
        "被串分路电流",
        # "主串钢轨电流",
        # "主串分路电流",
        # "主串轨面电压",
        # "主串SVA'电流",
        # "被串钢轨电流折算后",
        # "被串轨入电压",
        # "主串TB电流",
        # "被串TB电流",
        # "主串TB电压",
        # "被串TB电压",
        # "分路电流",
        # "分路功出电流",
        # "分路时主轨入",
        # "分路时小轨入",
    ]

    # data2excel.write2excel(sheet_names=names, header=None, writer1=writer)
    # data2excel.write2excel(sheet_names=names, header=posi_header, writer1=writer)
    data2excel.write2excel(sheet_names=names, writer=writer)

    writer.save()
    return 1


def write_to_excel(df, writer, sheet_name, hfmt):
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, hfmt)


def get_line_info(line1, line2):
    line1 = line1.copy()
    line2 = line2.copy()

    offset = line2[0] - line1[0]
    line1.pop(0)
    line2.pop(0)

    zhu_left = zhu_right = 0
    res = []
    for sec_zhu in line1:
        zhu_left = zhu_right
        zhu_right = zhu_left + sec_zhu[2]

        bei_list = []
        bei_offset = 0

        bei_left = bei_right = offset
        for sec_bei in line2:
            bei_left = bei_right
            bei_right = bei_left + sec_bei[2]

            if bei_right < (zhu_left - 60):
                continue

            if bei_left > (zhu_right + 60):
                continue

            if len(bei_list) == 0:
                bei_offset = bei_left - zhu_left

            bei_list.append(sec_bei)

        res.append((sec_zhu, bei_list, bei_offset))

    return res


if __name__ == '__main__':
    main_cal('邻线干扰参数输入_V002.xlsx',
             '仿真输出' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx',
             os.getcwd())
    # main(sys.argv[1], sys.argv[2], sys.argv[3])