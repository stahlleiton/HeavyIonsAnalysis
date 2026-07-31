from CRABClient.UserUtilities import config
config = config()
config.section_('General')
date = '2026_07_11'
config.General.workArea = 'crab_projects/'+date
config.General.requestName = 'HIPhysicsRawPrime_MUTNP_HIRun2023_PromptReco_MINIAOD_'+date
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'skim_MUTNP.py'
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 360
config.JobType.numCores = 8
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/hintt/Run3_2023_PbPb/MINIAOD/MUTNP/'+date
config.Data.publication = True
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20
infile = 'zboson_promptskim.txt'
config.Data.userInputFiles = open(infile).readlines()
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'HIPhysicsRawPrime'
config.Data.outputDatasetTag = config.General.requestName
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Site.whitelist = ['T2_CH_*','T2_FR_*','T2_DE_*','T2_IT_*']
