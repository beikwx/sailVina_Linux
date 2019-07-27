import os


def batch_dock(ligand, proteins_dir):

    protein = proteins_dir + os.sep + "preped.pdbqt"
    config = proteins_dir + os.sep + "config.txt"

    # windows版本
    # cmd = "." + os.sep + "sources" + os.sep + "vina.exe --ligand %s " \
    #                                           "--receptor %s " \
    #                                           "--config %s" % \
    #       (ligand, protein, config)

    # linux版本
    cmd = "vina --ligand %s --receptor %s --config %s" % \
          (ligand, protein, config)

    # print(cmd)
    os.system(cmd)
