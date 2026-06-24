from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException
import os.path
config = config()
config.section_('General')
date = '2024_12_26'
config.General.workArea = 'crab_projects/'+date+'/DATA_2nd_RECOVERY'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_ParticleTransformer_run3_SKIM_DATA.py'
config.JobType.maxMemoryMB = 2400
config.JobType.maxJobRuntimeMin = 720
config.section_('Data')
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/cmst3/group/hintt/Run3/HiForest/'+date+'/DATA'
config.Data.publication = False
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
#config.Site.ignoreGlobalBlacklist = True # to fix issue of missing blocks
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*', 'T2_US_Caltech', 'T2_US_Purdue', 'T2_US_Vanderbilt', 'T1_FR_*', 'T2_FR_*', 'T2_CH_CERN']

## Submit the PDs
for i in [22, 25]:
    config.General.requestName = f'HiForest_HIPhysicsRawPrime{i}_HIRun2023A_PromptReco_v2_SKIM_'+date+'_2nd_RECOVERY'
    config.Data.lumiMask = f'crab_projects/{date}/DATA_RECOVERY/crab_HiForest_HIPhysicsRawPrime{i}_HIRun2023A_PromptReco_v2_SKIM_{date}_RECOVERY/results/notFinishedLumis.json'
    if not os.path.exists(config.Data.lumiMask):
        continue
    config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2023A-PromptReco-v2/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))
