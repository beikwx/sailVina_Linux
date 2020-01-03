1. 将配体(pdbqt格式，单个/多个都可以)放到Ligands文件夹中。
2. 将受体(pdbqt格式，单个/多个都可以)放到Proteins文件夹中。
3. 在命令行输入如下指令：  
python3 ./main.py ./Proteins  
将进行对接。
4. 提取分数：  
python3 ./extract_scores.py  
将提取Output文件夹里面的分数  
5. 提取想要的结果  
python3 ./extract_output.py 要提取的最大分数  
结果提取到Final文件夹中。  

ps：PreProteins为工作目录，对接完后请手动删除。  
如果并行多个任务，建立多个Protein文件夹即可。
