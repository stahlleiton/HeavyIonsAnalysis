import json

dir="crab_projects/2026_08_30/DATA/PHOLEP/crab_HiForest_HIPhysicsRawPrime_HIRun2023A_PromptReco_v2_PHOLEPSKIM_2026_08_30/results/"

with open(dir+"filesToProcess.json", "r") as f1:
    file1 = json.loads(f1.read())

with open(dir+"processedFiles.json", "r") as f2:
    file2 = json.loads(f2.read())

flist = []
for item in file1:
    if item not in file2:
        flist += file1[item]

with open("recover_files.txt", "a") as myfile:
    for f in flist:
        myfile.write(f+"\n")

print(len(flist) / 4)
