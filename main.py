import os
import sys

import check


class Main:

    def __init__(self):
        self.ligand = None
        self.proteins_dir = None

    def run(self):
        # 1.读取命令行输入
        if not check.check_cmd_para(sys.argv):
            sys.exit()
        else:
            self.ligand = sys.argv[1]
            self.proteins_dir = sys.argv[2]

        print("ligand = " + self.ligand)
        print("proteins = " + self.proteins_dir)

        # 2.进行对接
        protein = self.proteins_dir + os.sep + "preped.pdbqt"
        config = self.proteins_dir + os.sep + "config.txt"

        # windows版本
        # cmd = "." + os.sep + "sources" + os.sep + "vina.exe --ligand %s " \
        #                                           "--receptor %s " \
        #                                           "--config %s" % \
        #       (self.ligand, protein, config)

        # linux版本
        cmd = "vina --ligand %s --receptor %s --config %s" % \
              (self.ligand, protein, config)

        # print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    main = Main()
    main.run()
