import FWCore.ParameterSet.Config as cms

hltanalysis = cms.EDAnalyzer(
    'TriggerAnalyzer',
    HLTProcessName = cms.string('HLT'),
    hltresults = cms.InputTag('TriggerResults::HLT'),
    l1results = cms.InputTag('gtStage2Digis'),
    hltdummybranches = cms.vstring([]),
    l1dummybranches = cms.vstring([]),
    hltPSProvCfg=cms.PSet(stageL1Trigger = cms.uint32(2)),
    )
