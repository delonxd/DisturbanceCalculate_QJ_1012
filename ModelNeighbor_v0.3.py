from MainCalculate import *
import time
import os


def main(path1, path2, path3):
    try:
        main_cal(path1, path2, path3)
        print('finished')
        return 1
    except BaseException as reason:
        print(reason)
        return reason


def main(path1, path2, path3):
    try:
        main_cal(path1, path2, path3)
        print('unfinished')
        return 1
    except BlockingIOError as reason:
        print(reason)
        return reason

    except BaseException as reason:
        for ele in range(path1):
            path1 += 1
            show_ele(vessel=path1)

        print(reason)
        return reason


if __name__ == '__main__':
    main('邻线干扰参数输入_V002.xlsx',
         '仿真输出' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx',
         os.getcwd())
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    # path_dir = '测试结果/输出_' + time.strftime("%Y%m%d%H%M%S", time.localtime())
    # os.makedirs(path_dir)
    # name_list = [
    #              # '测试表格1_区段名称测试',
    #              # '测试表格2_方向测试',
    #              # '测试表格3_区段长度测试',
    #              # '测试表格4_相对位置测试',
    #              # '测试表格5_耦合系数测试',
    #              # '测试表格6_电平级测试',
    #              # '测试表格7_频率测试',
    #              # '测试表格8_电缆长度测试',
    #              '测试表格9_电容数测试',
    #              # '测试表格10_电容值测试',
    #              # '测试表格11_道床电阻测试',
    #              # '测试表格12_TB模式测试',
    #              ]
    #
    # for ele in name_list:
    #     path1 = '测试表格/' + ele + '.xlsx'
    #     path2 = path_dir + '/' + ele + '_输出结果.xlsx'
    #     main(path1,
    #          path2,
    #          os.getcwd())
