import FWCore.ParameterSet.Config as cms

hltobject = cms.EDAnalyzer("TriggerObjectAnalyzer",
   processName = cms.string("HLT"),
   treeName = cms.string("JetTriggers"),
   triggerResults = cms.InputTag("TriggerResults","","HLT"),
   #triggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT")
   triggerObjects = cms.InputTag("slimmedPatTrigger","")
)

trigger_list_data_2023_skimmed = cms.vstring(
   'HLT_HIEle20Gsf_v',
   'HLT_HIL2SingleMu7_v',
)

trigger_list_data_2024_skimmed = cms.vstring(
    'HLT_HIGEDPhoton10_v',
    'HLT_HIEle20Gsf_v',
    'HLT_HIL2SingleMu7_v',
)

trigger_list_data_2025_skimmed = cms.vstring(
    'HLT_HIGEDPhoton10_v',
    'HLT_HIL2SingleMu7_v',
)

trigger_list_data_2026_skimmed = cms.vstring(
    'HLT_HIGEDPhoton10_v',
    'HLT_HIL2SingleMu7_v',
)
