# coding: utf-8

import shutil
import os
import sys


def extract_model(input_path, output_path):
    """
    从根文件夹中提取pdb文件。
    :param input_path: 要提取的根路径，比如C:\\models
    :param output_path: 输出路径，比如C:\\Output
    """
    # xx/12354/model/01/model.pdb --> 12345_01.pdb
    root_folders = os.listdir(input_path)
    for root_name in root_folders:
        # D:\\test\\outputs\\12345
        root_name_path = input_path + os.sep + root_name
        if os.path.isdir(root_name_path):
            # D:\\test\\outputs\\12345\\model
            # D:\\test\\outputs\\12345\\Untitled_Project_2019-07-01\\model
            sub_model_folders_path = root_name_path + os.sep + "model"
            if not os.path.exists(sub_model_folders_path):
                sub_folder = os.listdir(root_name_path)[0]
                sub_model_folders_path = root_name_path + os.sep + sub_folder + os.sep + "model"
            sub_model_folders = os.listdir(sub_model_folders_path)
            for sub_model_name in sub_model_folders:
                # D:\\test\\outputs\\12345\\model\\01
                sub_model_folder_path = sub_model_folders_path + os.sep + sub_model_name
                # D:\\test\\outputs\\12345\\model\\01\\model.pdb
                model_file = sub_model_folder_path + os.sep + "model.pdb"
                # D:\\test\\extract\\12345_01.pdb
                output_file = output_path + os.sep + root_name + "_" + sub_model_name + ".pdb"
                shutil.copyfile(model_file, output_file)


if __name__ == '__main__':
    # 读取命令行输入
    if len(sys.argv) == 1:
        sys.exit()
    elif len(sys.argv) != 3:
        sys.exit()
    else:
        extract_model(sys.argv[1], sys.argv[2])
