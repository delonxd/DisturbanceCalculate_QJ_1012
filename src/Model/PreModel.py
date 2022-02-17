from src.TrackCircuitElement.SectionGroup import *
from src.TrackCircuitElement.Train import *
from src.TrackCircuitElement.Line import *
from src.TrackCircuitElement.LineGroup import *
from src.Model.MainModel import *
from src.Model.ModelParameter import *
from src.FrequencyType import Freq
from src.Method import *


class PreModel:
    def __init__(self, parameter):
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train3 = Train(name_base='列车3', posi=0, parameter=parameter)
        # self.train4 = Train(name_base='列车4', posi=0, parameter=parameter)

        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)

        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']]*3,
                           j_lens=[0]*4,
                           # m_typs=['2000A_BPLN']*3,
                           m_typs=['2000A']*3,
                           c_nums=[para['主串电容数']]*3,
                           sr_mods=[para['sr_mod_主']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)
        # sg3['区段1']['左调谐单元'].set_power_voltage()

        m_frqs = generate_frqs(Freq(para['freq_被']), 3)

        sg4 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']]*3,
                           j_lens=[0]*4,
                           # m_typs=['2000A_BPLN']*3,
                           m_typs=['2000A']*3,
                           c_nums=[para['被串电容数']]*3,
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        partent = sg3['区段1']
        ele = JumperWire(parent_ins=partent,
                         name_base='跳线',
                         posi=para['主串区段长度'])
        partent.add_child('跳线', ele)
        ele.set_posi_abs(0)
        self.jumper = ele

        # partent = sg3['区段2']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=0)
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # jumper2 = ele

        # config_jumpergroup(jumper1, jumper2)


        self.section_group3 = sg3
        self.section_group4 = sg4

        # self.check_C2TB()
        self.change_c_value()
        self.pop_c()
        # self.config_c_posi()
        self.config_c_fault()
        # self.check_fault()

        self.change_cable_length()
        self.change_r_shunt()

        # sg3['区段1'].element.pop('TB2')
        # sg3['区段1'].element.pop('左调谐单元')
        # sg3['区段1']['TB2'].z = para['标准开路阻抗']

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

        pass

    def check_C2TB(self):
        para = self.parameter

        if para['主串更换TB'] is True:
            self.section_group3['区段1'].change_CapC2TB()

        if para['被串更换TB'] is True:
            self.section_group4['区段1'].change_CapC2TB()


    def change_c_value(self):
        para = self.parameter

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']

        # cv = para['换电容位置']
        # str_temp = 'C' + str(cv)
        # self.section_group3['区段1'][str_temp].z = para['Ccmp_z_change_zhu']
        # self.section_group4['区段1'][str_temp].z = para['Ccmp_z_change_chuan']


    def pop_c(self):
        para = self.parameter
        name_list = self.section_group3['区段1'].get_C_TB_names()

        for temp in para['主串拆卸情况']:
            str_temp = name_list[-temp][1]
            self.section_group3['区段1'].element.pop(str_temp)

        name_list = self.section_group4['区段1'].get_C_TB_names()
        for temp in para['被串拆卸情况']:
            str_temp = name_list[-temp][1]
            self.section_group4['区段1'].element.pop(str_temp)

        # for temp in para['主串拆卸情况']:
        #     str_temp = 'C' + str(temp)
        #     self.section_group3['区段1'].element.pop(str_temp)
        #
        # for temp in para['被串拆卸情况']:
        #     str_temp = 'C' + str(temp)
        #     # self.section_group4['区段1'][str_temp].z = para['抑制装置电感短路']
        #
        #     self.section_group4['区段1'].element.pop(str_temp)

    def config_c_posi(self):
        para = self.parameter

        if para['主串电容位置'] is not None:
            name_list = self.section_group3['区段1'].get_C_names()
            for name_ele, temp in zip(name_list, para['主串电容位置']):
                self.section_group3['区段1'][name_ele[1]].posi_rlt = temp

        if para['被串电容位置'] is not None:
            name_list = self.section_group4['区段1'].get_C_names()
            for name_ele, temp in zip(name_list, para['被串电容位置']):
                self.section_group4['区段1'][name_ele[1]].posi_rlt = temp

        self.section_group3.set_posi_abs(0)
        self.section_group4.set_posi_abs(0)

    def config_c_fault(self):
        para = self.parameter
        sec = self.section_group4['区段1']
        name_list = sec.get_C_TB_names()
        # for temp in para['被串故障位置']:
        #     str_temp = name_list[-temp][1]
        #     ele = sec[str_temp]
        #     ele_c = para['inhibitor'][para['freq_被']][1]
        #
        #     if para['被串故障模式'] == '全开路':
        #         sec.element.pop(str_temp)
        #     elif para['被串故障模式'] == '电感故障':
        #         para_temp = ImpedanceMultiFreq()
        #         para_temp.rlc_s = {
        #             1700: [10e-3, None, ele_c],
        #             2000: [10e-3, None, ele_c],
        #             2300: [10e-3, None, ele_c],
        #             2600: [10e-3, None, ele_c]}
        #         ele.z = para_temp
        #     elif para['被串故障模式'] == '无':
        #         pass

        for pst, mode in zip(para['被串故障位置'], para['被串故障模式']):
            str_temp = name_list[-pst][1]
            ele = sec[str_temp]

            if mode == '全开路':
                sec.element.pop(str_temp)
            elif mode == '电感短路':
                ele_c = para['TB_电感短路'][para['freq_被']]
                para_temp = ImpedanceMultiFreq()
                para_temp.rlc_s = {
                    1700: [10e-3, None, ele_c],
                    2000: [10e-3, None, ele_c],
                    2300: [10e-3, None, ele_c],
                    2600: [10e-3, None, ele_c]}
                ele.z = para_temp
            elif mode == '电感开路':
                ele_c = para['TB_电感开路'][para['freq_被']]
                para_temp = ImpedanceMultiFreq()
                para_temp.rlc_s = {
                    1700: [10e-3, None, ele_c],
                    2000: [10e-3, None, ele_c],
                    2300: [10e-3, None, ele_c],
                    2600: [10e-3, None, ele_c]}
                ele.z = para_temp
            elif para['被串故障模式'] == '无':
                pass


        # sec = self.section_group3['区段1']
        # name_list = sec.get_C_TB_names()
        # for temp in para['主串故障位置']:
        #     str_temp = name_list[-temp][1]
        #     ele = sec[str_temp]
        #     ele_c = para['inhibitor'][para['freq_主']][1]
        #
        #     if para['主串故障模式'] == '全开路':
        #         sec.element.pop(str_temp)
        #     elif para['主串故障模式'] == '电感故障':
        #         para_temp = ImpedanceMultiFreq()
        #         para_temp.rlc_s = {
        #             1700: [10e-3, None, ele_c],
        #             2000: [10e-3, None, ele_c],
        #             2300: [10e-3, None, ele_c],
        #             2600: [10e-3, None, ele_c]}
        #         ele.z = para_temp
        #     elif para['主串故障模式'] == '无':
        #         pass



    def change_cable_length(self):
        para = self.parameter

        if para['主串电缆长度'] is not None:
            for ele in self.section_group3['区段1'].element.values():
                if isinstance(ele, ZPW2000A_ZN_PTSVA1):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']
                elif isinstance(ele, ZPW2000A_Optimize_0809):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']


        if para['被串电缆长度'] is not None:
            for ele in self.section_group4['区段1'].element.values():
                if isinstance(ele, ZPW2000A_ZN_PTSVA1):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['被串电缆长度']
                elif isinstance(ele, ZPW2000A_Optimize_0809):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']


    def change_r_shunt(self):
        para = self.parameter

        if para['主串分路电阻'] is not None:
            self.train2['分路电阻1'].z = para['主串分路电阻']

        if para['被串分路电阻'] is not None:
            self.train1['分路电阻1'].z = para['被串分路电阻']


    def check_fault(self):
        para = self.parameter
        sg3 = self.section_group3
        sg4 = self.section_group4

        if para['故障情况'] == '主串PT开路':
            sg3['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']
        elif para['故障情况'] == '被串PT开路':
            sg4['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主被串PT开路':
            sg3['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']
            sg4['区段1']['右调谐单元']['5PT_CA'].z = para['标准开路阻抗']

        elif para['故障情况'] == '主串PT短路':
            sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准短路阻抗']}
        elif para['故障情况'] == '被串PT短路':
            sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准短路阻抗']}
        elif para['故障情况'] == '主被串PT短路':
            sg3['区段1']['右调谐单元']['5BA'].z = {2600: para['标准短路阻抗']}
            sg4['区段1']['右调谐单元']['5BA'].z = {2000: para['标准短路阻抗']}

        elif para['故障情况'] == '主串SVA1开路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        elif para['故障情况'] == '被串SVA1开路':
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主被串SVA1开路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主串SVA1短路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']
        elif para['故障情况'] == '被串SVA1短路':
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']
        elif para['故障情况'] == '主被串SVA1短路':
            sg3['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']
            sg4['区段1']['右调谐单元']['6SVA1'].z = para['标准短路阻抗']

        elif para['故障情况'] == '主串TB开路':
            sg3['区段1']['TB2'].z = para['标准开路阻抗']
        elif para['故障情况'] == '被串TB开路':
            sg4['区段1']['TB2'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主被串TB开路':
            sg3['区段1']['TB2'].z = para['标准开路阻抗']
            sg4['区段1']['TB2'].z = para['标准开路阻抗']
        elif para['故障情况'] == '主串TB短路':
            sg3['区段1']['TB2'].z = para['标准短路阻抗']
        elif para['故障情况'] == '被串TB短路':
            sg4['区段1']['TB2'].z = para['标准短路阻抗']
        elif para['故障情况'] == '主被串TB短路':
            sg3['区段1']['TB2'].z = para['标准短路阻抗']
            sg4['区段1']['TB2'].z = para['标准短路阻抗']

    @staticmethod
    def set_rail_para(line, z_trk, rd):
        rail = line.rail_group.rail_list[0]
        rail.ztrk, rail.rd = z_trk, rd

    def add_train(self):
        para = self.parameter
        # l3 = Line(name_base='线路3', sec_group=self.section_group3,
        #           parameter=self.parameter, train=[self.train2])
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter)
        self.l3 = l3

        l4 = Line(name_base='线路4', sec_group=self.section_group4,
                  parameter=self.parameter, train=[self.train1])
        self.l4 = l4

        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()


class PreModelAdjust(PreModel):
    def __init__(self, parameter):
        super().__init__(parameter)
        self.parameter = para = parameter

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)

        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['length']] * 3,
                           j_lens=[0] * 4,
                           m_typs=['2000A'] * 3,
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']] * 3,
                           send_lvs=[send_level] * 3,
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        self.section_group3 = sg3

        self.change_c_value()
        self.pop_c()
        self.check_fault()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])

        self.lg = LineGroup(l3, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def add_train(self):
        para = self.parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=para)

        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train1])
        self.l3 = l3
        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])

        self.lg = LineGroup(self.l3, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()


class PreModel_25Hz_coding(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)

        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']]*3,
                           j_lens=[0]*4,
                           m_typs=['2000A_25Hz_Coding']*3,
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 3)
        sg4 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']]*3,
                           j_lens=[0]*4,
                           m_typs=['2000A_25Hz_Coding']*3,
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        # sg3['区段1'].element.pop('左调谐单元')
        # sg3['区段1'].element.pop('右调谐单元')
        # sg4['区段1'].element.pop('左调谐单元')
        # sg4['区段1'].element.pop('右调谐单元')

        # partent = sg3['区段1']
        # ele = ZPW2000A_ZN_25Hz_Coding(parent_ins=partent,
        #                               name_base='25Hz叠加电码化发送器',
        #                               posi_flag='右',)
        # partent.add_child('25Hz叠加电码化发送器', ele)
        # ele.set_posi_abs(0)
        #
        # ele = ZOutside(parent_ins=partent,
        #                name_base='接收端阻抗',
        #                posi=0,
        #                z=para['z_EL_25Hz'])
        # partent.add_child('接收端阻抗', ele)
        # ele.set_posi_abs(0)
        #
        # partent = sg4['区段1']
        # ele = ZOutside(parent_ins=partent,
        #                name_base='接收端阻抗',
        #                posi=0,
        #                z=para['z_EL_25Hz'])
        # partent.add_child('接收端阻抗', ele)
        # ele.set_posi_abs(0)
        #
        # ele = ZOutside(parent_ins=partent,
        #                name_base='发送端阻抗',
        #                posi=para['被串区段长度'],
        #                z=para['z_EL_25Hz'])
        # partent.add_child('发送端阻抗', ele)
        # ele.set_posi_abs(0)


        # for ttt in [1,3,5,7,9,11]:
        # for ttt in [2,4,6,8,10]:
        #     str_temp = 'C' + str(ttt)
        #     sg3['区段1'].element.pop(str_temp)
        #     sg4['区段1'].element.pop(str_temp)

        partent = sg3['区段1']
        ele = JumperWire(parent_ins=partent,
                         name_base='跳线',
                         posi=para['主串区段长度'])
        partent.add_child('跳线', ele)
        ele.set_posi_abs(0)
        self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.pop_c()


        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()



