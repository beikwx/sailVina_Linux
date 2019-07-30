import os
import shutil


def pdbqt2dir(pdbqt_path):
    """
    在相同路径创建一个该名字的文件夹，将pdbqt文件移动进去。\n
    比如pdbqt_path = ./Proteins/a.pdbqt
    :param pdbqt_path: pdbqt文件路径
    """
    # 1.创建文件夹
    pdbqt_dir = pdbqt_path[0:-6]
    os.mkdir(pdbqt_dir)
    # 2.移动文件
    target_path = pdbqt_dir + os.sep + "preped.pdbqt"
    shutil.move(pdbqt_path, target_path)


def read_para(para_name):
    with open("para.txt", "r") as f:
        for line in f.readlines():
            if line.startswith(para_name):
                return line.split("=")[1].strip()


def gen_config_file(output_name, x, y, z, size):
    """

    :param output_name: 输出路径文件名
    :param x: x坐标
    :param y: y坐标
    :param z: z坐标
    :param size: 盒子大小
    """
    exhaustiveness = read_para("exhaustiveness")
    num_modes = read_para("num_modes")
    energy_range = read_para("energy_range")
    with open(output_name, "w") as f:
        f.writelines("center_x = " + str(x) + "\n")
        f.writelines("center_y = " + str(y) + "\n")
        f.writelines("center_z = " + str(z) + "\n")
        f.writelines("size_x = " + str(size) + "\n")
        f.writelines("size_y = " + str(size) + "\n")
        f.writelines("size_z = " + str(size) + "\n")
        f.writelines("exhaustiveness = " + exhaustiveness + "\n")
        f.writelines("num_modes = " + num_modes + "\n")
        f.writelines("energy_range = " + energy_range + "\n")


def get_config_files(protein_path):
    """

    :param protein_path: 蛋白文件夹路径，比如"./Proteins/01"
    :return: 蛋白的config文件
    """
    files = os.listdir(protein_path)
    config_files = []
    for file in files:
        if file.startswith("config"):
            config_files.append(protein_path + os.sep + file)
    return config_files


def mk_output_dir(output_path):
    os.mkdir(output_path)


if __name__ == '__main__':
    # pdbqt2dir("./Proteins/pdb (1).pdbqt")
    # gen_config_file("./config.txt", 1, 1, 1, 20)
    get_config_files(r".\Proteins\01")
