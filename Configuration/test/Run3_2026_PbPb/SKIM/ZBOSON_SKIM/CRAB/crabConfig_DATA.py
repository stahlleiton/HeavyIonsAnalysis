from CRABClient.UserUtilities import config
config = config()
config.section_('General')
date = '2026_07_11'
config.General.workArea = 'crab_projects/'+date+'/DATA'
config.General.requestName = f'HiForest_EGREG_HIPhysicsRawPrime_HIRun2026A_PromptReco_'+date
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = f'../forest_regstudy_DATA.py'
config.JobType.inputFiles = ['../phoEleReg_Run3_2025_PbPb.db']
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 360
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/hintt/Run3_2026_PbPb/HiForest/EGREG/'+date+'/DATA'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50
config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions26HI/Collisions26HI_5p36TeV_404337_404926_golden.json'
config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/HIPhysicsRawPrime/phys_heavyions-HIPhysicsRawPrime_EGREG_HIRun2026_PromptReco_MINIAOD_2026_07_11-73ab4d95b2ca9ce320e485471ed6688e/USER'
config.Data.outputDatasetTag = config.General.requestName
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_FR_*', 'T2_IT_*', 'T2_DE_*', 'T2_CH_*']
