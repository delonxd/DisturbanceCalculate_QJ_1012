from src.Module.TCSRBasic import *


# ZPW2000A区间标准配置
class ZPW2000A_QJ_Normal(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))
        # if self.mode == '发送':
        #     # self.add_child('3CabComp', TPortZSeries(self, '3CabComp', para['加感_发送']))
        #     self.add_child('3CabComp', TPortZParallel(self, '3CabComp', para['加感_发送']))
        # elif self.mode == '接收':
        #     # self.add_child('3CabComp', TPortZSeries(self, '3CabComp', para['加感_接收']))
        #     self.add_child('3CabComp', TPortZParallel(self, '3CabComp', para['加感_接收']))

        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        self.add_child('4TAD', TcsrTAD(self, '4TAD',
                                       para['TAD_z1_发送端_区间'],
                                       para['TAD_z2_发送端_区间'],
                                       para['TAD_z3_发送端_区间'],
                                       para['TAD_n_发送端_区间'],
                                       para['TAD_c_发送端_区间']))
        self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内PT+SVA'配置
class ZPW2000A_ZN_PTSVA1(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))
        # self.add_child('3CabComp', TcsrCableComp(self, '3CabComp'))
        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))

        self.add_child('4TAD', TcsrTAD(self, '4TAD',
                                       para['TAD_z1_发送端_区间'],
                                       para['TAD_z2_发送端_区间'],
                                       para['TAD_z3_发送端_区间'],
                                       para['TAD_n_发送端_区间'],
                                       para['TAD_c_发送端_站内']))
        self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('5PT_CA', TPortZSeries(self, '5PT_CA', para['标准短路阻抗']))
        self.add_child('6SVA1', TPortZParallel(self, '6SVA1', para['SVA1_z']))
        self.add_child('7CA', TcsrCA(self, '7CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内PT+SVA'配置
class ZPW2000A_Optimize_Test(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
            self.add_child('2防雷', TcsrFL(self, '2防雷',
                                         para['FL_z1_发送端'],
                                         para['FL_z2_发送端'],
                                         para['FL_n_发送端']))
            self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                              para['Cable_R'],
                                              para['Cable_L'],
                                              para['Cable_C']))

            self.add_child('4TAD', TcsrTAD(self, '4TAD',
                                           para['TAD_z1_发送端_区间'],
                                           para['TAD_z2_发送端_区间'],
                                           para['TAD_z3_发送端_区间'],
                                           para['TAD_n_发送端_区间'],
                                           para['TAD_c_发送端_站内']))
            self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))

            self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))
            # self.add_child('7JZ', TPortZParallel(self, '7JZ', para['Joint_z']))
            self.add_child('7JZ', TPortZParallel(self, '7JZ', para['SVA1_z']))

        elif self.mode == '接收':
            # self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
            self.add_child('1接收端阻抗', TcsrReceiver(self, '1接收端阻抗', para['Zl_rcv']))
        self.add_child('2并联阻抗', TPortZParallel(self, '2并联阻抗', para['zc_half']))
        # self.add_child('2防雷', TcsrFL(self, '2防雷',
        #                              para['FL_z1_发送端'],
        #                              para['FL_z2_发送端'],
        #                              para['FL_n_发送端']))
        # self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
        #                                   para['Cable_R'],
        #                                   para['Cable_L'],
        #                                   para['Cable_C']))
        #
        # self.add_child('4TAD', TcsrTAD(self, '4TAD',
        #                                para['TAD_z1_发送端_区间'],
        #                                para['TAD_z2_发送端_区间'],
        #                                para['TAD_z3_发送端_区间'],
        #                                para['TAD_n_发送端_区间'],
        #                                para['TAD_c_发送端_站内']))
        # self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        #
        # self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))
        # # self.add_child('7JZ', TPortZParallel(self, '7JZ', para['Joint_z']))
        # self.add_child('7JZ', TPortZParallel(self, '7JZ', para['SVA1_z']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A区间白俄配置
class ZPW2000A_QJ_Belarus(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))
        self.add_child('1_隔离盒', TcsrIsolationBelarus(self, '1_隔离盒',
                                              para['Z_iso1_Belarus'],
                                              para['Z_iso2_Belarus']))
        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))
        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        self.add_child('4TAD', TcsrTADBelarus(self, '4TAD',
                                              para['TAD_z1_Belarus'],
                                              para['TAD_z2_Belarus'],
                                              para['TAD_n_Belarus']))
        self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内移频脉冲标准配置
