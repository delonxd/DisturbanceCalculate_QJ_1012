from src.AbstractClass.ElePack import *
from src.Module.JumperWire import *
from src.Model.SingleLineModel import *
import numpy as np


#################################################################################

# 显示元素
def show_ele(vessel, para=''):
    if isinstance(vessel, (list, set)):
        list_t = list()
        for ele in vessel:
            if para == '':
                list_t.append(ele.__repr__())
            else:
                list_t.append(ele.__dict__[para].__repr__())
        list_t.sort()
        for ele in list_t:
            print(ele)
    elif isinstance(vessel, (dict, ElePack)):
        keys = sorted(list(vessel.keys()))
        for key in keys:
            if para == '':
                print(key, ':', vessel[key])
            else:
                print(vessel[key].__dict__[para])


#################################################################################

# 获取频率
def generate_frqs(freq1, m_num, flip_flag=False):
    frqs = list()
    if flip_flag:
        freq1.change_freq()
    for _ in range(m_num):
        frqs.append(freq1)
        freq1 = freq1.copy()
        freq1.change_freq()
    return frqs


#################################################################################

# 获取电容数
def get_c_nums(m_frqs, m_lens):
    c_nums = list()
    for num in range(len(m_frqs)):
        freq = m_frqs[num]
        length = m_lens[num]
        c_num = get_c_num(freq, length)
        c_nums.append(c_num)
    return c_nums


#################################################################################

# 获取电容数
def get_c_num(freq, length):
    if 0 < length < 300:
        index = 0
    elif length == 300:
        index = 1
    elif length > 300:
        index = int((length - 251) / 50)
    else:
        index  = 0

    CcmpTable1 = [0, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23, 24, 25]
    CcmpTable2 = [0, 4, 5, 5, 6, 7,  7,  8,  8,  9, 10, 10, 11, 12, 12, 13, 13, 14, 15, 15, 16, 17, 17, 18, 18]

    freq = freq.value
    if freq == 1700 or freq == 2000:
        table = CcmpTable1
    elif freq == 2300 or freq == 2600:
        table = CcmpTable2
    else:
        table = []

    c_num = table[index]

    return c_num


#################################################################################

# 获取钢轨电流
def get_i_trk(line, posi, direct='右'):
    i_trk = None
    if direct == '右':
        if line.node_dict[posi].r_track is not None:
            i_trk = line.node_dict[posi].r_track['I1'].value_c
        else:
            i_trk = 0.0
    elif direct == '左':
        if line.node_dict[posi].l_track is not None:
            i_trk = line.node_dict[posi].l_track['I2'].value_c
        else:
            i_trk = 0.0

    return i_trk


#################################################################################

# 获取耦合系数
def get_mutual(distance):
    l1 = 6
    d = 1.435
    k1 = 13

    k_mutual = k1 / np.log((l1 * l1 - d * d) / l1 / l1)
    l2 = distance
    k2 = k_mutual * np.log((l2 * l2 - d * d) / l2 / l2)
    return k2


#################################################################################

# 配置SVA'互感
def config_sva1_mutual(model, temp, zm_sva):
    # zm_sva = 2 * np.pi * 1700 * 1 * 1e-6 * 1j
    m1 = model

    # temp_list = [(3, 4, '右'), (3, 4, '左') ,(4, 3, '左') ,(4, 3, '左')]
    # for temp in temp_list:
    line_zhu = '线路' + str(temp[0])
    line_bei = '线路' + str(temp[1])
    str_t = '线路组_' + line_bei + '_地面_区段1_' + temp[2] + '调谐单元_6SVA1_方程1'
    equ_t = m1.equs.equ_dict[str_t]
    str_t = '线路组_' + line_zhu + '_地面_区段1_' + temp[2] + '调谐单元'
    varb1 = m1[line_zhu]['元件'][str_t]['6SVA1']['I1']
    varb2 = m1[line_zhu]['元件'][str_t]['6SVA1']['I2']
    equ_t.varb_list.append(varb1)
    equ_t.varb_list.append(varb2)
    equ_t.coeff_list = np.append(equ_t.coeff_list, zm_sva)
    equ_t.coeff_list = np.append(equ_t.coeff_list, -zm_sva)


#################################################################################

# 配置跳线组
def config_jumpergroup(*jumpers):
    for jumper in jumpers:
        if not isinstance(jumper, JumperWire):
            raise KeyboardInterrupt('类型错误：参数需要为跳线类型')
        else:
            jumper.jumpergroup = list(jumpers)