class PreModel_EeMe(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)

        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)

        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[29, 0],
                           m_typs=['2000A'],
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 1)

        sg4 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           j_lens=[29, 0],
                           m_typs=['2000A'],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.pop_c()
        self.check_fault()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()


class PreModel_YPMC(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)

        sg3 = SectionGroup(name_base='地面', posi=para['offset'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']]*3,
                           j_lens=[0]*4,
                           m_typs=['2000A_YPMC']*3,
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 3)
        sg4 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']]*3,
                           j_lens=[0]*4,
                           m_typs=['2000A_YPMC']*3,
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)


        partent = sg3['区段1']
        ele = JumperWire(parent_ins=partent,
                         name_base='跳线',
                         posi=para['主串区段长度'])
        partent.add_child('跳线', ele)
        ele.set_posi_abs(0)
        self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        # self.pop_c()

        self.change_EL_n()
        self.change_cable_length()
        self.change_r_shunt()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_EL_n(self):
        para = self.parameter

        if para['主串扼流变比'] is not None:
            for ele in self.section_group3['区段1'].element.values():
                if isinstance(ele, ZPW2000A_YPMC_Normal):
                    ele_EL = ele['4扼流']['3变压器']
                    ele_EL.n = para['主串扼流变比']

        if para['被串扼流变比'] is not None:
            for ele in self.section_group4['区段1'].element.values():
                if isinstance(ele, ZPW2000A_YPMC_Normal):
                    ele_EL = ele['4扼流']['3变压器']
                    ele_EL.n = para['被串扼流变比']

    def change_cable_length(self):
        para = self.parameter

        if para['主串电缆长度'] is not None:
            for ele in self.section_group3['区段1'].element.values():
                if isinstance(ele, ZPW2000A_YPMC_Normal):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']

        if para['被串电缆长度'] is not None:
            for ele in self.section_group4['区段1'].element.values():
                if isinstance(ele, ZPW2000A_YPMC_Normal):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['被串电缆长度']

    def change_r_shunt(self):
        para = self.parameter

        if para['主串分路电阻'] is not None:
            self.train2['分路电阻1'].z = para['主串分路电阻']

        if para['被串分路电阻'] is not None:
            self.train1['分路电阻1'].z = para['被串分路电阻']


