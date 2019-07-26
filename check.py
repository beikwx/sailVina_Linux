import help_text
import os


def check_cmd_para(cmd_para):
    # 直接运行
    if len(cmd_para) == 1:
        print(help_text.INFO)
        return 0
    # 参数个数不正确
    elif len(cmd_para) != 3:
        print("输入的参数个数不正确，请检查命令并重新输入")
        print(help_text.INFO)
        return 0
    # 检查文件名
    else:
        ligand = cmd_para[1]
        proteins = cmd_para[2]
        if check_file(ligand) and check_dir(proteins):
            if check_format(ligand, "pdbqt"):
                return 1
            else:
                return 0
        else:
            return 0


def check_dir(filename):
    """

    :param filename: 判断的名字
    :return: 如果是文件夹，如果存在返回1，不存在返回0。不是文件夹返回0。
    """
    if os.path.isdir(filename):
        if os.path.exists(filename):
            return 1
        else:
            print("文件夹不存在")
            return 0
    else:
        print("不是文件夹")
        return 0


def check_file(filename):
    """

    :param filename: 判断的名字
    :return: 是文件返回1，不是返回0
    """
    if os.path.isfile(filename):
        return 1
    else:
        print(filename + "不是文件")
        return 0


def check_format(filename, target_format):
    """

    :param filename: 文件名，必须是文件
    :param target_format: 匹配的后缀
    :return: 是否是指定格式
    """
    file_format = os.path.splitext(filename)[-1]
    if file_format != "." + target_format:
        print(filename + "文件不是" + target_format + "格式")
        return 0
    else:
        return 1
