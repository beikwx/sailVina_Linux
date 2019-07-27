import sys

from check import *
from dock_processor import batch_dock


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

        # 2.进行对接
        batch_dock(self.ligand, self.proteins_dir)


if __name__ == '__main__':
    main = Main()
    main.run()
