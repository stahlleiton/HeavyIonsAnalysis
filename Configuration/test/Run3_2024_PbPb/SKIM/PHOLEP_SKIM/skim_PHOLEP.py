# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: skim --conditions 141X_dataRun3_Prompt_v1 -s NONE --datatier MINIAOD --eventcontent MINIAOD --data --process SKIM --scenario pp --customise Configuration/DataProcessing/RecoTLR.customisePostEra_Run3_pp_on_PbPb_2024 --filein /store/hidata/HIRun2024A/HIPhysicsRawPrime0/MINIAOD/PbPbEW-PromptReco-v1/000/399/485/00000/6a31df14-1615-43e8-8f3a-351327a47980.root --fileout miniaod.root --era Run3_pp_on_PbPb_2024 --nThreads 8 -n -1
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_pp_on_PbPb_2024_cff import Run3_pp_on_PbPb_2024

process = cms.Process('SKIM',Run3_pp_on_PbPb_2024)

# import of standard configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/hidata/HIRun2024B/HIPhysicsRawPrime0/MINIAOD/PromptReco-v2/000/388/710/00000/2603db0b-9307-4b83-88cc-fef1bbb2633f.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('skim nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAOD'),
        filterName = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('forest')),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(-900),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('miniaod.root'),
    outputCommands = process.MINIAODEventContent.outputCommands,
    overrideBranchesSplitLevel = cms.untracked.VPSet(
        cms.untracked.PSet(
            branch = cms.untracked.string('patPackedCandidates_packedPFCandidates__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('recoGenParticles_prunedGenParticles__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('patTriggerObjectStandAlones_slimmedPatTrigger__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('patPackedGenParticles_packedGenParticles__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('patJets_slimmedJets__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('recoVertexs_offlineSlimmedPrimaryVertices__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('recoVertexs_offlineSlimmedPrimaryVerticesWithBS__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('recoCaloClusters_reducedEgamma_reducedESClusters_*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEBRecHits_*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEERecHits_*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('recoGenJets_slimmedGenJets__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('patJets_slimmedJetsPuppi__*'),
            splitLevel = cms.untracked.int32(99)
        ),
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedESRecHits_*'),
            splitLevel = cms.untracked.int32(99)
        )
    ),
    overrideInputFileSplitLevels = cms.untracked.bool(True),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

###########################################################################
# Add secondary vertex
###########################################################################
process.vertexSeq = cms.Sequence()
process.forest = cms.Path()
cols = []
def _addSecondaryVertex(process,n=''):
    process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
    import RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff as _sv
    if n == 'Negative':
        import RecoVertex.AdaptiveVertexFinder.inclusiveNegativeVertexing_cff as _sv
    for mod in [f'inclusiveCandidate{n}VertexFinder',f'candidate{n}VertexArbitrator']:
        setattr(process,mod,getattr(_sv,mod).clone(
            tracks = "packedPFCandidates",
            primaryVertices = "offlineSlimmedPrimaryVertices"
        ))
    getattr(process,f'inclusiveCandidate{n}VertexFinder').minHits = 10
    getattr(process,f'inclusiveCandidate{n}VertexFinder').minPt = 1.0
    setattr(process,f'candidate{n}VertexMerger',getattr(_sv,f'candidate{n}VertexMerger').clone())
    setattr(process,f'slimmed{n}SecondaryVertices',getattr(_sv,f'inclusiveCandidate{n}SecondaryVertices').clone())
    for mod in [f'inclusiveCandidate{n}VertexFinder',f'candidate{n}VertexMerger',
                f'candidate{n}VertexArbitrator',f'slimmed{n}SecondaryVertices']:
        process.vertexSeq += getattr(process,mod)
    cols.append(f'slimmed{n}SecondaryVertices')
_addSecondaryVertex(process)
_addSecondaryVertex(process,"Negative")
process.forest += process.vertexSeq

###########################################################################
# Define output collections
###########################################################################
for new_collection_to_keep in cols:
    process.MINIAODoutput.outputCommands += [
        f'drop *_{new_collection_to_keep}__*',
        f'keep *_{new_collection_to_keep}__{process.name_()}']

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '141X_dataRun3_Prompt_v4', '')

# Path and EndPath definitions
process.MINIAODoutput_step = cms.EndPath(process.MINIAODoutput)

process.goodMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("slimmedMuons::@skipCurrentProcess"),
    cut = cms.string("pt >= 15.0 && passed('CutBasedIdLoose')")
)
process.goodElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons::@skipCurrentProcess"),
    cut = cms.string("pt >= 15.0")
)
process.goodPhotons = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("slimmedPhotons::@skipCurrentProcess"),
    cut = cms.string("pt >= 25.0")
)
process.oneLepton = cms.EDFilter("PATCountFilter",
    electronSource = cms.InputTag("goodElectrons"),
    muonSource     = cms.InputTag("goodMuons"),
    tauSource      = cms.InputTag(""),
    photonSource   = cms.untracked.InputTag("goodPhotons"),
    countElectrons = cms.bool(True),
    countMuons     = cms.bool(True),
    countTaus      = cms.bool(False),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1000000),
)
process.leptonSelection = cms.Sequence(process.goodElectrons * process.goodMuons * process.goodPhotons * process.oneLepton)
process.filterSequence = cms.Sequence(
    process.leptonSelection
)
process.forest.insert(0,process.filterSequence)

# Schedule definition
process.schedule = cms.Schedule(process.forest,process.MINIAODoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 8
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.RecoTLR
from Configuration.DataProcessing.RecoTLR import customisePostEra_Run3_pp_on_PbPb_2024 

#call to customisation function customisePostEra_Run3_pp_on_PbPb_2024 imported from Configuration.DataProcessing.RecoTLR
process = customisePostEra_Run3_pp_on_PbPb_2024(process)

# End of customisation functions


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
