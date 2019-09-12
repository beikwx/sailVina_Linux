# coding: utf-8

import os
from file_processor import pdbqt2dir
from file_processor import gen_config_file
import check
import math
import sys


def proteins2dir(proteins_dir):
    """
    将指定受体文件夹中的受体移动到以受体命名的文件夹中，将受体重命名为"preped.pdbqt"
    :param proteins_dir: 包含pdbqt受体的目录
    :return:生成的受体目录
    """
    receptors = __get_proteins(proteins_dir)
    receptors_dir = []
    for receptor in receptors:
        pdbqt_path = proteins_dir + os.sep + receptor
        receptors_dir.append(os.path.splitext(pdbqt_path)[0])
        pdbqt2dir(pdbqt_path)
    return receptors_dir


def gen_config(protein, ligand):
    """

    :param protein: 蛋白路径，比如r"./Proteins/pdb1/preped.pdbqt"
    :param ligand: 配体路径，比如r"./Ligands/aspirin.pdbqt"
    """
    x_cos, y_cos, z_cos, size = __gen_config_boxes(protein, ligand)
    count = 1
    for x in x_cos:
        for y in y_cos:
            for z in z_cos:
                filename = os.path.split(protein)[0] + os.sep + "config" + str(count) + ".txt"
                # print(filename)
                gen_config_file(filename, x, y, z, size)
                count += 1


def __gen_config_boxes(protein, ligand):
    """
    根据受体和配体生成多个config的盒子
    :param protein: 蛋白路径
    :param ligand: 配体路径
    :returns:x,y,z方向的所有坐标，盒子的大小
    """
    # 获取受体的盒子
    protein_box = __get_pdb_box(protein)
    # 获取配体的盒子
    ligand_box = __get_pdb_box(ligand)

    # 定义对接最大的盒子
    config_box_size = 30.0

    # print(protein_box)
    # print(ligand_box)

    # x方向需要的盒子
    x_count = math.ceil((protein_box[3] + ligand_box[3]) / (config_box_size - ligand_box[3]))
    y_count = math.ceil((protein_box[4] + ligand_box[4]) / (config_box_size - ligand_box[3]))
    z_count = math.ceil((protein_box[5] + ligand_box[5]) / (config_box_size - ligand_box[3]))
    # print(x_count, y_count, z_count)

    x_coordinates = []
    y_coordinates = []
    z_coordinates = []

    # 求config盒子的X坐标合集
    i = 0
    max_x = (protein_box[0] + 0.5 * protein_box[3] + ligand_box[3]) - 0.5 * config_box_size
    while i < x_count:
        x = (protein_box[0] - 0.5 * protein_box[3] - ligand_box[3]) + 0.5 * config_box_size + (
                config_box_size - ligand_box[3]) * i
        if x <= max_x:
            x_coordinates.append(round(x, 2))
        else:
            x_coordinates.append(round(max_x, 2))
        i += 1

    # 求config盒子的Y坐标合集
    i = 0
    min_y = (protein_box[1] - 0.5 * protein_box[4] - ligand_box[4]) + 0.5 * config_box_size
    while i < y_count:
        y = (protein_box[1] + 0.5 * protein_box[4] + ligand_box[4]) - 0.5 * config_box_size - (
                config_box_size - ligand_box[4]) * i
        if y >= min_y:
            y_coordinates.append(round(y, 2))
        else:
            y_coordinates.append(round(min_y, 2))
        i += 1

    # 求config盒子的Z坐标合集
    i = 0
    min_z = (protein_box[2] - 0.5 * protein_box[5] - ligand_box[5]) + 0.5 * config_box_size
    while i < z_count:
        z = (protein_box[2] + 0.5 * protein_box[5] + ligand_box[5]) - 0.5 * config_box_size - (
                config_box_size - ligand_box[5]) * i
        if z >= min_z:
            z_coordinates.append(round(z, 2))
        else:
            z_coordinates.append(round(min_z, 2))
        i += 1

    # print(x_coordinates)
    # print(y_coordinates)
    # print(z_coordinates)
    return x_coordinates, y_coordinates, z_coordinates, config_box_size


def __get_proteins(proteins_dir):
    """

    :param proteins_dir: 受体目录，其中是pdbqt的受体文件
    :return: 所有pdbqt文件的文件名
    """
    proteins = os.listdir(proteins_dir)
    receptors = []
    for protein in proteins:
        if protein.endswith(".pdbqt"):
            receptors.append(protein)

    print("------------------------------------------------------------")
    print("发现受体pdbqt文件" + str(len(receptors)) + "个")
    print("开始移动文件")
    return receptors


def __get_pdb_box(pdb_file_path):
    """
    计算蛋白或者配体的空间中心坐标和最大立方体长宽高。
    :param pdb_file_path: pdb或者pdbqt文件路径名
    :return: 中心x坐标，中心y坐标，中心z坐标，长，宽，高。
    """
    # 保证文件存在
    if not check.check_file(pdb_file_path):
        print(pdb_file_path + "不存在")
        sys.exit()

    atoms_x_list = []
    atoms_y_list = []
    atoms_z_list = []

    # 额外距离
    extra_distance = 0

    # 读取所有非H原子的坐标
    with open(pdb_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                if line[13:14] != "H":
                    atoms_x_list.append(float(line[30:38]))
                    atoms_y_list.append(float(line[38:46]))
                    atoms_z_list.append(float(line[46:54]))

    if len(atoms_x_list) == 0:
        print("没有检测到原子")
        sys.exit()

    box_center_x = round(sum(atoms_x_list) / len(atoms_x_list), 3)
    box_center_y = round(sum(atoms_y_list) / len(atoms_y_list), 3)
    box_center_z = round(sum(atoms_z_list) / len(atoms_z_list), 3)

    box_length = round(max(atoms_x_list) - min(atoms_x_list), 1) + extra_distance
    box_width = round(max(atoms_y_list) - min(atoms_y_list), 1) + extra_distance
    box_height = round(max(atoms_z_list) - min(atoms_z_list), 1) + extra_distance

    return box_center_x, box_center_y, box_center_z, box_length, box_width, box_height


if __name__ == '__main__':
    pass
    # 本地调试代码
    # box = get_pdb_box(r"./Proteins/pdb2/preped.pdbqt")
    # box = __get_pdb_box(r"./Ligands/aspirin.pdbqt", file_type="ligand")
    # print(box)
    # gen_config(r".\Proteins\pdb1\preped.pdbqt", r".\Ligands\aspirin.pdbqt")
    # dirs = proteins2dir(r".\Proteins")
    # print(dirs)
    # print(__gen_config_boxes("D:\\下载\\pdbbind_v2018_other_PL\\v2018-other-PL\\1a0t\\1a0t_pocket.pdb",
    #                          "D:\\Desktop\\1a0t_ligand.pdbqt"))
