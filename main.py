import os
import sys

from check import check_cmd_para
from dock_processor import vina_dock
from file_processor import copy_proteins, mk_output_dir, pdbqt2dir, get_config_files, remove_dir
from help_text import INFO
from pdb_processor import gen_config


class Main:

    def __init__(self):
        self.ligands = []
        self.ligands_no_suf = []
        self.proteins = []
        self.proteins_no_suf = []
        self.output_path = []
        self.pre_proteins_path = []

    def run(self):

        # 0.检查参数
        if not check_cmd_para(sys.argv):
            print(INFO)
            sys.exit()

        # 1.文件路径获取
        # 1.1读取配体文件名，筛选掉非pdbqt文件
        for ligand in os.listdir("Ligands"):
            if ligand.endswith(".pdbqt") and os.path.getsize("Ligands" + os.sep + ligand):
                self.ligands.append(ligand)
                self.ligands_no_suf.append(ligand[0:-6])
                self.pre_proteins_path.append(os.path.join("PreProteins", ligand[0:-6]))
        # print(self.ligands)
        # print(self.ligands_no_suf)
        # print(self.pre_proteins_path)
        # 1.2读取受体文件名
        protein_dir = sys.argv[1]
        for protein in os.listdir(protein_dir):
            if protein.endswith(".pdbqt") and os.path.getsize("Proteins" + os.sep + protein):
                self.proteins.append(protein)
                self.proteins_no_suf.append(protein[0:-6])
        # print(self.proteins)
        # print(self.proteins_no_suf)
        # 1.3创建输出路径
        for ligand in self.ligands_no_suf:
            for protein in self.proteins_no_suf:
                output_path = os.path.join("Output", ligand, protein)
                mk_output_dir(output_path)
                self.output_path.append(output_path)
        # print(self.output_path)

        # 2.准备文件
        # 2.1移动文件,建文件夹
        for path in self.pre_proteins_path:
            mk_output_dir(path)
            copy_proteins(protein_dir, path)
            for protein in self.proteins:
                pdbqt2dir(os.path.join(path, protein))

        # 2.2生成config文件
        for ligand in self.ligands_no_suf:
            for protein in self.proteins_no_suf:
                receptor_file = "PreProteins" + os.sep + ligand + os.sep + protein + os.sep + "preped.pdbqt"
                gen_config(receptor_file, "Ligands" + os.sep + ligand + ".pdbqt")

        # 2.3进行对接
        # 2.1配体文件
        for ligand in self.ligands_no_suf:
            ligand_file = "Ligands" + os.sep + ligand + ".pdbqt"
            # 2.2受体文件
            for protein in self.proteins_no_suf:
                receptor_file = "PreProteins" + os.sep + ligand + os.sep + protein + os.sep + "preped.pdbqt"
                # 2.3配置文件
                config_files = get_config_files("PreProteins" + os.sep + ligand + os.sep + protein)
                # 2.4输出文件
                output_count = 0
                for config_file in config_files:
                    output_file = "Output" + os.sep + ligand + os.sep + protein + os.sep + str(output_count) + ".pdbqt"
                    # 2.5对接
                    vina_dock(ligand_file, receptor_file, config_file, output_file)
                    output_count += 1
                # 2.6删除受体文件夹
                remove_dir("PreProteins" + os.sep + ligand + os.sep + protein)


if __name__ == '__main__':
    main = Main()
    main.run()
