import os
from file_processor import pdbqt2dir


def proteins2dir(proteins_dir):
    receptors = get_proteins(proteins_dir)
    for receptor in receptors:
        pdbqt_path = proteins_dir + os.sep + receptor
        pdbqt2dir(pdbqt_path)


def get_proteins(proteins_dir):
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


def get_pdb_box(pdb_file_path):
    """

    :param pdb_file_path: pdb或者pdbqt文件路径名
    :return: 中心x坐标，中心y坐标，中心z坐标，长，宽，高。
    """
    pass


if __name__ == '__main__':
    proteins2dir(r".\Proteins")
