from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

config = config()
config.section_('General')
date = '2026_05_10'
config.General.workArea = 'crab_projects/'+date+'/MC'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_run3_pO_MC.py'
config.JobType.maxMemoryMB = 3500
config.JobType.maxJobRuntimeMin = 2749
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/CERN/pO2025/HiForest/'+date+'/MC'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'

def submit(config, dryrun):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

dataMap = {}
dataMap["MinimumBias_v11_PYTHIA8"] = { "PD": "/PYTHIA8_9p62TeV_2025Run3/anstahll-MinimumBias_v11_PYTHIA8_pO_9p62TeV_TuneCP5_2025Run3_RECO_2026_05_08-5dcb09b56697ad402530677e0cf6bfd5/USER", "Units": 6, "Memory": 3000,   "RunTime": 2749 }
dataMap["MinimumBias_v13_PYTHIA8"] = { "PD": "/PYTHIA8_9p62TeV_2025Run3/anstahll-MinimumBias_v13_PYTHIA8_pO_9p62TeV_TuneCP5_2025Run3_RECO_2026_05_08-5dcb09b56697ad402530677e0cf6bfd5/USER", "Units": 6, "Memory": 3000,   "RunTime": 2749 }
dataMap["MinimumBias_v14_PYTHIA8"] = { "PD": "/PYTHIA8_9p62TeV_2025Run3/anstahll-MinimumBias_v14_PYTHIA8_pO_9p62TeV_TuneCP5_2025Run3_RECO_2026_05_08-5dcb09b56697ad402530677e0cf6bfd5/USER", "Units": 6, "Memory": 3000,   "RunTime": 2749 }
dataMap["MinimumBias_v15_PYTHIA8"] = { "PD": "/PYTHIA8_9p62TeV_2025Run3/anstahll-MinimumBias_v15_PYTHIA8_pO_9p62TeV_TuneCP5_2025Run3_RECO_2026_05_08-5dcb09b56697ad402530677e0cf6bfd5/USER", "Units": 6, "Memory": 3000,   "RunTime": 2749 }

## Submit PDs
for key, val in dataMap.items():
    config.General.requestName = f'HiForest_{key}_pO_9p62TeV_2025Run3_'+date
    config.Data.inputDataset = val["PD"]
    config.Data.inputDBS = 'global' if ("HINPbPbSpring23MiniAOD" in val["PD"]) else 'phys03'
    config.Data.unitsPerJob = val["Units"]
    config.JobType.maxMemoryMB = val["Memory"]
    config.JobType.maxJobRuntimeMin = val["RunTime"]
    config.Data.outputDatasetTag = config.General.requestName
    submit(config = config, dryrun=False)
