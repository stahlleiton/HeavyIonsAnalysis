import json

dir="crab_projects/2026_08_07/crab_HIPhysicsRawPrime_PHOLEP_HIRun2023_PromptReco_MINIAOD_2026_08_07/results/"

with open(dir+"filesToProcess.json", "r") as f1:
    file1 = json.loads(f1.read())

with open(dir+"processedFiles.json", "r") as f2:
    file2 = json.loads(f2.read())

flist = []
for item in file1:
    if item not in file2:
        flist += file1[item]

with open("recover_minbias_promptskim.txt", "a") as myfile:
    for f in flist:
        myfile.write(f+"\n")

print(len(flist) / 20)
