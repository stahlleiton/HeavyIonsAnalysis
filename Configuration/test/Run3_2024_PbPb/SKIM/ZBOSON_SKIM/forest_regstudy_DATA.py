### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_2024_cff import Run3_pp_on_PbPb_2024
process = cms.Process('HiForest', Run3_pp_on_PbPb_2024)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 141X, data")

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/group/phys_heavyions/anstahll/hintt/Run3_2024_PbPb/MINIAOD/EGREG/2026_07_11/HIPhysicsRawPrime/HIPhysicsRawPrime_EGREG_HIRun2024_PromptReco_MINIAOD_2026_07_11/260711_020734/0009/miniaod_9055.root'),
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
process.GlobalTag = GlobalTag(process.GlobalTag, '141X_dataRun3_Prompt_forHI_NominalCentrality', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

###############################################################################

# Define centrality binning
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

###############################################################################

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestMiniAOD.root"))

###############################################################################

# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_data_2024_skimmed
process.hltobject.triggerNames = trigger_list_data_2024_skimmed
from HeavyIonsAnalysis.EventAnalysis.dummybranches_cff import dummy_branches_for_PbPb_2024_HLT
process.hltanalysis.hltdummybranches = dummy_branches_for_PbPb_2024_HLT

################################
# electrons, photons, muons
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.load('HeavyIonsAnalysis.EGMAnalysis.correctedSSPatElectronProducer_cfi')
process.load('HeavyIonsAnalysis.EGMAnalysis.correctedSSPatPhotonProducer_cfi')
correctionFile = "HeavyIonsAnalysis/EGMAnalysis/data/Run3_2024_PbPb/egreg26_scaleSmear_Run3_2024_PbPb.json.gz"
process.correctedElectrons = process.correctedSSPatElectronProducer.clone(src = "slimmedElectrons", correctionFile = correctionFile)
process.correctedPhotons = process.correctedSSPatPhotonProducer.clone(src = "slimmedPhotons", correctionFile = correctionFile)
process.ggHiNtuplizer.electronSrc = "correctedElectrons"
process.ggHiNtuplizer.photonSrc = "correctedPhotons"
process.ggHiNtuplizer.muonSrc = "slimmedMuons"
process.egammaSequence = cms.Sequence(process.correctedPhotons * process.correctedElectrons * process.ggHiNtuplizer)
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.centralityBin +
    process.hiEvtAnalyzer +
    process.hltanalysis +
    process.hltobject +
    process.egammaSequence
    )

#########################
# Apply egamma regression
#########################
from HeavyIonsAnalysis.EGMAnalysis.applyEgammaRegression_cfi import applyEgammaRegression
process = applyEgammaRegression(process, era = "Run3_2024_PbPb")

#########################
# Event Selection -> add the needed filters here
#########################

process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.load('HeavyIonsAnalysis.EventAnalysis.hffilter_cfi')
process.pAna = cms.EndPath(process.skimanalysis)
