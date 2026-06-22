from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

config = config()
config.section_('General')
tryMulti = True
date = '2025_4_16'
config.General.workArea = 'crab_projects/'+date+'/DATA'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_ParticleTransformer_run3_SKIM_DATA.py'
config.JobType.maxMemoryMB = 3500
config.JobType.maxJobRuntimeMin = 2749
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/cmst3/group/hintt/Run3_2024_ppRef/HiForest/'+date+'/DATA'
config.Data.publication = False
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Site.ignoreGlobalBlacklist = True # to fix issue of missing blocks
#config.Site.blacklist = ['T2_EE_Estonia']

def submit(config, dryrun):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

if tryMulti:
    config.Data.splitting = 'LumiBased'
    config.Data.unitsPerJob = 20
    config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_ppref_387474_387721_golden.json'
    config.Data.inputDBS = 'global'
    ## Submit the muon PDs
    for i in range(0, 4, 1):
        config.General.requestName = f'HiForest_PPRefSingleMuon{i}_Run2024J_PromptReco_v1_SKIM_'+date
        config.Data.inputDataset = f'/PPRefSingleMuon{i}/Run2024J-PromptReco-v1/MINIAOD'
        config.Data.outputDatasetTag = config.General.requestName
        submit(config = config, dryrun=False)
    ## Submit the electron PDs
    for i in range(0, 5, 1):
        config.General.requestName = f'HiForest_PPRefHardProbes{i}_Run2024J_PromptReco_v1_SKIM_'+date
        config.Data.inputDataset = f'/PPRefHardProbes{i}/Run2024J-PromptReco-v1/MINIAOD'
        config.Data.outputDatasetTag = config.General.requestName
        submit(config = config, dryrun=False)
