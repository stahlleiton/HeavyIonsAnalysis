### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run2_2016_UPC_cff import Run2_2016_UPC
process = cms.Process('HiForest', Run2_2016_UPC)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 141X, data")

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/hidata/PARun2016C/ZeroBias/MINIAOD/16Dec2024-v1/2540000/3829990c-9382-4255-b5f5-b4f04717deb6.root'),
#        /store/hidata/PARun2016C/PAForward/MINIAOD/16Dec2024-v1/2820001/ff661707-3239-44c5-828e-65c2be3e20cd.root'),
)

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

###############################################################################

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '141X_dataRun2_v3', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

###############################################################################

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestMiniAOD.root"))

#########################
# ZDC RecHit Producer && Analyzer
#########################
# to prevent crash related to HcalSeverityLevelComputerRcd record
process.load("RecoLocalCalo.HcalRecAlgos.hcalRecAlgoESProd_cfi")
from RecoLocalCalo.HcalRecProducers.HcalHitReconstructor_zdc_cfi import zdcreco
from HeavyIonsAnalysis.ZDCAnalysis.ZDCRecHitAnalyzerHC_cfi import zdcanalyzer
process.zdcreco = zdcreco.clone(
    digiLabelhcal = cms.InputTag("hcalDigis:ZDC"),
)
from RecoLocalCalo.HcalRecProducers.ZdcHitReconstructor_Run3 import ZdcHitReconstructor_Run3
process.zdcreco = ZdcHitReconstructor_Run3(
    # Modo offline 2023 (Ts2-Ts1) — recomendado para rereco Run2 en CMSSW 14
    correctionMethodEM  = cms.int32(0),
    correctionMethodHAD = cms.int32(0),
    ootpuRatioEM        = cms.double(-1),
    ootpuRatioHAD       = cms.double(-1),
    ootpuFracEM         = cms.double(1.0),
    ootpuFracHAD        = cms.double(1.0),
    skipRPD             = cms.bool(True),
)
process.zdcanalyzer = zdcanalyzer.clone(
   ZDCRecHitSource = 'zdcreco',
   doZdcDigis = True,
   doHardcodedRPD = False
)

###############################################################################
# main forest sequence
process.forest = cms.Path(
	process.zdcreco +
	process.zdcanalyzer
    )
