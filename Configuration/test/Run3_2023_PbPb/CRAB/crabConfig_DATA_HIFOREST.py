from CRABClient.UserUtilities import config

config = config()
config.section_('General')
date = '2026_08_26'
config.General.requestName = f'HiForest_HIPhysicsRawPrime_HIRun2023A_PromptReco_v2_PHOLEPSKIM_'+date
config.General.workArea = 'crab_projects/'+date+'/DATA/PHOLEP'
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../forest_miniAOD_ParticleTransformer_run3_DATA.py'
config.JobType.inputFiles = ['../phoEleReg_Run3_2023_PbPb.db']
config.JobType.maxMemoryMB = 3000
config.JobType.maxJobRuntimeMin = 720
config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.inputDataset = '/HIPhysicsRawPrime/anstahll-HIPhysicsRawPrime_PHOLEP_HIRun2023_PromptReco_MINIAOD_2026_08_07-e43f75fe31bec706cb7bbfec94d6b42e/USER'
config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions23HI/Cert_Collisions2023HI_374288_375823_Golden.json'
config.Data.inputDBS = 'phys03'
config.Data.outLFNDirBase = '/store/group/cmst3/group/hintt/Run3_2023_PbPb/HiForest/'+date+'/DATA/PHOLEP'
config.Data.publication = False
config.Data.outputDatasetTag = config.General.requestName
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*', 'T1_FR_*', 'T2_US_MIT', 'T2_FR_*', 'T2_US_Vanderbilt', 'T2_CH_CERN']
config.Site.blacklist = ['T2_CN_*', 'T2_TW_*', 'T2_DE_*', 'T2_EE_*']
