### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_2024_ppRef_cff import Run3_2024_ppRef
process = cms.Process('HiForest', Run3_2024_ppRef)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 141X, data")

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        'root://xrootd-cms.infn.it//store/data/Run2024J/PPRefSingleMuon2/MINIAOD/PromptReco-v1/000/387/606/00000/cc433506-1095-4592-804e-e7e0a4d5bd69.root'
    ),
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
process.GlobalTag = GlobalTag(process.GlobalTag, '141X_dataRun3_Prompt_v4', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

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
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')
process.metFilters = process.skimanalysis.clone(hltresults = "TriggerResults::RECO")

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_data_2024_ppref_skimmed
process.hltobject.triggerNames = trigger_list_data_2024_ppref_skimmed

process.hiEvtAnalyzer.doCentrality = False
process.hiEvtAnalyzer.doHFfilters = False

process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
################################
# electrons, photons, muons
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.ggHiNtuplizer.doPhotons = False
################################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.hiFJSoftKillerAnalyzer_cff')
################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
# muons
process.ggHiNtuplizer.muonSrc = "slimmedMuons"
process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
###############################################################################

# ZDC RecHit Producer
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018Producer_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018RecHit_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi')

process.zdcdigi.SOI = cms.untracked.int32(2)
process.zdcanalyzer.doZDCRecHit = False
process.zdcanalyzer.doZDCDigi = True
process.zdcanalyzer.zdcRecHitSrc = cms.InputTag("QWzdcreco")
process.zdcanalyzer.zdcDigiSrc = cms.InputTag("hcalDigis", "ZDC")
process.zdcanalyzer.calZDCDigi = False
process.zdcanalyzer.verbose = False
process.zdcanalyzer.nZdcTs = cms.int32(6)

###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hiEvtAnalyzer +
    process.hltanalysis +
    process.hltobject +
    process.l1object +
    process.unpackedTracksAndVertices +
    process.particleFlowAnalyser +
    process.ggHiNtuplizer +
    process.hiFJSoftKillerAnalyzer +
    process.metFilters +
    process.zdcanalyzer
    )

#customisation
process.particleFlowAnalyser.ptMin = 0.0
process.ggHiNtuplizer.muonPtMin = 0.0

# Select the types of jets filled
jetPtMin = 15
jetAbsEtaMax = 2.5

# Choose which additional information is added to jet trees
doHIJetID = True             # Fill jet ID and composition information branches
doWTARecluster = True        # Add jet phi and eta for WTA axis

# add candidate tagging
for jetR in [0.3, 0.4]:
    R = str(int(jetR*10))
    from HeavyIonsAnalysis.JetAnalysis.deepNtupleSettings_cff import candidateBtaggingMiniAOD
    candidateBtaggingMiniAOD(process, isMC = False, jetPtMin = jetPtMin, jetR = jetR, jetCorrLevels = ['L2Relative', 'L2L3Residual'])

    # setup jet analyzer
    setattr(process,f'akCs{R}PFJetAnalyzer', process.akCs4PFJetAnalyzer.clone())
    getattr(process,f'akCs{R}PFJetAnalyzer').jetTag = f'selectedUpdatedPatJetsAKCs{R}DeepFlavour'
    getattr(process,f'akCs{R}PFJetAnalyzer').jetName = f'akCs{R}PF'
    getattr(process,f'akCs{R}PFJetAnalyzer').rParam = jetR
    getattr(process,f'akCs{R}PFJetAnalyzer').doHiJetID = doHIJetID
    getattr(process,f'akCs{R}PFJetAnalyzer').doWTARecluster = doWTARecluster
    getattr(process,f'akCs{R}PFJetAnalyzer').useNewBtaggers = True
    getattr(process,f'akCs{R}PFJetAnalyzer').jetPtMin = jetPtMin
    getattr(process,f'akCs{R}PFJetAnalyzer').useRawPt = True
    getattr(process,f'akCs{R}PFJetAnalyzer').jetAbsEtaMax = cms.untracked.double(jetAbsEtaMax)
    getattr(process,f'akCs{R}PFJetAnalyzer').pfJetProbabilityBJetTag = cms.untracked.string(f"pfJetProbabilityBJetTagsAKCs{R}DeepFlavour")
    getattr(process,f'akCs{R}PFJetAnalyzer').pfDeepCSVJetTags = cms.untracked.string(f"pfDeepCSVJetTagsAKCs{R}DeepFlavour")
    getattr(process,f'akCs{R}PFJetAnalyzer').pfDeepFlavourJetTags = cms.untracked.string(f"pfDeepFlavourJetTagsAKCs{R}DeepFlavour")
    getattr(process,f'akCs{R}PFJetAnalyzer').pfParticleTransformerAK4JetTags = cms.untracked.string(f"pfParticleTransformerAK4JetTagsAKCs{R}DeepFlavour")
    getattr(process,f'akCs{R}PFJetAnalyzer').pfUnifiedParticleTransformerAK4JetTags = cms.untracked.string(f"pfUnifiedParticleTransformerAK4JetTagsAKCs{R}DeepFlavour")
    process.forest += getattr(process,f'akCs{R}PFJetAnalyzer')


#########################
# Event Selection -> add the needed filters here
#########################

process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.pAna = cms.EndPath(process.skimanalysis)

process.goodMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("pt >= 15.0 && passed('CutBasedIdLoose')")
)
process.goodElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string("pt >= 15.0")
)
process.oneLepton = cms.EDFilter("PATLeptonCountFilter",
    electronSource = cms.InputTag("goodElectrons"),
    muonSource     = cms.InputTag("goodMuons"),
    tauSource      = cms.InputTag(""),
    countElectrons = cms.bool(True),
    countMuons     = cms.bool(True),
    countTaus      = cms.bool(False),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1000000),
)
process.leptonSelection = cms.Sequence(process.goodElectrons * process.goodMuons * process.oneLepton)
process.filterSequence = cms.Sequence(
    process.clusterCompatibilityFilter *
    process.primaryVertexFilter *
    process.leptonSelection
)

process.superFilterPath = cms.Path(process.filterSequence)
process.skimanalysis.superFilters = cms.vstring("superFilterPath")

for path in process.paths:
    if path != "superFilterPath":
        getattr(process, path)._seq = process.filterSequence * getattr(process,path)._seq

