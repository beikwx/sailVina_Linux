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
    mgl_python_path = mgl_dir + os.sep + "python.exe"
    if not os.path.exists(mgl_python_path):
        print("mgltools路径下没有python文件")
        sys.exit()

    prepare_receptor4_path = mgl_dir + os.sep + "Lib" + os.sep + "site-packages" + \
                             os.sep + "AutoDockTools" + os.sep + "Utilities24" + \
                             os.sep + "prepare_receptor4"
    if not os.path.exists(prepare_receptor4_path):
        print("没有发现准备prepare_receptor4.py文件")
        sys.exit()

    receptors = os.listdir(receptors_path)
    filter_receptors = []
    output_files = []
    for receptor in receptors:
        if receptor.endswith(".pdb") or receptor.endswith(".mol2") or \
                receptor.endswith(".pdbq"):
            filter_receptors.append(receptor)
            # 获得文件名
            output_files.append(output_dir + os.sep + os.path.split(receptor)[1].split(".")[0] + ".pdbqt")

    i = 0
