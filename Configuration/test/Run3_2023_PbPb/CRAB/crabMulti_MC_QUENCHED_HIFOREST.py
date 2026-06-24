from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

config = config()
config.section_('General')
date = '2025_2_03'
config.General.workArea = 'crab_projects/'+date+'/MC_Quenched'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_ParticleTransformer_Quenched_run3_MC.py'
config.JobType.numCores = 1
config.section_('Data')
config.Data.splitting = 'LumiBased'
config.Data.outLFNDirBase = '/store/group/cmst3/group/hintt/Run3/HiForest/'+date+'/MC'
config.Data.publication = False
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*', 'T2_US_Caltech', 'T2_US_Purdue', 'T2_US_Vanderbilt', 'T1_FR_*', 'T2_FR_*', 'T2_CH_CERN']

dataMap = {}
dataMap["TT_hvq_POWHEG_Hydjet_Official"] = { "PD": "/TT_TuneCP5_5p36TeV_powheg-pythia8/HINPbPbSpring23MiniAOD-132X_mcRun3_2023_realistic_HI_v9-v3/MINIAODSIM", "Units": 10, "Memory": 3900, "RunTime": 2749 }

## Submit PDs
for key, val in dataMap.items():
    config.General.requestName = f'HiForest_Quenched_{key}_5p36TeV_TuneCP5_2023Run3_'+date
    config.Data.inputDataset = val["PD"]
    config.Data.inputDBS = 'global' if ("HINPbPbSpring23MiniAOD" in val["PD"]) else 'phys03'
    config.Data.unitsPerJob = val["Units"]
    config.JobType.maxMemoryMB = val["Memory"]
    config.JobType.maxJobRuntimeMin = val["RunTime"]
    config.Data.outputDatasetTag = config.General.requestName
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))
