from src.Module.PortNetwork import TwoPortNetwork
from src.AbstractClass.Equation import *
from src.Module.ParameterType import *
from src.ConstantType import *
import numpy as np


# 钢轨段模型
class SubRailPi(TwoPortNetwork):
    new_table = {
        '左端位置': 'l_posi',
        '右端位置': 'r_posi',
        '长度': 'track_length',
        '钢轨阻抗': 'z_trk',
        '道床电阻': 'rd'
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'z_trk': VariableImpedance,
        'rd': Constant}

    def __init__(self, parent_ins, name_base, l_posi, r_posi, z_trk, rd):
        super().__init__(parent_ins, name_base)
        self.init_position(l_posi)
        self.flag_ele_unit = True
        self.l_posi = l_posi
        self.r_posi = r_posi
        self.track_length = r_posi - l_posi
        self.z_trk = z_trk
        self.rd = rd

    def init_equs(self, freq):
        self.equ1.name = self.name + '_方程1'
        self.equ2.name = self.name + '_方程2'
        self.equ1.varb_list = [self['I1'], self['U1'], self['U2']]
        self.equ2.varb_list = [self['I2'], self['U1'], self['U2']]
        if hasattr(self, 'mutual_trk'):
            m_circuit = self.mutual_trk
            self.varb_dict['Im'] = m_circuit.varb_dict['I1']
            self.equ1.varb_list.append(self['Im'])
            self.equ2.varb_list.append(self['Im'])
        self.get_coeffs(freq)

    def get_coeffs(self, freq):
        z_trk = self.z_trk
        try:
            rd = float(self.rd)
        except:
            print(type(self.rd), '-->', self.rd)
            raise KeyboardInterrupt

        length = self.track_length / 1000
        z0 = z_trk[freq].z
        y0 = 1 / rd
        zc = np.sqrt(z0 / y0)
        gama = np.sqrt(z0 * y0)
        zii = zc * np.sinh(gama * length)
        yii = (np.cosh(gama * length) - 1) / zc / np.sinh(gama * length)
        # rii = np.real(1 / yii)
        # yii = 1 / rii
        y_tk = 1 / zii
        y_rd = yii
        self.value2coeffs(y_rd, y_tk)
        return self.equs

    def value2coeffs(self, y_rd, y_tk):
        self.equ1.coeff_list = np.array([-1, (y_rd + y_tk), -y_tk])
        self.equ2.coeff_list = np.array([-1, -y_tk, (y_tk + y_rd)])
        # mmm = 2 * np.pi* 2600 * 22.820 * 1e-6


        freq_zhu = self.parent_ins.parameter.parameter['freq_主']
        km = self.parent_ins.parameter.parameter['耦合系数']

        # mmm = 2 * np.pi* freq_zhu * km * 1e-6
        mmm = 2 * np.pi* freq_zhu * km * 1e-6 * 1j
        # mmm = 2 * np.pi* 2600 * 13 * 1e-6
        special_point = self.parent_ins.parameter.parameter['极性交叉位置']
        for temp_point in special_point:
            if self.r_posi <= temp_point:
                break
            mmm = -mmm

        if hasattr(self, 'mutual_trk'):
            # m = self.track_length / 1000 * 0.30
            m = self.track_length / 1000 * mmm
            self.equ1.coeff_list = np.array([-1, (y_rd + y_tk), -y_tk,
                                             (m * y_tk)])
            self.equ2.coeff_list = np.array([-1, -y_tk, (y_tk + y_rd),
                                             -(m * (y_rd + y_tk))])

        # if hasattr(self, 'mutual_trk'):
        #     # m = self.track_length / 1000 * 0.30
        #     m = self.track_length / 1000 * mmm
        #     self.equ1.coeff_list = np.array([-1, (y_rd + y_tk), -y_tk,
        #                                      (m * (y_rd + y_tk))])
        #     self.equ2.coeff_list = np.array([-1, -y_tk, (y_tk + y_rd),
        #                                      -(m * y_tk)])
