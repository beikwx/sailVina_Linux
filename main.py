import sys

from check import *
from dock_processor import batch_dock
from pdb_processor import proteins2dir


class Main:

    def __init__(self):
        self.ligand = None
        self.proteins_dir = None

    def run(self):

        # 1.读取命令行输入
        if not check_cmd_para(sys.argv):
            sys.exit()
        else:
            self.ligand = sys.argv[1]
            self.proteins_dir = sys.argv[2]

        print("选定的配体是：" + self.ligand)
        print("选定的受体目录是：" + self.proteins_dir)

        # 2.将pdbqt文件放入文件夹
        proteins2dir(self.proteins_dir)

        # Todo 3.生成config.txt文件。
        # 确定对接位点，可能会生成多个config文件

        # Todo 4.进行对接
        # 多个配置文件分别对接
        # 显示对接进度
        # 确定输出文件

        # Todo 5.结果分析
        # 对所有输出文件进行汇总，同一类的多个对接结果算一个
        # 输出所有分数(txt/excel)

        # Todo 6.提取结果
        # 从确定的n个结果中输出（配体/受体/复合物）


if __name__ == '__main__':
    main = Main()
    main.run()