#################################################################################

# 合并节点
def combine_node(nodes):
    if len(nodes) < 1:
        raise KeyboardInterrupt('数量错误：合并node至少需要1个参数')

    posi = nodes[0].posi
    node_new = Node(posi)
    node_new.node_type = 'combined'
    node_new.l_track = list()
    node_new.r_track = list()
    for node in nodes:
        if not isinstance(node, Node):
            raise KeyboardInterrupt('类型错误：合并node参数需要为节点类型')
        elif not node.posi == posi:
            raise KeyboardInterrupt('位置错误：合并node需要节点在相同水平位置')
        else:
            if node.l_track is not None:
                node_new.l_track.append(node.l_track)
            if node.r_track is not None:
                node_new.r_track.append(node.r_track)
            for key, value in node.element.items():
                node_new.element[key] = value
            node_new.equs.add_equations(node.equs)
    node_new.group_type = 'combined'
    return node_new


#################################################################################

# 合并节点组
def combine_node_group(lines):
    groups = NodeGroup()
    posi_set = set()
    for line in lines:
        posi_set.update(line.node_dict.posi_set)

    posi_list = list(posi_set)
    posi_list.sort()

    for posi in posi_list:
        nodes_list = list()
        for line in lines:
            if posi in line.node_dict.keys():
                nodes_list.append(line.node_dict[posi])
        nodes = tuple(nodes_list)
        node_new = combine_node(nodes)
        groups.node_dict[posi] = node_new

    return groups


#################################################################################

