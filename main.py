# coding: utf-8

from check import *
from dock_processor import vina_dock
from pdb_processor import proteins2dir
from pdb_processor import gen_config
from file_processor import get_config_files, create_scores_file
from file_processor import mk_output_dir
from file_processor import get_best_scores, copy_proteins
from Tools.read_scores import read_root_folder_scores


class Main:

    def __init__(self):
        self.ligands = None
        self.proteins_dir = None
        self.output_path = None

    def run(self):

        # 1.读取配体和受体
        # 输入的配体放在./Ligands文件夹
        # 输入的受体放在./Proteins文件夹
        # 输出在./Output文件夹
        self.ligands = "." + os.sep + "Ligands"
        self.proteins_dir = "." + os.sep + "Proteins"
        pre_proteins_dir = "." + os.sep + "PreProteins"
        self.output_path = "." + os.sep + "Output"

        # 2.根据配体和受体建立文件夹。
        for ligand in os.listdir(self.ligands):
            if not ligand.endswith(".pdbqt"):
                continue
            ligand_path = "." + os.sep + "Ligands" + os.sep + ligand
            ligand_folder = pre_proteins_dir + os.sep + ligand[:-6]
            # 在PreProteins中创建文件夹，以配体命名
            mk_output_dir(ligand_folder)
            # 将受体复制到配体文件夹中
            copy_proteins(self.proteins_dir, ligand_folder)
            # 将受体移动到文件夹中，改名
            receptors_dir = proteins2dir(ligand_folder)

            # 3.生成config.txt文件。
            for receptor_dir in receptors_dir:
                receptor_file = receptor_dir + os.sep + "preped.pdbqt"
                gen_config(receptor_file, ligand_path)

            # 4.进行对接
            for receptor_dir in receptors_dir:
                # 此时receptor_dir = ".\PreProteins\ligand1\01
                # current_receptor = receptor_dir.split(os.sep)[-1]

                # 受体文件
                receptor_file = receptor_dir + os.sep + "preped.pdbqt"

                # 配置文件
                config_files = get_config_files(receptor_dir)

                # 创建输出文件夹
                output_dir = self.output_path + os.sep + ligand[:-6] + os.sep + receptor_dir.split(os.sep)[-1]
                mk_output_dir(output_dir)

                output_count = 0
                for config_file in config_files:
                    output_file = output_dir + os.sep + str(output_count) + ".pdbqt"
                    # print("当前配置文件:" + config_file)
                    vina_dock(ligand_path, receptor_file, config_file, output_file)
                    # print("------------------------------------------------------------")
                    output_count += 1

                # 5.结果分析，输出分数最低的结果

            best_dict = get_best_scores(read_root_folder_scores(self.output_path + os.sep + ligand[:-6], mode=1))
            score_file = self.output_path + os.sep + ligand[:-6] + os.sep + "output.txt"
            create_scores_file(score_file, best_dict)


if __name__ == '__main__':
    main = Main()
    main.run()
