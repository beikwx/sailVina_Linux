import os

from Tools.read_scores import read_root_folder_scores
from file_processor import get_best_scores, create_scores_file

output_folder = "." + os.sep + "Output"
output_txt_list = []

for ligand in os.listdir(output_folder):
    if ligand.endswith(".txt"):
        continue
    best_dict = get_best_scores(read_root_folder_scores(output_folder + os.sep + ligand, mode=1))
    score_file = output_folder + os.sep + ligand + os.sep + "output.txt"
    # 每个配体文件夹创建输出文本
    create_scores_file(score_file, best_dict)

    # 输出文本路径
    output_txt_list.append(score_file)

scores = ["Ligands\tProteins\tbest_ligand\tscores\n"]
for output_txt in output_txt_list:
    with open(output_txt, "r") as f:
        text = f.readline()
        while text:
            if text == "receptor_name\tligand_name\tscores\n":
                text = f.readline()
                continue
            # Output / aspirin1 / output.txt
            new_text = output_txt.split(os.sep)[-2] + "\t" + text
            scores.append(new_text)
            text = f.readline()

scores_file = output_folder + os.sep + "scores.txt"
with open(scores_file, "w") as f:
    f.writelines(scores)
