import os
from file_processor import pdbqt2dir
import check
import math


def proteins2dir(proteins_dir):
    receptors = __get_proteins(proteins_dir)
    for receptor in receptors:
        pdbqt_path = proteins_dir + os.sep + receptor
        pdbqt2dir(pdbqt_path)


def gen_config(protein, ligand):
    """
    根据受体和配体生成config文件
    :param protein: 蛋白路径
    :param ligand: 配体路径
    """
    # 获取受体的盒子
    protein_box = __get_pdb_box(protein)
    # 获取配体的盒子
    ligand_box = __get_pdb_box(ligand, file_type="ligand")

    # 定义对接最大的盒子
    config_box_size = 30.0

    print(protein_box)
    print(ligand_box)

    # x方向需要的盒子
    x_count = math.ceil((protein_box[3] + ligand_box[3]) / (config_box_size - ligand_box[3]))
    y_count = math.ceil((protein_box[4] + ligand_box[4]) / (config_box_size - ligand_box[3]))
    z_count = math.ceil((protein_box[5] + ligand_box[5]) / (config_box_size - ligand_box[3]))
    print(x_count, y_count, z_count)


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
    print("发现受体pdbqt文件" + str(len(receptors)) + "个")
    print("开始准备文件.........")
    return receptors


def __get_pdb_box(pdb_file_path, file_type="protein"):
    """
    计算蛋白或者配体的空间中心坐标和最大立方体长宽高。
    :param pdb_file_path: pdb或者pdbqt文件路径名
    :param file_type:输入的格式类型，默认为蛋白，设置为ligand则为小分子
    :return: 中心x坐标，中心y坐标，中心z坐标，长，宽，高。
    """
    # 保证文件存在
    if not check.check_file(pdb_file_path):
        return

    atoms_x_list = []
    atoms_y_list = []
    atoms_z_list = []

    # 额外距离
    extra_distance = 0

    # 判断参数类型
    if file_type == "protein":
        atom_marker = "ATOM"
    elif file_type == "ligand":
        atom_marker = "HETATM"
    else:
        print("参数不正确")
        return

    # 读取所有非H原子的坐标
    with open(pdb_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(atom_marker):
                if line[13:14] != "H":
                    atoms_x_list.append(float(line[30:38]))
                    atoms_y_list.append(float(line[38:46]))
                    atoms_z_list.append(float(line[46:54]))

    if len(atoms_x_list) == 0:
        print("没有检测到原子")
        return

    box_center_x = round(sum(atoms_x_list) / len(atoms_x_list), 3)
    box_center_y = round(sum(atoms_y_list) / len(atoms_y_list), 3)
    box_center_z = round(sum(atoms_z_list) / len(atoms_z_list), 3)

    box_length = round(max(atoms_x_list) - min(atoms_x_list), 1) + extra_distance
    box_width = round(max(atoms_y_list) - min(atoms_y_list), 1) + extra_distance
    box_height = round(max(atoms_z_list) - min(atoms_z_list), 1) + extra_distance

    return box_center_x, box_center_y, box_center_z, box_length, box_width, box_height


if __name__ == '__main__':
    # # box = get_pdb_box(r"./Proteins/pdb2/preped.pdbqt")
    # box = __get_pdb_box(r"./Ligands/aspirin.pdbqt", file_type="ligand")
    # print(box)

    gen_config(r"./Proteins/pdb1/preped.pdbqt", r"./Ligands/aspirin.pdbqt")
