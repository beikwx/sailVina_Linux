import sys
import os
import shutil
from help_text import EXTRACT_INFO


if __name__ == '__main__':
    # 直接输入命令
    if len(sys.argv) == 1:
        print(EXTRACT_INFO)
        sys.exit()
    if len(sys.argv) != 2:
        print("Parameter error.\n" + EXTRACT_INFO)
        sys.exit()

    scores_file = "." + os.sep + "Output" + os.sep + "scores.txt"
    maximum_score = float(sys.argv[1])
    with open(scores_file, "r") as f:
        # 跳过第一行
        f.readline()
        text = f.readline()
        while text:
            ligand, protein, best, scores = text.split()

            if float(scores) <= maximum_score:
                # 复制配体
                file_path = "." + os.sep + "Output" + os.sep + ligand + os.sep + protein + os.sep + best
                output_dir = "." + os.sep + "Final" + os.sep + ligand + os.sep + protein
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                shutil.copy(file_path, output_dir)

            text = f.readline()