# 检查输入
def check_input(df):
    para = dict()
    para['FREQ'] = [1700, 2000, 2300, 2600]
    para['SEND_LEVEL'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    para['CABLE_LENGTH'] = [7.5, 10]
    para['C_NUM'] = [0, 1, 2, 3, 4, 5, 6, 7]
    para['TB_MODE'] = ['双端TB', '左端单TB', '右端单TB', '无TB']


    num_len = len(list(df['序号']))
    for temp_temp in range(num_len):
        df_input = df.iloc[temp_temp]

        # 检查主串名称格式
        name = str(df_input['主串区段'])
        if len(name) <= 8:
            pass
        else:
            raise KeyboardInterrupt("主串区段应填写长度小于等于8位的字符串")

        # 检查被串名称格式
        name = str(df_input['被串区段'])
        if len(name) <= 8:
            pass
        else:
            raise KeyboardInterrupt("被串区段应填写长度小于等于8位的字符串")

        # 检查主串方向格式
        if df_input['主串方向'] == '左发' or df_input['主串方向'] == '右发':
            pass
        else:
            raise KeyboardInterrupt("主串方向应填写'左发'或'右发'")

        # 检查被串方向格式
        if df_input['被串方向'] == '左发' or df_input['被串方向'] == '右发':
            pass
        else:
            raise KeyboardInterrupt("被串方向应填写'左发'或'右发'")

        # 检查主串区段长度格式
        if 0 <= df_input['主串区段长度(m)'] <= 650:
            pass
        else:
            raise KeyboardInterrupt("'主串区段长度(m)'应填写0~650的实数")

        # 检查被串区段长度格式
        if 0 <= df_input['被串区段长度(m)'] <= 650:
            pass
        else:
            raise KeyboardInterrupt("'被串区段长度(m)'应填写0~650的实数")

        # 检查被串相对位置格式
        if -650 <= df_input['被串相对位置(m)'] <= 650:
            pass
        else:
            raise KeyboardInterrupt("'被串相对位置(m)'应填写-650~650的实数")

        # 检查耦合系数格式
        if 0 < df_input['耦合系数'] <= 40:
            pass
        else:
            raise KeyboardInterrupt("'耦合系数'应填写大于0小于等于40的实数")

        # 检查主串电平级格式
        if df_input['主串电平级'] in para['SEND_LEVEL']:
            pass
        else:
            raise KeyboardInterrupt("'主串电平级'应填写1~9的整数")

        # 检查主串频率格式
        if df_input['主串频率(Hz)'] in para['FREQ']:
            pass
        else:
            raise KeyboardInterrupt("'主串频率(Hz)'应填写四种标准载频之一")

        # 检查被串频率格式
        if df_input['被串频率(Hz)'] in para['FREQ']:
            pass
        else:
            raise KeyboardInterrupt("'被串频率(Hz)'应填写四种标准载频之一")

        # 检查主串电缆长度格式
        if df_input['主串电缆长度(km)'] in para['CABLE_LENGTH']:
            pass
        else:
            raise KeyboardInterrupt("'主串电缆长度(km)'应填写7.5或10")

        # 检查被串电缆长度格式
        if df_input['被串电缆长度(km)'] in para['CABLE_LENGTH']:
            pass
        else:
            raise KeyboardInterrupt("'被串电缆长度(km)'应填写7.5或10")

        # 检查主串电容数格式
        if df_input['主串电容数(含TB)'] in para['C_NUM']:
            pass
        else:
            raise KeyboardInterrupt("'主串电容数(含TB)'应填写0~7之间的整数")

        # 检查被串电容数格式
        if df_input['被串电容数(含TB)'] in para['C_NUM']:
            pass
        else:
            raise KeyboardInterrupt("'被串电容数(含TB)'应填写0~7之间的整数")

        # 检查主串电容值格式
        if 25 <= df_input['主串电容值(μF)'] <= 80:
            pass
        else:
            raise KeyboardInterrupt("'主串电容值(μF)'应填写25~80的实数")

        # 检查被串电容值格式
        if 25 <= df_input['被串电容值(μF)'] <= 80:
            pass
        else:
            raise KeyboardInterrupt("'被串电容值(μF)'应填写25~80的实数")

        # 检查主串道床电阻格式
        if 0 < df_input['主串道床电阻(Ω·km)'] <= 10000:
            pass
        else:
            raise KeyboardInterrupt("'主串道床电阻(Ω·km)'应填写0~10000的正实数")

        # 检查被串道床电阻格式
        if 0 < df_input['被串道床电阻(Ω·km)'] <= 10000:
            pass
        else:
            raise KeyboardInterrupt("'被串道床电阻(Ω·km)'应填写0~10000的正实数")

        # 检查TB模式格式
        if df_input['TB模式'] in para['TB_MODE']:
            pass
        else:
            raise KeyboardInterrupt("'TB模式'应填写标准格式")


def get_section_length():

    import itertools
    param = list()
    zhu_list = range(50, 601, 50)

    for offset in range(50, 301, 50):
        for len1 in zhu_list:
            l_list = [-offset, offset]
            r_list = [len1 - offset, len1 + offset]

            for l_pos, r_pos in itertools.product(l_list, r_list):

                tmp = Param20201307(
                    len_zhu=len1,
                    l_pos=l_pos,
                    r_pos=r_pos,
                )
                if tmp.flg is True:
                    param.append(tmp)
                    print(tmp.lens_zhu, tmp.lens_bei, tmp.offset, tmp.index_bei)
    return param


class LengthParam:
    def __init__(self):
        self.zhu_length = list()
        self.bei_length = list()
        self.offset = 0


class Param20201307:

    def __init__(self, len_zhu, l_pos, r_pos):
        offset = abs(l_pos)
        self.flg = True
        self.l_pos = l_pos
        self.r_pos = r_pos

        self.lens_zhu = [len_zhu]

        tmp = r_pos - l_pos
        self.lens_bei = [len_zhu, tmp, len_zhu]

        # print(self.lens_bei)
        self.offset = None
        self.index_bei = None

        if abs(r_pos) < offset:
            self.flg = False

        if abs(len_zhu - l_pos) < offset:
            self.flg = False

        if r_pos <= l_pos:
            self.flg = False

        if r_pos - l_pos > 600:
            self.flg = False

        if l_pos < 0:
            self.offset = l_pos
            self.lens_bei.pop(0)
            self.index_bei = 0

            if r_pos >= len_zhu:
                self.lens_bei.pop(-1)

        elif l_pos > 0:
            self.offset = l_pos - len_zhu
            self.index_bei = 1

            if r_pos >= len_zhu:
                self.lens_bei.pop(-1)


def parallel(z1, z2):
    return (z1 * z2) / (z1 + z2)


def cal_zl(zpt, zin):
    zj = (0.037931222832602786+0.3334597710765984j)
    zca = (0.006459333+0.030996667j)
    z1 = (zpt * zin) / (zpt + zin) + zca
    return (z1 * zj) / (z1 + zj)


if __name__ == '__main__':
    # m_lens = [700, 700, 700]
    # m_frqs = generate_frqs(Freq(2600), 3)
    # c_nums = get_c_nums(m_frqs, m_lens)
    pass