class ZPW2000A_YPMC_Normal(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [45, 37.5, 30, 22.5]
        self.u_list_min = [45, 37.5, 30, 22.5]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPowerYPMC(self, '1发送器',
                                                 para['z_pwr_yp'],
                                                 para['z_pwr_ypmc_iso']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiverYPMC(self, '1接收器',
                                                    para['z_rcv_ypmc_iso2'],
                                                    para['z_rcv_ypmc_iso'],
                                                    para['z_rcv_ypmc']))
        # 注意拓扑结构
        self.add_child('2防雷', TcsrFLYPMC(self, '2防雷',
                                         para['z1_FL_ypmc'],
                                         para['z2_FL_ypmc'],
                                         para['n_FL_ypmc']))
        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        self.add_child('4扼流', TcsrELYPMC(self, '4扼流',
                                         para['z1_EL_ypmc'],
                                         para['z2_EL_ypmc'],
                                         para['n_EL_ypmc']))
        # self.add_child('5BA', TcsrBA(self, '5BA', para['PT']))
        # self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_区间']))
        self.add_child('6CA', TcsrCA(self, '6CA', para['CA_z_站内']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内BPLN配置
class ZPW2000A_ZN_BPLN(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))

        self.add_child('2防雷', TcsrFL(self, '2防雷',
                                     para['FL_z1_发送端'],
                                     para['FL_z2_发送端'],
                                     para['FL_n_发送端']))

        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))
        #
        self.add_child('4BPLN', TcsrTAD(self, '4BPLN',
                                       para['TAD_z1_发送端_站内'],
                                       para['TAD_z2_发送端_站内'],
                                       para['TAD_z3_发送端_站内'],
                                       para['TAD_n_发送端_站内'],
                                       para['TAD_c_发送端_站内']))

        self.add_child('5扼流', TPortZParallel(self, '5扼流',
                                        para['z_be']))

        self.add_child('7CA', TcsrCA(self, '7CA', para['CA_z_站内']))

        # if self.mode == '发送':
        #     self.add_child('2防雷', TPortABCD_tr(self, '2防雷',
        #                                     para['FL_fs_ABCD_A'],
        #                                     para['FL_fs_ABCD_B'],
        #                                     para['FL_fs_ABCD_C'],
        #                                     para['FL_fs_ABCD_D']))
        # elif self.mode == '接收':
        #     self.add_child('2防雷', TPortABCD_re(self, '2防雷',
        #                                     para['FL_js_ABCD_A'],
        #                                     para['FL_js_ABCD_B'],
        #                                     para['FL_js_ABCD_C'],
        #                                     para['FL_js_ABCD_D']))
        #
        #
        # self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
        #                                   para['Cable_R'],
        #                                   para['Cable_L'],
        #                                   para['Cable_C']))
        #
        # if self.mode == '发送':
        #     self.add_child('4BPLN', TPortABCD_tr(self, '4BPLN',
        #                                     para['BPLN_fs_ABCD_A'],
        #                                     para['BPLN_fs_ABCD_B'],
        #                                     para['BPLN_fs_ABCD_C'],
        #                                     para['BPLN_fs_ABCD_D']))
        # elif self.mode == '接收':
        #     self.add_child('4BPLN', TPortABCD_re(self, '4BPLN',
        #                                     para['BPLN_js_ABCD_A'],
        #                                     para['BPLN_js_ABCD_B'],
        #                                     para['BPLN_js_ABCD_C'],
        #                                     para['BPLN_js_ABCD_D']))
        #
        # if self.mode == '发送':
        #     self.add_child('5扼流', TPortZParallel(self, '5扼流',
        #                                     para['EL_fs_z_open']))
        # elif self.mode == '接收':
        #     self.add_child('5扼流', TPortZParallel(self, '5扼流',
        #                                     para['EL_js_z_open']))
        #
        # self.add_child('7CA', TcsrCA(self, '7CA', para['CA_z_站内']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内25Hz叠加电码化
