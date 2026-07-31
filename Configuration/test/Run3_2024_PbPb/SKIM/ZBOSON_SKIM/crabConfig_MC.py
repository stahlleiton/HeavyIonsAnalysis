from CRABClient.UserUtilities import config
config = config()
config.section_('General')
date = '2026_07_11'
config.General.workArea = 'crab_projects/'+date+'/MC'
config.General.requestName = f'HiForest_EGREG_SSCorr_DYToEE_M_50_POWHEG_Hydjet_5p36TeV_2024Run3_'+date
config.General.transferOutputs = True
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = f'../forest_regstudy_MC.py'
config.JobType.inputFiles = ['../phoEleReg_Run3_2024_PbPb.db']
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 360
config.section_('Data')
config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/hintt/Run3_2024_PbPb/HiForest/EGREG/'+date+'/MC'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.inputDataset = '/DYto2E_MLL-50_TuneCP5_5p36TeV_powheg-pythia8/HINPbPbWinter24MiniAOD-141X_mcRun3_2024_realistic_HI_v14-v2/MINIAODSIM'
config.Data.outputDatasetTag = config.General.requestName
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_FR_*', 'T2_IT_*', 'T2_DE_*', 'T2_CH_*']
