from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

config = config()
config.section_('General')
tryMulti = True
date = '2026_05_17'
config.General.workArea = 'crab_projects/'+date+'/DATA_PHOLEPT'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_ParticleTransformer_run3_SKIM_DATA.py'
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 1749
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/cmst3/group/hintt/Run3_2024_PbPb/HiForest/'+date+'/DATA_PHOLEPT'
config.Data.publication = False
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Site.ignoreGlobalBlacklist = True # to fix issue of missing blocks
#config.Site.blacklist = ['T2_EE_Estonia']
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*', 'T1_FR_*', 'T2_US_MIT', 'T2_FR_*', 'T2_US_Vanderbilt', 'T2_CH_CERN']
config.Site.blacklist = ['T2_CN_*', 'T2_TW_*', 'T2_DE_*']

def submit(config, dryrun):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

if tryMulti:
    config.Data.splitting = 'LumiBased'
    config.Data.unitsPerJob = 25#100
    config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions24HI/Cert_Collisions2024_HI_387853_388784_Golden.json'
    config.Data.inputDBS = 'global'
    ## Submit the muon PDs
    for i in range(0, 15, 1):
        config.General.requestName = f'HiForest_HIPhysicsRawPrime{i}_HIRun2024A_PromptReco_v1_SKIM_'+date
        config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2024A-PromptReco-v1/MINIAOD'
        config.Data.outputDatasetTag = config.General.requestName
        submit(config = config, dryrun=False)
    for i in range(15, 60, 1):
        if i == 36:
            config.General.requestName = f'HiForest_HIPhysicsRawPrime{i}_HIRun2024A_OfflinePromptReco_v2_SKIM_'+date
            config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2024A-OfflinePromptReco-v2/MINIAOD'
        else:
            config.General.requestName = f'HiForest_HIPhysicsRawPrime{i}_HIRun2024A_OfflinePromptReco_v1_SKIM_'+date
            config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2024A-OfflinePromptReco-v1/MINIAOD'
        config.Data.outputDatasetTag = config.General.requestName
        submit(config = config, dryrun=False)
    for i in range(0, 60, 1):
        config.General.requestName = f'HiForest_HIPhysicsRawPrime{i}_HIRun2024B_PromptReco_v1_SKIM_'+date
        config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2024B-PromptReco-v1/MINIAOD'
        config.Data.outputDatasetTag = config.General.requestName
        submit(config = config, dryrun=False)
    for i in range(0, 60, 1):
        config.General.requestName = f'HiForest_HIPhysicsRawPrime{i}_HIRun2024B_PromptReco_v2_SKIM_'+date
        config.Data.inputDataset = f'/HIPhysicsRawPrime{i}/HIRun2024B-PromptReco-v2/MINIAOD'
        config.Data.outputDatasetTag = config.General.requestName
        submit(config = config, dryrun=False)
else:
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 40
    infile = 'minbias_prompt_v2.txt'
    config.Data.userInputFiles = open(infile).readlines()
    config.Data.totalUnits = len(config.Data.userInputFiles)
    config.Data.outputPrimaryDataset = 'HIPhysicsRawPrime'
    config.Site.whitelist = ['T2_US_Vanderbilt']
    config.General.requestName = 'HiForest_HIPhysicsRawPrime_HIRun2023A_PromptReco_v2_SKIM_'+date
    config.Data.outputDatasetTag = config.General.requestName
    crabCommand('submit', config = config, dryrun=False)
