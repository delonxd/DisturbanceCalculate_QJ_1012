from src.ElePack import ElePack
from src.BasicOutsideModel import SVA


import src.TrackCircuitCalculator3 as tc

# 绝缘节
class Joint(ElePack):
    new_table = {
        '位置标志': 'posi_flag',
        '左侧区段': 'l_section',
        '右侧区段': 'r_section',
        '绝缘节长度': 'j_length',
        '区段类型': 'sec_type'
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, posi_flag,
                 l_section, r_section, j_type, j_length):
        super().__init__(parent_ins, name_base)
        self.posi_flag = posi_flag
        self.init_position(0)
        self.j_type = j_type
        self.l_section = l_section
        self.r_section = r_section
        self.j_length = j_length
        self.set_element()

    @property
    def posi_rlt(self):
        posi = self.parent_ins.s_length if self.posi_flag == '右' else 0
        return posi

    @posi_rlt.setter
    def posi_rlt(self, value):
        self._posi_rlt = value

    @property
    def sec_type(self):
        # sec_type = None
        if self.l_section and self.r_section:
            if self.j_type == '电气':
                if not self.l_section.m_type == self.r_section.m_type:
                    raise KeyboardInterrupt(
                        repr(self.l_section) + '和' + repr(self.r_section) + '区段类型不符')
        sec_type = self.parent_ins.m_type
        return sec_type

    def set_element(self):
        if self.j_type == '电气':
            if self.sec_type == '2000A':
                self.element['SVA'] = SVA(parent_ins=self,
                                          name_base='SVA',
                                          posi=0,
                                          z=tc.TCSR_2000A['SVA_z'])

    def add_joint_tcsr(self):
        if self.j_type == '电气':
            name = '相邻调谐单元'
            if not self.l_section:
                tcsr = self.r_section['左调谐单元']
                flag = '右'
            elif not self.r_section:
                tcsr = self.l_section['右调谐单元']
                flag = '左'
            else:
                return

            if isinstance(tcsr, tc.ZPW2000A_QJ_Normal):
                self[name] = tc.ZPW2000A_QJ_Normal(parent_ins=self, name_base=name, posi_flag=flag,
                                                cable_length=tcsr.cable_length,
                                                mode=tc.change_sr_mode(tcsr.mode), level=1)
