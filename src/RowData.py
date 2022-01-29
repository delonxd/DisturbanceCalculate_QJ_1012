import pandas as pd
from src.FrequencyType import Freq
from src.ConstantType import *
from src.ImpedanceParaType import *


class RowData:
    def __init__(self, df_input, para, data, pd_read_flag):
        self.df_input = df_input
        self.para = para
        self.data = data
        self.pd_read_flag = pd_read_flag

    #################################################################################

    def read_parameters(self):
        return self.df_input, self.para, self.data

    # 序号
    def config_number(self, counter, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['序号'] = para['序号'] = df_input['序号']
        else:
            data['序号'] = para['序号'] = counter

    #################################################################################

    # 备注
    def config_remarks(self, remarks, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['备注'] = para['备注'] = df_input['备注']
        else:
            data['备注'] = para['备注'] = remarks

    #################################################################################

    # 区段名称
    def config_sec_name(self, name_zhu, name_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串区段'] = para['主串区段'] = df_input['主串区段']
            data['被串区段'] = para['被串区段'] = df_input['被串区段']
        else:
            data['主串区段'] = para['主串区段'] = name_zhu
            data['被串区段'] = para['被串区段'] = name_bei

    #################################################################################

    # 区段长度
    def config_sec_length(self, len_zhu, len_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串区段长度(m)'] = para['主串区段长度'] = df_input['主串区段长度(m)']
            data['被串区段长度(m)'] = para['被串区段长度'] = df_input['被串区段长度(m)']
        else:
            data['主串区段长度(m)'] = para['主串区段长度'] = len_zhu
            data['被串区段长度(m)'] = para['被串区段长度'] = len_bei

        # if pd_read_flag:
        #     data['被串相对主串位置'] = off_set_send = df_input['被串相对主串位置']
        # else:
        #     data['被串相对主串位置'] = off_set_send = 0
        #
        # para['offset'] = data['被串区段长度(m)'] - data['主串区段长度(m)'] - off_set_send

    #################################################################################

    # 设置偏移
    def config_offset(self, offset, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # if pd_read_flag:
        #     data['被串相对主串位置'] = off_set_send = df_input['被串相对主串位置']
        # else:
        #     data['被串相对主串位置'] = off_set_send = offset
        #
        # para['offset'] = off_set_send

        # if pd_read_flag:
        #     data['主串左端里程标'] = para['offset_zhu'] = df_input['主串左端里程标']
        #     data['被串左端里程标'] = para['offset_bei'] = df_input['被串左端里程标']
        # else:
        #     data['主串左端里程标'] = para['offset_zhu'] = offset
        #     data['被串左端里程标'] = para['offset_bei'] = offset

        if pd_read_flag:
            data['被串相对位置(m)'] = df_input['被串相对位置(m)']

            data['主串左端里程标'] = para['offset_zhu'] = 0
            data['被串左端里程标'] = para['offset_bei'] = df_input['被串相对位置(m)']
        else:
            data['主串左端里程标'] = para['offset_zhu'] = 0
            data['被串左端里程标'] = para['offset_bei'] = offset

            data['被串相对位置(m)'] = offset

    #################################################################################

    # 耦合系数
    def config_mutual_coeff(self, coeff, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            # data['线间距'] = para['线间距'] = df_input['线间距']
            data['耦合系数'] = para['耦合系数'] = df_input['耦合系数']
        else:
            data['耦合系数'] = para['耦合系数'] = coeff

    #################################################################################

    # 区段频率
    def config_freq(self, frq_zhu, frq_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串频率(Hz)'] = para['freq_主'] = freq = df_input['主串频率(Hz)']
            data['被串频率(Hz)'] = para['freq_被'] = df_input['被串频率(Hz)']
        else:
            data['主串频率(Hz)'] = para['freq_主'] = freq = frq_zhu
            data['被串频率(Hz)'] = para['freq_被'] = frq_bei

        data['freq'] = para['freq'] = Freq(freq)

    #################################################################################

    # 电容数量
    def config_c_num(self, cnum_zhu, cnum_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # data['主串电容数'] = para['主串电容数'] = get_c_num(Freq(data['主串频率']), data['区段长度'])
        # data['被串电容数'] = para['被串电容数'] = get_c_num(Freq(data['被串频率']), data['区段长度'])
        if pd_read_flag:
            data['主串电容数(含TB)'] = para['主串电容数'] = df_input['主串电容数(含TB)']
            data['被串电容数(含TB)'] = para['被串电容数'] = df_input['被串电容数(含TB)']
        else:
            data['主串电容数(含TB)'] = para['主串电容数'] = cnum_zhu
            data['被串电容数(含TB)'] = para['被串电容数'] = cnum_bei

    #################################################################################

    # 电容位置
    def config_c_posi(self, c_pst_zhu, c_pst_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串电容(不含TB)位置'] = para['主串电容位置'] = df_input['主串电容(不含TB)位置']
            data['被串电容(不含TB)位置'] = para['被串电容位置'] = df_input['主串电容(不含TB)位置']
        else:
            data['主串电容(不含TB)位置'] = para['主串电容位置'] = c_pst_zhu
            data['被串电容(不含TB)位置'] = para['被串电容位置'] = c_pst_bei

        # hlf_pst = list(np.linspace(0, 650, 15))
        # c_pst = [hlf_pst[num * 2 + 1] - 90 for num in range(7)]
        # c_pst = c_pst[1:-1]
        # data['主串电容(不含TB)位置'] = para['主串电容位置'] = c_pst
        # data['被串电容(不含TB)位置'] = para['被串电容位置'] = c_pst

        pass

    #################################################################################

    # 电容换TB
    def config_c2TB(self, change_flag):
        df_input, para, data = self.read_parameters()

        data['是否全部更换TB'] = change_flag

        if data['是否全部更换TB'] is True:
            # if data['主串频率(Hz)'] == 1700 or data['主串频率(Hz)'] == 2000:
            #     data['主串更换TB'] = para['主串更换TB'] = True
            # if data['被串频率(Hz)'] == 1700 or data['被串频率(Hz)'] == 2000:
            #     data['被串更换TB'] = para['被串更换TB'] = True

            data['主串更换TB'] = para['主串更换TB'] = True
            data['被串更换TB'] = para['被串更换TB'] = True
        else:
            data['主串更换TB'] = para['主串更换TB'] = False
            data['被串更换TB'] = para['被串更换TB'] = False

    #################################################################################

    # 电容容值
    def config_c_value(self, c_val_zhu, c_val_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串电容值(μF)'] = c_value1 = df_input['主串电容值(μF)']
            data['被串电容值(μF)'] = c_value2 = df_input['被串电容值(μF)']
        else:
            data['主串电容值(μF)'] = c_value1 = c_val_zhu
            data['被串电容值(μF)'] = c_value2 = c_val_bei

        c_value1 = c_value1 * 1e-6
        c_value2 = c_value2 * 1e-6

        para['Ccmp_z_change_zhu'].rlc_s = {
            1700: [10e-3, None, c_value1],
            2000: [10e-3, None, c_value1],
            2300: [10e-3, None, c_value1],
            2600: [10e-3, None, c_value1]}
        para['Ccmp_z_change_chuan'].rlc_s = {
            1700: [10e-3, None, c_value2],
            2000: [10e-3, None, c_value2],
            2300: [10e-3, None, c_value2],
            2600: [10e-3, None, c_value2]}

        # para['Ccmp_z_change_zhu'] = para['TB'][para['freq_主']].copy()
        # para['Ccmp_z_change_chuan'] = para['TB'][para['freq_被']].copy()

        # para['Ccmp_z_change_chuan'].rlc_s = {
        #     1700: [10e-3, 390e-6, 11.9e-6],
        #     2000: [10e-3, 390e-6, 11.9e-6],
        #     2300: [10e-3, 390e-6, 11.9e-6],
        #     2600: [10e-3, 390e-6, 11.9e-6]}

        # data['被串电容值'] = '抑制装置'
        # para['抑制装置电感短路'] = ImpedanceMultiFreq()
        # para['抑制装置电感短路'].rlc_s = {
        #     1700: [10e-3, None, 11.9e-6],
        #     2000: [10e-3, None, 11.9e-6],
        #     2300: [10e-3, None, 11.9e-6],
        #     2600: [10e-3, None, 11.9e-6]}

        # data['换电容位置'] = para['换电容位置'] = cv2
        # data['换电容位置'] = para['换电容位置'] = 0

    #################################################################################

    # 安装干扰抑制电容
    def config_c_inhibitor(self, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        pd_read_flag = False
        # if pd_read_flag:
        #     data['主串电容值(μF)'] = c_value1 = df_input['主串电容值(μF)']
        #     data['被串电容值(μF)'] = c_value2 = df_input['被串电容值(μF)']
        # else:
        #     data['主串电容值(μF)'] = c_value1 = c_val_zhu
        #     data['被串电容值(μF)'] = c_value2 = c_val_bei

        L1 = para['主串抑制电容L1'] = para['inhibitor'][para['freq_主']][0]
        C1 = para['主串抑制电容C1'] = para['inhibitor'][para['freq_主']][1]
        L2 = para['被串抑制电容L2'] = para['inhibitor'][para['freq_被']][0]
        C2 = para['被串抑制电容C2'] = para['inhibitor'][para['freq_被']][1]

        data['主串抑制电容L1(μH)'] = L1 * 1e6
        data['主串抑制电容C1(μF)'] = C1 * 1e6
        data['被串抑制电容L2(μH)'] = L2 * 1e6
        data['被串抑制电容C2(μF)'] = C2 * 1e6

        if para['freq_主'] == 1700 or para['freq_主'] == 2000:
            para['Ccmp_z_change_zhu'].rlc_s = {
                1700: [None, L1, C1],
                2000: [None, L1, C1],
                2300: [None, L1, C1],
                2600: [None, L1, C1]}
            data['主串抑制电容模式'] = 'LC串联'
        else:
            para['Ccmp_z_change_zhu'].rlc_p = {
                1700: [None, L1, C1],
                2000: [None, L1, C1],
                2300: [None, L1, C1],
                2600: [None, L1, C1]}
            data['主串抑制电容模式'] = 'LC并联'
        para['Ccmp_z_change_zhu'] = para['Ccmp_z_change_zhu'] + 10e-3

        if para['freq_被'] == 1700 or para['freq_被'] == 2000:
            para['Ccmp_z_change_chuan'].rlc_s = {
                1700: [None, L2, C2],
                2000: [None, L2, C2],
                2300: [None, L2, C2],
                2600: [None, L2, C2]}
            data['被串抑制电容模式'] = 'LC串联'
        else:
            para['Ccmp_z_change_chuan'].rlc_p = {
                1700: [None, L2, C2],
                2000: [None, L2, C2],
                2300: [None, L2, C2],
                2600: [None, L2, C2]}
            data['被串抑制电容模式'] = 'LC并联'
        para['Ccmp_z_change_chuan'] = para['Ccmp_z_change_chuan'] + 10e-3

    #################################################################################

    # 电容故障模式
    def config_c_fault_mode(self, mode_zhu_list, mode_bei_list, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        para['主串故障模式'] = mode_zhu_list
        para['被串故障模式'] = mode_bei_list

        data['主串故障模式'] = list()
        data['被串故障模式'] = list()

        for mode_zhu in mode_zhu_list:
            data['主串故障模式'].append(mode_zhu)
            if mode_zhu == '电感开路':
                if para['freq_主'] == 1700 or para['freq_主'] == 2000:
                    data['主串故障模式'] = None
                    break

        for mode_bei in mode_bei_list:
            data['被串故障模式'].append(mode_bei)
            if mode_bei == '电感开路':
                if para['freq_被'] == 1700 or para['freq_被'] == 2000:
                    data['被串故障模式'] = None
                    break

    #################################################################################

    # 电容故障位置
    def config_c_fault_num(self, fault_zhu, fault_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串故障位置'] = para['主串故障位置'] = eval(df_input['主串故障位置'][0])
            data['被串故障位置'] = para['被串故障位置'] = eval(df_input['被串故障位置'][0])
        else:
            data['主串故障位置'] = para['主串故障位置'] = fault_zhu
            data['被串故障位置'] = para['被串故障位置'] = fault_bei

    #################################################################################

    # 道床电阻
    def config_rd(self, rd_zhu, rd_bei, pd_read_flag=False, respectively=True):
        df_input, para, data = self.read_parameters()

        if respectively:
            if pd_read_flag:
                data['主串道床电阻(Ω·km)'] = df_input['主串道床电阻(Ω·km)']
                data['被串道床电阻(Ω·km)'] = df_input['被串道床电阻(Ω·km)']
            else:
                data['主串道床电阻(Ω·km)'] = rd_zhu
                data['被串道床电阻(Ω·km)'] = rd_bei

            para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
            para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])
            para['Rd'].value = rd_zhu

        else:
            data['道床电阻'] = rd_zhu
            if pd_read_flag:
                data['道床电阻(Ω·km)'] = df_input['道床电阻(Ω·km)']
                data['主串道床电阻(Ω·km)'] = data['道床电阻(Ω·km)']
                data['被串道床电阻(Ω·km)'] = data['道床电阻(Ω·km)']
            else:
                data['道床电阻(Ω·km)'] = rd_zhu
                data['主串道床电阻(Ω·km)'] = rd_zhu
                data['被串道床电阻(Ω·km)'] = rd_zhu

            para['主串道床电阻'] = Constant(data['主串道床电阻(Ω·km)'])
            para['被串道床电阻'] = Constant(data['被串道床电阻(Ω·km)'])
            para['Rd'].value = rd_zhu

    #################################################################################

    # 钢轨阻抗
    def config_trk_z(self, pd_read_flag=False, respectively=True):
        df_input, para, data = self.read_parameters()

        freq = data['主串频率(Hz)']

        if respectively:
            if pd_read_flag:
                data['主串钢轨电阻'] = df_input['主串钢轨电阻']
                data['主串钢轨电感'] = df_input['主串钢轨电感']
                data['被串钢轨电阻'] = df_input['被串钢轨电阻']
                data['被串钢轨电感'] = df_input['被串钢轨电感']

                para['主串钢轨阻抗'] = ImpedanceMultiFreq()
                para['主串钢轨阻抗'].rlc_s = \
                    {data['主串频率(Hz)']: [data['主串钢轨电阻'], data['主串钢轨电感'], None]}
                para['被串钢轨阻抗'] = ImpedanceMultiFreq()
                para['被串钢轨阻抗'].rlc_s = \
                    {data['主串频率(Hz)']: [data['被串钢轨电阻'], data['被串钢轨电感'], None]}
            else:
                data['主串钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                data['主串钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                data['被串钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                data['被串钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
                para['主串钢轨阻抗'] = para['Trk_z']
                para['被串钢轨阻抗'] = para['Trk_z']
        else:
            if pd_read_flag:
                data['钢轨电阻(Ω/km)'] = df_input['钢轨电阻(Ω/km)']
                data['钢轨电感(H/km)'] = df_input['钢轨电感(H/km)']
                para['Trk_z'].rlc_s = \
                        {freq: [data['钢轨电阻(Ω/km)'], data['钢轨电感(H/km)'], None]}
            else:
                data['钢轨电阻(Ω/km)'] = round(para['Trk_z'].rlc_s[freq][0], 10)
                data['钢轨电感(H/km)'] = round(para['Trk_z'].rlc_s[freq][1], 10)

            para['主串钢轨阻抗'] = para['Trk_z']
            para['被串钢轨阻抗'] = para['Trk_z']

        if para['主串钢轨阻抗'][freq].z == 0:
            para['主串钢轨阻抗'] = para['Trk_z']
            data['主串钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
            data['主串钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)
        if para['被串钢轨阻抗'][freq].z == 0:
            para['被串钢轨阻抗'] = para['Trk_z']
            data['被串钢轨电阻'] = round(para['Trk_z'].rlc_s[freq][0], 10)
            data['被串钢轨电感'] = round(para['Trk_z'].rlc_s[freq][1], 10)

    #################################################################################

    # TB模式
    def config_TB_mode(self, tb_mode, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # pd_read_flag = False

        if pd_read_flag:
            data['TB模式'] = flag_tb = df_input['TB模式']
        else:
            data['TB模式'] = flag_tb = tb_mode

        # if flag_tb == '双端TB':
        #     para['TB模式'] = '双'
        # elif flag_tb == '发送端单TB':
        #     para['TB模式'] = '右'
        # elif flag_tb == '接收端单TB':
        #     para['TB模式'] = '左'
        # elif flag_tb == '无TB':
        #     para['TB模式'] = '无'
        # else:
        #     raise KeyboardInterrupt('TB模式错误')

        if flag_tb == '双端TB':
            para['TB模式'] = '双'
        elif flag_tb == '右端单TB':
            para['TB模式'] = '右'
        elif flag_tb == '左端单TB':
            para['TB模式'] = '左'
        elif flag_tb == '无TB':
            para['TB模式'] = '无'
        else:
            raise KeyboardInterrupt('TB模式错误')

    #################################################################################

    # 发码方向
    def config_sr_mode(self, sr_zhu, sr_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # data['主串发送器位置'] = para['sr_mod_主'] = sr_zhu
        # data['被串发送器位置'] = para['sr_mod_被'] = sr_bei

        if pd_read_flag:
            # data['主串方向'] = flag_zhu = df_input['主串方向']
            # data['被串方向'] = flag_bei = df_input['被串方向']
            #
            # if flag_zhu == '正向':
            #     data['主串发送器位置'] = para['sr_mod_主'] = '右发'
            # elif flag_zhu == '反向':
            #     data['主串发送器位置'] = para['sr_mod_主'] = '左发'
            #
            # if flag_bei == '正向':
            #     data['被串发送器位置'] = para['sr_mod_被'] = '右发'
            # elif flag_bei == '反向':
            #     data['被串发送器位置'] = para['sr_mod_被'] = '左发'

            # data['被串发送器位置'] = para['sr_mod_被'] = '不发码'

            data['主串方向'] = para['sr_mod_主'] = df_input['主串方向']
            data['被串方向'] = para['sr_mod_被'] = df_input['被串方向']

        else:
            data['主串方向'] = para['sr_mod_主'] = sr_zhu
            data['被串方向'] = para['sr_mod_被'] = sr_bei

        # # 发码方向
        # if pd_read_flag:
        #     data['发码继电器状态'] = df_input['发码继电器状态'][temp_temp]
        # else:
        #     # data['发码继电器状态'] = 1
        #     data['发码继电器状态'] = 0
        #
        # if data['发码继电器状态'] == 1:
        #     data['被串发送器位置'] = para['sr_mod_被'] = '不发码'
        # elif data['发码继电器状态'] == 0:
        #     data['被串发送器位置'] = para['sr_mod_被'] = '右发'

    #################################################################################

    # 设备拆卸情况
    def config_pop(self, pop_zhu, pop_bei, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串拆卸情况'] = para['主串拆卸情况'] = eval(df_input['主串拆卸情况'][0])
            data['被串拆卸情况'] = para['被串拆卸情况'] = eval(df_input['被串拆卸情况'][0])
        else:
            data['主串拆卸情况'] = para['主串拆卸情况'] = pop_zhu
            data['被串拆卸情况'] = para['被串拆卸情况'] = pop_bei

            data['主串电容断线'] = data['主串拆卸情况']
            data['被串电容断线'] = data['被串拆卸情况']

    #################################################################################

    # 电缆参数
    def config_cable_para(self):
        df_input, para, data = self.read_parameters()

        data['电缆电阻最大(Ω/km)'] = 45
        data['电缆电阻最小(Ω/km)'] = 43
        # data['电缆电容最大(F/km)'] = 30e-9
        # data['电缆电容最小(F/km)'] = 26e-9
        data['电缆电容最大(F/km)'] = 28e-9
        data['电缆电容最小(F/km)'] = 28e-9

        para['Cable_R'].value = data['电缆电阻最小(Ω/km)']
        para['Cable_C'].value = data['电缆电容最大(F/km)']

    #################################################################################

    # 电缆长度
    def config_cable_length(self, len_zhu, len_bei, pd_read_flag=False, respectively=True):
        df_input, para, data = self.read_parameters()

        if respectively:
            para['cab_len'] = len_zhu
            if pd_read_flag:
                data['主串电缆长度(km)'] = para['主串电缆长度'] = df_input['主串电缆长度(km)']
                data['被串电缆长度(km)'] = para['被串电缆长度'] = df_input['被串电缆长度(km)']
            else:
                data['主串电缆长度(km)'] = para['主串电缆长度'] = len_zhu
                data['被串电缆长度(km)'] = para['被串电缆长度'] = len_bei
        else:
            if pd_read_flag:
                data['电缆长度(km)'] = para['cab_len'] = df_input['电缆长度(km)']
            else:
                data['电缆长度(km)'] = para['cab_len'] = len_zhu

    #################################################################################

    # 分路电阻
    def config_r_sht(self, r_zhu, r_bei, pd_read_flag=False, respectively=True):
        df_input, para, data = self.read_parameters()

        if respectively:
            # para['Rsht_z'] = 0.0000001
            if pd_read_flag:
                data['主串分路电阻(Ω)'] = para['主串分路电阻'] = df_input['主串分路电阻(Ω)']
                data['被串分路电阻(Ω)'] = para['被串分路电阻'] = df_input['被串分路电阻(Ω)']
            else:
                data['主串分路电阻(Ω)'] = para['主串分路电阻'] = r_zhu
                data['被串分路电阻(Ω)'] = para['被串分路电阻'] = r_bei

                if r_zhu == r_bei:
                    para['Rsht_z'] = r_zhu
                else:
                    raise KeyboardInterrupt('主被串分路电阻不同')
        else:
            if pd_read_flag:
                data['分路电阻(Ω)'] = para['Rsht_z'] = df_input['分路电阻(Ω)']
            else:
                data['分路电阻(Ω)'] = para['Rsht_z'] = r_zhu

    #################################################################################

    # 功出电源
    def config_power(self, send_level, v_power, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['主串电平级'] = para['send_level'] = df_input['主串电平级']
        else:
            data['主串电平级'] = para['send_level'] = send_level

        if pd_read_flag:
            # data['电源电压'] = para['pwr_v_flg'] = df_input['电源电压']
            data['电源电压'] = para['pwr_v_flg'] = '最大'
        else:
            data['电源电压'] = para['pwr_v_flg'] = v_power

    #################################################################################

    # 分路间隔
    def config_interval(self, interval, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        if pd_read_flag:
            data['分路间隔(m)'] = df_input['分路间隔(m)']
        else:
            data['分路间隔(m)'] = interval

        return data['分路间隔(m)']

    #################################################################################

    # 特殊位置
    def config_sp_posi(self):
        df_input, para, data = self.read_parameters()

        # 极性交叉位置
        data['极性交叉位置'] = para['极性交叉位置'] = []

        # data['特殊位置'] = para['special_point'] = list(np.linspace(0,length + length, 21))
        data['特殊位置'] = para['special_point'] = data['极性交叉位置']

        data['节点选取模式'] = para['节点选取模式'] = '特殊'

    #################################################################################

    # 机车信号
    def config_train_signal(self):
        df_input, para, data = self.read_parameters()

        data['最小机车信号位置'] = '-'

        data['机车信号感应系数'] = \
            str(para['机车信号比例V']) + '/' + str(para['机车信号比例I'][para['freq_主']])
        para['机车信号系数值'] = para['机车信号比例V'] / para['机车信号比例I'][para['freq_主']]

    #################################################################################

    # 开短路故障
    def config_error(self):
        df_input, para, data = self.read_parameters()

        data['故障情况'] = para['故障情况'] = '正常'

    #################################################################################

    # 25Hz电码化参数
    def config_25Hz_coding_device(self, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # # 发码方向
        # if pd_read_flag:
        #     data['发码继电器状态'] = df_input['发码继电器状态']
        # else:
        #     # data['发码继电器状态'] = 1
        #     data['发码继电器状态'] = 0
        #
        # if data['发码继电器状态'] == 1:
        #     data['被串发送器位置'] = para['sr_mod_被'] = '不发码'
        # elif data['发码继电器状态'] == 0:
        #     data['被串发送器位置'] = para['sr_mod_被'] = '右发'

        #################################################################################

        # FT1-U参数
        if pd_read_flag:
            # data['FT1-U短路阻抗-Rs(Ω)'] = value_r1 = df_input['FT1-U短路阻抗-Rs(Ω)'][temp_temp]
            # data['FT1-U短路阻抗-Ls(mH)'] = value_l1 = df_input['FT1-U短路阻抗-Ls(mH)'][temp_temp]
            # data['FT1-U开路阻抗-Rs(Ω)'] = value_r2 = df_input['FT1-U开路阻抗-Rs(Ω)'][temp_temp]
            # data['FT1-U开路阻抗-Ls(H)'] = value_l2 = df_input['FT1-U开路阻抗-Ls(H)'][temp_temp]
            #
            # value_l1 = value_l1 * 1e-3
            # para['zm_FT1u_25Hz_Coding'].rlc_s = {
            #     1700: [value_r2, value_l2, None],
            #     2000: [value_r2, value_l2, None],
            #     2300: [value_r2, value_l2, None],
            #     2600: [value_r2, value_l2, None]}
            #
            # para['zs_FT1u_25Hz_Coding'].rlc_s = {
            #     1700: [value_r1, value_l1, None],
            #     2000: [value_r1, value_l1, None],
            #     2300: [value_r1, value_l1, None],
            #     2600: [value_r1, value_l1, None]}

            n2_FT1u = df_input['FT1-U二次侧输出电压(V)']
        else:
            n2_FT1u = 40

        value_n = 170 / n2_FT1u
        para['n_FT1u_25Hz_Coding'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}

        #################################################################################

        # 设备参数
        if pd_read_flag:
            data['调整电阻(Ω)'] = Rt = df_input['调整电阻(Ω)']
            data['调整电感(H)'] = Lt = df_input['调整电感(H)']
            data['调整电容(F)'] = Ct = df_input['调整电容(F)']
            data['调整RLC模式'] = mode_rlc = df_input['调整RLC模式']
        else:
            data['调整电阻(Ω)'] = Rt = 50
            data['调整电感(H)'] = Lt = None
            data['调整电容(F)'] = Ct = None
            data['调整RLC模式'] = mode_rlc = '串联'

        if mode_rlc == '串联':
            para['Rt_25Hz_Coding'].rlc_s = {
                1700: [Rt, Lt, Ct],
                2000: [Rt, Lt, Ct],
                2300: [Rt, Lt, Ct],
                2600: [Rt, Lt, Ct]}
        elif mode_rlc == '并联':
            para['Rt_25Hz_Coding'].rlc_p = {
                1700: [Rt, Lt, Ct],
                2000: [Rt, Lt, Ct],
                2300: [Rt, Lt, Ct],
                2600: [Rt, Lt, Ct]}

        #################################################################################

        # 室内隔离盒
        if pd_read_flag:
            data['NGL-C1(μF)'] = value_c = df_input['NGL-C1(μF)']
        else:
            data['NGL-C1(μF)'] = value_c = 1

        value_c = value_c * 1e-6
        para['C1_NGL_25Hz_Coding'].rlc_s = {
            1700: [None, None, value_c],
            2000: [None, None, value_c],
            2300: [None, None, value_c],
            2600: [None, None, value_c]}

        #################################################################################

        # 室外隔离盒
        if pd_read_flag:
            data['WGL-C1(μF)'] = value_c1 = df_input['WGL-C1(μF)']
            data['WGL-C2(μF)'] = value_c2 = df_input['WGL-C2(μF)']
            data['WGL-L1-R(Ω)'] = value_r1 = df_input['WGL-L1-R(Ω)']
            data['WGL-L1-L(H)'] = value_l1 = df_input['WGL-L1-L(H)']
            data['WGL-L2-R(Ω)'] = value_r2 = df_input['WGL-L2-R(Ω)']
            data['WGL-L2-L(mH)'] = value_l2 = df_input['WGL-L2-L(mH)']
            data['WGL-BPM变比'] = value_n = df_input['WGL-BPM变比']
        else:
            data['WGL-C1(μF)'] = value_c1 = 1
            data['WGL-C2(μF)'] = value_c2 = 20
            data['WGL-L1-R(Ω)'] = value_r1 = None
            data['WGL-L1-L(H)'] = value_l1 = 0.5
            data['WGL-L2-R(Ω)'] = value_r2 = None
            data['WGL-L2-L(mH)'] = value_l2 = 5
            data['WGL-BPM变比'] = value_n = 4

        value_c1 = value_c1 * 1e-6
        value_c2 = value_c2 * 1e-6
        value_l2 = value_l2 * 1e-3

        para['C1_WGL_25Hz_Coding'].rlc_s = {
            1700: [None, None, value_c1],
            2000: [None, None, value_c1],
            2300: [None, None, value_c1],
            2600: [None, None, value_c1]}

        para['C2_WGL_25Hz_Coding'].rlc_s = {
            1700: [None, None, value_c2],
            2000: [None, None, value_c2],
            2300: [None, None, value_c2],
            2600: [None, None, value_c2]}

        para['L1_WGL_25Hz_Coding'].rlc_s = {
            1700: [value_r1, value_l1, None],
            2000: [value_r1, value_l1, None],
            2300: [value_r1, value_l1, None],
            2600: [value_r1, value_l1, None]}

        para['L2_WGL_25Hz_Coding'].rlc_s = {
            1700: [value_r2, value_l2, None],
            2000: [value_r2, value_l2, None],
            2300: [value_r2, value_l2, None],
            2600: [value_r2, value_l2, None]}

        para['n_WGL_25Hz_Coding'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}

        #################################################################################

        # 扼流变压器
        if pd_read_flag:
            data['扼流变压器变比'] = value_n = df_input['扼流变压器变比']
            data['BE-Rm(Ω)'] = value_r = df_input['BE-Rm(Ω)']
            data['BE-Lm(H)'] = value_l = df_input['BE-Lm(H)']
        else:
            data['扼流变压器变比'] = value_n = 3
            data['BE-Rm(Ω)'] = value_r = 110
            data['BE-Lm(H)'] = value_l = 0.024

        para['n_EL_25Hz_Coding'] = {
            1700: value_n,
            2000: value_n,
            2300: value_n,
            2600: value_n}

        para['zm_EL_25Hz_Coding'].rlc_s = {
            1700: [value_r, value_l, None],
            2000: [value_r, value_l, None],
            2300: [value_r, value_l, None],
            2600: [value_r, value_l, None]}

    #################################################################################

    # 配置移频脉冲参数
    def config_ypmc_EL(self, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # 设置变比
        if pd_read_flag:
            data['主串扼流变压器变比'] = value_n = df_input['主串扼流变压器变比']
            para['主串扼流变比'] = {
                1700: value_n,
                2000: value_n,
                2300: value_n,
                2600: value_n}

            data['被串扼流变压器变比'] = value_n = df_input['被串扼流变压器变比']
            para['被串扼流变比'] = {
                1700: value_n,
                2000: value_n,
                2300: value_n,
                2600: value_n}
        else:
            data['主串扼流变压器变比'] = para['主串扼流变比'] = None
            data['被串扼流变压器变比'] = para['被串扼流变比'] = None

    #################################################################################

    # 配置优化扼流变比
    def config_optimize_EL(self, pd_read_flag=False):
        df_input, para, data = self.read_parameters()

        # 设置变比
        if pd_read_flag:

            para['优化扼流变比'] = tmp_n = df_input['扼流变比']

            tmp1 = tmp_n * tmp_n / 100

            para['Op_0809_z1'] = ImpedanceMultiFreq()
            para['Op_0809_z1'].rlc_s = {
                1700: [3.252607, 0.002579, None],
                2000: [3.52039, 0.002562, None],
                2300: [3.7859, 0.002548, None],
                2600: [4.05009, 0.002537, None]}

            para['Op_0809_z1'] = para['Op_0809_z1'] * tmp1

            para['Op_0809_z2'] = ImpedanceMultiFreq()
            para['Op_0809_z2'].rlc_s = {
                1700: [1.513, 0.001322, None],
                2000: [2.0234, 0.001314, None],
                2300: [2.591654, 0.001305, None],
                2600: [3.221816, 0.001296, None]}

            para['Op_0809_z2'] = para['Op_0809_z2'] * tmp1 * 100

            para['Op_0809_n'] = {
                1700: tmp_n,
                2000: tmp_n,
                2300: tmp_n,
                2600: tmp_n}

            data['扼流变比'] = tmp_n
        else:
            data['扼流变比'] = '默认'


    #################################################################################