class PreModel_2000A_QJ(PreModel):
    def __init__(self, parameter):
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train3 = Train(name_base='列车3', posi=0, parameter=parameter)
        # self.train4 = Train(name_base='列车4', posi=0, parameter=parameter)

        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 3)
        m_lens = [para['主串区段长度']] * 3
        c_nums = get_c_nums(m_frqs, m_lens)
        offset = para['offset'] + m_lens[0]

        sg3 = SectionGroup(name_base='地面', posi=offset, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[29]*4,
                           m_typs=['2000A']*3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_主']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)
        # sg3['区段1']['左调谐单元'].set_power_voltage()

        m_frqs = generate_frqs(Freq(para['freq_被']), 3, flip_flag=True)
        m_lens = [para['被串区段长度']] * 3
        c_nums = get_c_nums(m_frqs, m_lens)

        sg4 = SectionGroup(name_base='地面', posi=0, m_num=3,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[29]*4,
                           m_typs=['2000A']*3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_被']]*3,
                           send_lvs=[send_level]*3,
                           parameter=parameter)

        partent = sg3['区段1']
        ele = JumperWire(parent_ins=partent,
                         name_base='跳线',
                         posi=para['主串区段长度'])
        partent.add_child('跳线', ele)
        ele.set_posi_abs(0)
        self.jumper = ele

        # partent = sg3['区段2']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=0)
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # jumper2 = ele

        # config_jumpergroup(jumper1, jumper2)


        self.section_group3 = sg3
        self.section_group4 = sg4

        # self.check_C2TB()
        # self.change_c_value()
        # self.pop_c()
        # self.config_c_posi()
        # self.check_fault()

        # self.change_cable_length()
        # self.change_r_shunt()

        # sg3['区段1'].element.pop('TB2')
        # sg3['区段1'].element.pop('左调谐单元')
        # sg3['区段1']['TB2'].z = para['标准开路阻抗']

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

        pass

    def add_train_bei(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter)
        self.l3 = l3

        l4 = Line(name_base='线路4', sec_group=self.section_group4,
                  parameter=self.parameter, train=[self.train1])
        self.l4 = l4

        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()


class PreModel_QJ_25Hz_coding(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[29, 0],
                           m_typs=['2000A'],
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 1)
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           # j_lens=[0, 0],
                           # m_typs=['2000A_25Hz_Coding'],
                           j_lens=[29, 29],
                           m_typs=['2000A'],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # m_frqs = generate_frqs(Freq(para['freq_被']), 2)
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=2,
        #                    m_frqs=m_frqs,
        #                    m_lens=[560, 830],
        #                    j_lens=[29, 29, 29],
        #                    m_typs=['2000A']*2,
        #                    c_nums=[6, 9],
        #                    sr_mods=[para['sr_mod_被']]*2,
        #                    send_lvs=[send_level]*2,
        #                    parameter=parameter)

        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        # self.pop_c()


        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['Trk_z'], rd=para['Trk_z'])
        self.set_rail_para(line=l4,z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']

        # for ele in self.section_group4['区段2'].element.values():
        #     if isinstance(ele, CapC):
        #         ele.z = para['Ccmp_z_change_chuan']


class PreModel_20200730(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[0, 0],
                           m_typs=['2000A'],
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 1)
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           # j_lens=[0, 0],
                           # m_typs=['2000A_25Hz_Coding'],
                           j_lens=[0, 0],
                           m_typs=['2000A'],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # m_frqs = generate_frqs(Freq(para['freq_被']), 2)
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=2,
        #                    m_frqs=m_frqs,
        #                    m_lens=[560, 830],
        #                    j_lens=[29, 29, 29],
        #                    m_typs=['2000A']*2,
        #                    c_nums=[6, 9],
        #                    sr_mods=[para['sr_mod_被']]*2,
        #                    send_lvs=[send_level]*2,
        #                    parameter=parameter)

        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        # self.pop_c()


        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['Trk_z'], rd=para['Trk_z'])
        self.set_rail_para(line=l4,z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']


class PreModel_V001(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)

        sg3 = SectionGroup(name_base='地面', posi=para['offset_zhu'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['主串区段长度']],
                           j_lens=[0, 0],
                           m_typs=['2000A'],
                           c_nums=[para['主串电容数']],
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        m_frqs = generate_frqs(Freq(para['freq_被']), 1)
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
                           m_frqs=m_frqs,
                           m_lens=[para['被串区段长度']],
                           # j_lens=[0, 0],
                           # m_typs=['2000A_25Hz_Coding'],
                           j_lens=[0, 0],
                           m_typs=['2000A'],
                           c_nums=[para['被串电容数']],
                           sr_mods=[para['sr_mod_被']],
                           send_lvs=[send_level],
                           parameter=parameter)

        # m_frqs = generate_frqs(Freq(para['freq_被']), 2)
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=2,
        #                    m_frqs=m_frqs,
        #                    m_lens=[560, 830],
        #                    j_lens=[29, 29, 29],
        #                    m_typs=['2000A']*2,
        #                    c_nums=[6, 9],
        #                    sr_mods=[para['sr_mod_被']]*2,
        #                    send_lvs=[send_level]*2,
        #                    parameter=parameter)

        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        self.change_c_value()
        self.pop_c()

        self.change_cable_length()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)
        self.set_rail_para(line=l3, z_trk=para['Trk_z'], rd=para['Trk_z'])
        self.set_rail_para(line=l4, z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']

    def change_cable_length(self):
        para = self.parameter

        if para['主串电缆长度'] is not None:
            for ele in self.section_group3['区段1'].element.values():
                if isinstance(ele, ZPW2000A_Optimize_0809):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']
        if para['被串电缆长度'] is not None:
            for ele in self.section_group4['区段1'].element.values():
                if isinstance(ele, ZPW2000A_Optimize_0809):
                    ele_cab = ele['3Cab']
                    ele_cab.length = para['主串电缆长度']

    def pop_c(self):
        para = self.parameter
        name_list = self.section_group3['区段1'].get_C_TB_names()

        for temp in para['主串拆卸情况']:
            str_temp = name_list[temp-1][1]
            self.section_group3['区段1'].element.pop(str_temp)

        name_list = self.section_group4['区段1'].get_C_TB_names()
        for temp in para['被串拆卸情况']:
            str_temp = name_list[temp-1][1]
            self.section_group4['区段1'].element.pop(str_temp)


class PreModel_QJ_20201204(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        # m_frqs = generate_frqs(Freq(para['freq_主']), 1)

        m_frqs = [Freq(para['freq_主'])]
        m_lens = [para['主串区段长度']]
        # c_nums = get_c_nums(m_frqs, m_lens)
        c_nums = [para['主串电容数']]

        print(m_frqs)

        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[29, 29],
                           m_typs=['2000A'],
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        # param = para['param']
        #
        # m_frqs = generate_frqs(Freq(para['freq_被']), 3, flip_flag=True)
        #
        # if param.index_bei == 0:
        #     m_frqs.pop(0)
        #
        # # m_lens = param.lens_bei
        #
        # m_num = len(m_lens)
        #
        # m_frqs = m_frqs[0:m_num]
        #
        # c_nums = get_c_nums(m_frqs, m_lens)
        # print(c_nums, m_frqs)

        # 轨道电路初始化
        send_level = para['send_level']
        # m_frqs = generate_frqs(Freq(para['freq_被']), 2)
        # m_lens = [para['被串区段长度']] * 2

        m_frqs = list(map(lambda x: Freq(x), para['freq_被']))
        m_lens = para['被串区段长度']
        # c_nums = get_c_nums(m_frqs, m_lens)
        c_nums = para['被串电容数']

        print(m_frqs)

        # c_nums = para['被串电容数']
        sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=len(m_lens),
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           # j_lens=[0, 0],
                           # m_typs=['2000A_25Hz_Coding'],
                           j_lens=[29] * 4,
                           m_typs=['2000A'] * 3,
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_被']] * 3,
                           send_lvs=[send_level] * 3,
                           parameter=parameter)

        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        self.section_group4 = sg4

        # self.change_c_value()
        # self.pop_c()

        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
                            parameter=parameter)

        # self.set_rail_para(line=l3,z_trk=para['Trk_z'], rd=para['Trk_z'])
        # self.set_rail_para(line=l4,z_trk=para['Trk_z'], rd=para['Trk_z'])

        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        self.set_rail_para(line=l4, z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        self.lg = LineGroup(l3, l4, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        for ele in self.section_group4['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_chuan']

        v1 = 46 * 1e-6
        tmp = para['Ccmp_z_change_chuan'].copy()
        tmp.rlc_s = {
            1700: [10e-3, None, v1],
            2000: [10e-3, None, v1],
            2300: [10e-3, None, v1],
            2600: [10e-3, None, v1]}

        for ele in self.section_group4['区段2'].element.values():
            if isinstance(ele, CapC):
                ele.z = tmp


class PreModel_225Hz_coding(PreModel):
    def __init__(self, parameter):
        # super().__init__(turnout_list, parameter)
        self.parameter = para = parameter
        self.train1 = Train(name_base='列车1', posi=0, parameter=parameter)
        self.train2 = Train(name_base='列车2', posi=0, parameter=parameter)
        # self.train1['分路电阻1'].z = 1000000
        # self.train2['分路电阻1'].z = 1000000

        # 轨道电路初始化
        send_level = para['send_level']
        m_frqs = generate_frqs(Freq(para['freq_主']), 1)
        m_lens = [para['主串区段长度']]*1
        c_nums = get_c_nums(m_frqs, m_lens)
        # c_nums = para['主串电容数']
        sg3 = SectionGroup(name_base='地面', posi=0, m_num=1,
                           m_frqs=m_frqs,
                           m_lens=m_lens,
                           j_lens=[29, 29],
                           m_typs=['2000A'],
                           c_nums=c_nums,
                           sr_mods=[para['sr_mod_主']],
                           send_lvs=[send_level],
                           parameter=parameter)

        flg = para['pwr_v_flg']
        if para['sr_mod_主'] == '左发':
            sg3['区段1']['左调谐单元'].set_power_voltage(flg)
        elif para['sr_mod_主'] == '右发':
            sg3['区段1']['右调谐单元'].set_power_voltage(flg)

        # param = para['param']
        #
        # m_frqs = generate_frqs(Freq(para['freq_被']), 3, flip_flag=True)
        #
        # if param.index_bei == 0:
        #     m_frqs.pop(0)
        #
        # # m_lens = param.lens_bei
        #
        # m_num = len(m_lens)
        #
        # m_frqs = m_frqs[0:m_num]
        #
        # c_nums = get_c_nums(m_frqs, m_lens)
        # print(c_nums, m_frqs)

        # # 轨道电路初始化
        # send_level = para['send_level']
        # m_frqs = generate_frqs(Freq(para['freq_被']), 1)
        # m_lens = [para['被串区段长度']]*1
        # # c_nums = get_c_nums(m_frqs, m_lens)
        # c_nums = para['被串电容数']
        # sg4 = SectionGroup(name_base='地面', posi=para['offset_bei'], m_num=1,
        #                    m_frqs=m_frqs,
        #                    m_lens=m_lens,
        #                    # j_lens=[0, 0],
        #                    # m_typs=['2000A_25Hz_Coding'],
        #                    j_lens=[29] * 4,
        #                    m_typs=['2000A'] * 3,
        #                    c_nums=c_nums,
        #                    sr_mods=[para['sr_mod_被']] * 3,
        #                    send_lvs=[send_level] * 3,
        #                    parameter=parameter)


        # partent = sg3['区段1']
        # ele = JumperWire(parent_ins=partent,
        #                  name_base='跳线',
        #                  posi=para['主串区段长度'])
        # partent.add_child('跳线', ele)
        # ele.set_posi_abs(0)
        # self.jumper = ele

        self.section_group3 = sg3
        # self.section_group4 = sg4

        self.change_c_value()
        # self.pop_c()


        self.l3 = l3 = Line(name_base='线路3', sec_group=sg3,
                            parameter=parameter)
        # self.l4 = l4 = Line(name_base='线路4', sec_group=sg4,
        #                     parameter=parameter)
        self.set_rail_para(line=l3,z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        # self.set_rail_para(line=l3, z_trk=para['Trk_z'], rd=para['Trk_z'])
        # self.set_rail_para(line=l4, z_trk=para['Trk_z'], rd=para['Trk_z'])

        # self.lg = LineGroup(l3, l4, name_base='线路组')
        self.lg = LineGroup(l3, name_base='线路组')

        self.lg.special_point = para['special_point']
        self.lg.refresh()

    def change_c_value(self):
        para = self.parameter

        for ele in self.section_group3['区段1'].element.values():
            if isinstance(ele, CapC):
                ele.z = para['Ccmp_z_change_zhu']

        # for ele in self.section_group4['区段1'].element.values():
        #     if isinstance(ele, CapC):
        #         ele.z = para['Ccmp_z_change_chuan']

        v1 = 46 * 1e-6
        tmp = para['Ccmp_z_change_chuan'].copy()
        tmp.rlc_s = {
            1700: [10e-3, None, v1],
            2000: [10e-3, None, v1],
            2300: [10e-3, None, v1],
            2600: [10e-3, None, v1]}

        # for ele in self.section_group4['区段2'].element.values():
        #     if isinstance(ele, CapC):
        #         ele.z = tmp

    def add_train(self):
        para = self.parameter
        l3 = Line(name_base='线路3', sec_group=self.section_group3,
                  parameter=self.parameter, train=[self.train2])
        self.l3 = l3

        # l4 = Line(name_base='线路4', sec_group=self.section_group4,
        #           parameter=self.parameter, train=[self.train1])
        # self.l4 = l4

        self.set_rail_para(line=l3, z_trk=para['主串钢轨阻抗'], rd=para['主串道床电阻'])
        # self.set_rail_para(line=l4,z_trk=para['被串钢轨阻抗'], rd=para['被串道床电阻'])

        # self.lg = LineGroup(self.l3, self.l4, name_base='线路组')
        self.lg = LineGroup(self.l3, name_base='线路组')
        self.lg.special_point = self.parameter['special_point']
        self.lg.refresh()
