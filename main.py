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
        self.ligand = None
        self.proteins_dir = None
        self.output_path = None

    def run(self):

        # 1.读取命令行输入
        # 输入的配体放在./Ligands文件夹
        # 输入的受体放在./Proteins文件夹
        # 输出在./Output文件夹
        self.ligand = "." + os.sep + "Ligands"
        self.proteins_dir = "." + os.sep + "Proteins"
        pro_proteins_dir = "." + os.sep + "PreProteins"
        self.output_path = "." + os.sep + "Output"

        # 2.将pdbqt文件放入文件夹
        # 复制蛋白到另外的目录
        copy_proteins(self.proteins_dir, pro_proteins_dir)
        receptors_dir = proteins2dir(pro_proteins_dir)

        # 3.生成config.txt文件。
        # print("----------------------------------------准备生成对接配置文件----------------------------------------")
        for receptor_dir in receptors_dir:
            receptor_file = receptor_dir + os.sep + "preped.pdbqt"
            gen_config(receptor_file, self.ligand)
        # print("----------------------------------------配置文件生成完毕----------------------------------------")

        # print("----------------------------------------准备对接----------------------------------------")

        # 4.进行对接
        for receptor_dir in receptors_dir:
            # 此时receptor_dir = ".\Proteins\01
            # current_receptor = receptor_dir.split(os.sep)[-1]
            # print("------------------------------------------------------------")
            # print("准备对接：" + current_receptor)
            # print("------------------------------------------------------------")

            # 受体文件
            receptor_file = receptor_dir + os.sep + "preped.pdbqt"

            # 配置文件
            config_files = get_config_files(receptor_dir)

            # 创建输出文件夹
            output_dir = self.output_path + os.sep + receptor_dir.split(os.sep)[-1]
            mk_output_dir(output_dir)

            output_count = 0
            for config_file in config_files:
                output_file = output_dir + os.sep + str(output_count) + ".pdbqt"
                # print("当前配置文件:" + config_file)
                vina_dock(self.ligand, receptor_file, config_file, output_file)
                # print("------------------------------------------------------------")
                output_count += 1

            # print("------------------------------------------------------------")
            # print("对接完毕：" + current_receptor)
            # print("------------------------------------------------------------")

        # 5.结果分析，输出分数最低的结果

        best_dict = get_best_scores(read_root_folder_scores(self.output_path, mode=1))
        score_file = self.output_path + os.sep + "output.txt"
        create_scores_file(score_file, best_dict)
        # print("输出分数到%s" % score_file)


if __name__ == '__main__':
    main = Main()
    main.run()
