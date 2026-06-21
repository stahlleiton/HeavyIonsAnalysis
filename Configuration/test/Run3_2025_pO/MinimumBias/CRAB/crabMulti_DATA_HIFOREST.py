from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

config = config()
config.section_('General')
date = '2026_05_09'
config.General.workArea = 'crab_projects/'+date+'/DATA'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_run3_pO_DATA.py'
config.JobType.maxMemoryMB = 3000
config.JobType.maxJobRuntimeMin = 2749
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/CERN/pO2025/HiForest/'+date+'/DATA'
config.Data.publication = False
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Site.ignoreGlobalBlacklist = True # to fix issue of missing blocks

def submit(config, dryrun):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10
config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions25pO/pO_golden.json'
config.Data.inputDBS = 'global'
## Submit the PDs
for i in range(0, 1, 1):
    config.General.requestName = f'HiForest_IonPhysics{i}_pORun2025_PromptReco_v1_MB_'+date
    config.Data.inputDataset = f'/IonPhysics{i}/pORun2025-PromptReco-v1/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    submit(config = config, dryrun=False)
