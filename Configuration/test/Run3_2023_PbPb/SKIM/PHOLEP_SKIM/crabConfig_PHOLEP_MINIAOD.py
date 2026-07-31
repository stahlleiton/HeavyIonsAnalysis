from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

config = config()
config.section_('General')
date = '2026_07_21'
config.General.workArea = 'crab_projects/'+date
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'skim_PHOLEP.py'
config.JobType.inputFiles = ['phoEleReg_Run3_2023_PbPb.db']
config.JobType.maxMemoryMB = 4500
config.JobType.maxJobRuntimeMin = 1749
config.JobType.numCores = 8
config.section_('Data')
config.Data.outLFNDirBase = '/store/user/anstahll/hintt/Run3_2023_PbPb/MINIAOD/PHOLEP/'+date
config.Data.publication = True
config.Data.outputDatasetTag = 'HIPhysicsRawPrime_PHOLEP_HIRun2023_PromptReco_MINIAOD_'+date
config.section_('Site')
config.Site.storageSite = 'T2_US_Vanderbilt'
config.Site.ignoreGlobalBlacklist = True # to fix issue of missing blocks
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*', 'T1_FR_*', 'T2_US_MIT', 'T2_FR_*', 'T2_US_*', 'T2_CH_*']
config.Site.blacklist = ['T2_CN_*', 'T2_TW_*', 'T2_DE_*', 'T2_EE_*']

def submit(config, dryrun):
    try:
        crabCommand('submit', config = config, dryrun=dryrun)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 25
config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions23HI/Cert_Collisions2023HI_374288_375823_Golden.json'
config.Data.inputDBS = 'global'
## Submit the muon PDs
for i in range(0, 32, 1):
    config.General.requestName = f'HIPhysicsRawPrime{i}_PHOLEP_HIRun2023_PromptReco_MINIAOD_'+date
    config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2023A-PromptReco-v2/MINIAOD'
    submit(config = config, dryrun=False)
