import os
import shutil


def pdbqt2dir(pdbqt_path):
    """
    pdbqt_path = ./Proteins/a.pdbqt
    :param pdbqt_path: pdbqt文件路径
    :return: 在相同路径创建一个该名字的文件夹，将pdbqt文件移动进去。
    """
    # 1.创建文件夹
    pdbqt_dir = pdbqt_path[0:-6]
    os.mkdir(pdbqt_dir)
    # 2.移动文件
    target_path = pdbqt_dir + os.sep + "preped.pdbqt"
    shutil.move(pdbqt_path, target_path)


if __name__ == '__main__':
    pdbqt2dir("./Proteins/pdb (1).pdbqt")
