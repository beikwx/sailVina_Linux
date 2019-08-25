"""
用于批量准备受体文件
需要mgltool的python路径和文件路径
"""

import os
import sys


def prepare_receptors(mgl_dir, receptors_path, output_dir):
    """

    :param mgl_dir: C:\\DrugDesign\\mgltools
    :param receptors_path: D:\\Desktop\\Receptors
    :param output_dir: D:\\Desktop\\output
    """
    # 检查mgltools的路径
    mgl_python_path = mgl_dir + os.sep + "python.exe"
    if not os.path.exists(mgl_python_path):
        print("mgltools路径下没有python文件")
        sys.exit()

    prepare_receptor4_path = mgl_dir + os.sep + "Lib" + os.sep + "site-packages" \
                             + os.sep + "AutoDockTools" + os.sep + "Utilities24" \
                             + os.sep + "prepare_receptor4.py"

    # print(prepare_receptor4_path)
    if not os.path.exists(prepare_receptor4_path):
        print("没有发现prepare_receptor4.py文件")
        sys.exit()

    # 获取输入的文件名 xx.pdb
    receptors_name = get_receptors(receptors_path)

    i = 0
    while i < len(receptors_name):
        input_file = receptors_path + os.sep + receptors_name[i]
        output_file = output_dir + os.sep + receptors_name[i].split(".")[0] + ".pdbqt"
        print("--------------------开始准备受体--------------------")
        print("当前输入文件" + input_file)
        cmd = "%s %s -r %s -o %s -A -e" % (mgl_python_path, prepare_receptor4_path, input_file, output_file)
        # print(cmd)
        os.system(cmd)
        print("--------------------受体准备完成--------------------")
        print("当前输出文件" + output_file)
        i += 1


def get_receptors(receptors_root_path):
    receptors = os.listdir(receptors_root_path)
    receptors_name = []
    for receptor_path in receptors:
        if receptor_path.endswith(".pdb") or receptor_path.endswith(".mol2") or \
                receptor_path.endswith(".pdbq"):
            receptors_name.append(os.path.split(receptor_path)[-1])
    return receptors_name


if __name__ == '__main__':
    # 读取命令行输入
    if len(sys.argv) == 1:
        print("--------------------------------------------------------------------------------")
        print('命令格式:\n'
              'python .\\batch_prepare_receptor.py mgltools目录 受体目录 输出目录\n\n'
              '其中:\n'
              'mgltools目录：安装mgltools的目录，比如C:\\mgltools，如果路径包含空格请用引号，比如"C:\\Program files\\mgltools"\n'
              '受体目录：所有受体所在的目录，比如D:\\Desktop\\Receptors\n'
              '输出目录：准备后文件输出的目录，比如D:\\Desktop\\Proteins')
        print("--------------------------------------------------------------------------------")
        sys.exit()
    elif len(sys.argv) != 4:
        print("参数个数不正确，请检查参数！")
        sys.exit()
    else:
        mgl_dir, receptors_path, output_dir = sys.argv[1:]
        prepare_receptors(mgl_dir, receptors_path, output_dir)
