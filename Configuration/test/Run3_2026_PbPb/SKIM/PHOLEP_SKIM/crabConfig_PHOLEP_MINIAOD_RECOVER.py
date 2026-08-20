from CRABClient.UserUtilities import config
config = config()
config.section_('General')
date = '2026_08_07'
config.General.workArea = 'crab_projects/RECOVER_'+date
config.General.requestName = 'HIPhysicsRawPrime_PHOLEP_HIRun2026_PromptReco_MINIAOD_RECOVER_'+date
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'skim_PHOLEP.py'
config.JobType.maxMemoryMB = 6000
config.JobType.maxJobRuntimeMin = 1440
config.JobType.numCores = 8
config.section_('Data')
config.Data.outLFNDirBase = '/store/user/anstahll/hintt/Run3_2026_PbPb/MINIAOD/PHOLEP/'+date
config.Data.publication = True
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
infile = 'zboson_promptskim_RECOVER.txt'
config.Data.userInputFiles = open(infile).readlines()
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'HIPhysicsRawPrime'
config.Data.outputDatasetTag = 'HIPhysicsRawPrime_PHOLEP_HIRun2026_PromptReco_MINIAOD_'+date
config.section_('Site')
config.Site.storageSite = 'T2_US_Vanderbilt'
config.Site.whitelist = ['T2_BE_IIHE','T2_BE_UCL','T2_US_Wisconsin','T2_US_Florida','T2_ES_CIEMAT']
