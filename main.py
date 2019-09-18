# coding: utf-8

import sys

from check import *
from dock_processor import vina_dock
from pdb_processor import proteins2dir
from pdb_processor import gen_config
from file_processor import get_config_files, create_scores_file
from file_processor import mk_output_dir
from file_processor import get_best_scores
from Tools.read_scores import read_root_folder_scores


class Main:

    def __init__(self):
        self.ligand = None
        self.proteins_dir = None
        self.output_path = None

    def run(self):

        # 1.读取命令行输入
        # 例如输入 main.py ./Proteins ./Ligands/aspirin.pdbqt
        if not check_cmd_para(sys.argv):
            sys.exit()
        else:
            self.ligand = sys.argv[1]
            self.proteins_dir = sys.argv[2]
            self.output_path = sys.argv[3]

        # print("选定的配体是：" + self.ligand)
        # print("选定的受体目录是：" + self.proteins_dir)

        # 2.将pdbqt文件放入文件夹
        # 此时受体目录"./Proteins/pdb/preped.pdbqt
        receptors_dir = proteins2dir(self.proteins_dir)

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
            current_receptor = receptor_dir.split(os.sep)[-1]
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