class ZPW2000A_ZN_25Hz_Coding(TCSR):
    # def __init__(self, parent_ins, name_base, posi_flag):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(
                self, '1发送器',
                z=para['z_pwr']))

            self.add_child('2FT1u', TcsrFT1u(
                self, '2FT1u',
                r1=para['R1_FT1u_25Hz_Coding'],
                zs=para['zs_FT1u_25Hz_Coding'],
                zm=para['zm_FT1u_25Hz_Coding'],
                n=para['n_FT1u_25Hz_Coding']))

        elif self.mode == '接收' or self.mode == '不发码':
            self.add_child('1开关断开', OPortPowerI(
                self, '1开关断开',
                current=0))

        self.add_child('3调整电阻', TPortZSeries(
            self, '3调整电阻',
            z=para['Rt_25Hz_Coding']))

        self.add_child('3室内隔离盒', TcsrNGL25HzCoding(
            self, '3室内隔离盒',
            z1=para['z1_NGL_25Hz_Coding'],
            c1=para['C1_NGL_25Hz_Coding'],
            l=para['L_NGL_25Hz_Coding'],
            c3=para['C3_NGL_25Hz_Coding'],
            c4=para['C4_NGL_25Hz_Coding']))

        self.add_child('4Cab', TPortCable(
            self, '4Cab',
            length=cable_length,
            cab_r=para['Cable_R'],
            cab_l=para['Cable_L'],
            cab_c=para['Cable_C']))

        self.add_child('5室外隔离盒', TcsrWGL25HzCoding(
            self, '5室外隔离盒',
            l1=para['L1_WGL_25Hz_Coding'],
            c1=para['C1_WGL_25Hz_Coding'],
            zs=para['zs_WGL_25Hz_Coding'],
            zm=para['zm_WGL_25Hz_Coding'],
            n=para['n_WGL_25Hz_Coding'],
            c2=para['C2_WGL_25Hz_Coding'],
            l2=para['L2_WGL_25Hz_Coding']))

        self.add_child('6扼流', TcsrEL25HzCoding(
            self, '6扼流',
            zs=para['zs_EL_25Hz_Coding'],
            zm=para['zm_EL_25Hz_Coding'],
            n=para['n_EL_25Hz_Coding']))

        # self.add_child('3FT1u电阻', TPortZSeries(self, '3FT1u阻抗', para['z_FT1u']))
        # self.add_child('4FT1u开路电阻', TPortZSeries(self, '3FT1u阻抗', para['z_FT1u']))
        # self.add_child('5FT1u变压器', TPortCircuitN(self, '4FT1u变压器', para['n_FT1u']))
        #
        # self.add_child('5BPM阻抗', TPortZSeries(self, '5BPM阻抗', para['z_BPM']))
        # self.add_child('6BPM变压器', TPortCircuitN(self, '6BPM变压器', para['n_BPM']))
        #
        # self.add_child('7扼流变压器', TPortCircuitN(self, '7扼流变压器', para['n_EL_25Hz']))
        # self.add_child('8扼流阻抗', TPortZParallel(self, '8扼流阻抗', para['z_EL_25Hz']))

        self.md_list = self.get_md_list([])
        self.config_varb()


# ZPW2000A站内PT+SVA'配置
class ZPW2000A_Optimize_0809(TCSR):
    def __init__(self, parent_ins, name_base,
                 posi_flag, cable_length, mode, level):
        super().__init__(parent_ins, name_base, posi_flag)
        self.parameter = para = parent_ins.parameter
        self.posi_flag = posi_flag
        self.init_position(0)
        self.flag_ele_list = True
        self.flag_ele_unit = True
        self.mode = mode
        self.send_level = level
        self.u_list_max = [183, 164, 142, 115, 81.5, 68, 60.5, 48.6, 40.8]
        self.u_list_min = [167, 150, 130, 105, 74.5, 61, 55, 44, 37]

        if self.mode == '发送':
            self.add_child('1发送器', TcsrPower(self, '1发送器', para['z_pwr']))
        elif self.mode == '接收':
            self.add_child('1接收器', TcsrReceiver(self, '1接收器', para['Z_rcv']))

        self.add_child('3Cab', TPortCable(self, '3Cab', cable_length,
                                          para['Cable_R'],
                                          para['Cable_L'],
                                          para['Cable_C']))

        self.add_child('4EL_Op_0809', TcsrEL_OP_0809(self, '4EL_Op_0809',
                                       para['Op_0809_z1'],
                                       para['Op_0809_z2'],
                                       para['Op_0809_n']))

        self.add_child('7CA', TcsrCA(self, '7CA', para['CA_z_区间']))

        self.md_list = self.get_md_list([])
        self.config_varb()