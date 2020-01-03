# coding: utf-8

import os
import shutil
import copy


def pdbqt2dir(pdbqt_path):
    """
    在相同路径创建一个该名字的文件夹，将pdbqt文件移动进去。\n
    比如pdbqt_path = ./Proteins/a.pdbqt
    :param pdbqt_path: pdbqt文件路径
    """
    # 1.创建文件夹
    pdbqt_dir = pdbqt_path[0:-6]
    if not os.path.exists(pdbqt_dir):
        os.mkdir(pdbqt_dir)
    # 2.移动文件
    target_path = pdbqt_dir + os.sep + "preped.pdbqt"
    shutil.move(pdbqt_path, target_path)


def read_para(para_name):
    with open("para.txt", "r", encoding='UTF-8') as f:
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
    with open(output_name, "w", encoding='UTF-8') as f:
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
    """
    如果不存在就创建输出文件夹
    :param output_path: 目标文件夹
    """
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except FileExistsError:
            return


def create_scores_file(output_file, scores_dict):
    """
    创建
    :param output_file: 输出目录
    :param scores_dict:分数字典
    """
    with open(output_file, "w", encoding='UTF-8') as f:
        f.write("receptor_name\tligand_name\tscores\n")
        for receptor in scores_dict:
            for ligand in scores_dict[receptor]:
                # 如果列表只有一个元素
                if not isinstance(scores_dict[receptor][ligand], list):
                    f.write(receptor + "\t" + ligand + "\t" + scores_dict[receptor][ligand] + "\n")
                else:
                    for score in scores_dict[receptor][ligand]:
                        f.write(receptor + "\t" + ligand + "\t" + score + "\n")


def get_best_scores(scores_dict):
    """
    传入分数字典，将分数最小的输出，多个都输出。
    :param scores_dict: 分数列表
    :return: 最小的配体字典
    """
    # 获取分数最低的值
    tmp_dict = copy.deepcopy(scores_dict)
    for receptor in scores_dict:
        min_score = 0
        for ligand in scores_dict[receptor]:
            score = float(scores_dict[receptor][ligand])
            if score <= min_score:
                min_score = score

        for ligand in scores_dict[receptor]:
            if float(scores_dict[receptor][ligand]) > min_score:
                # 删除分数大于最小值的字典
                tmp_dict[receptor].pop(ligand)

    return tmp_dict


def copy_proteins(src_dir, dst_dir):
    """
    将一个文件夹中的所有pdbqt格式的蛋白复制到另一个文件夹中
    :param src_dir: 原始文件夹
    :param dst_dir: 目标文件夹
    """
    for file in os.listdir(src_dir):
        if file.endswith(".pdbqt"):
            src_file = os.path.join(src_dir, file)
            shutil.copy(src_file, dst_dir)


if __name__ == '__main__':
    copy_proteins("./Proteins", "./PreProteins")
