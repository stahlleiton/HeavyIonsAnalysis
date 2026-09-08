#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "PhysicsTools/XGBoost/interface/XGBooster.h"
#include "fastjet/contrib/SoftKiller.hh"
#include "correction.h"

namespace pat {

  class HIElectronInfoProducer : public edm::global::EDProducer<> {
  public:
    explicit HIElectronInfoProducer(const edm::ParameterSet& iConfig)
        : electronToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("electrons"))),
          pfCandidateToken_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("pfCandidates"))),
          centralityToken_(consumes<int>(iConfig.getParameter<edm::InputTag>("centrality"))),
          etaToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("etaMap"))),
          rhoToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("rhoMap"))),
          patElectronPutToken_(produces<pat::ElectronCollection>()),
          pfMaxEta_(iConfig.getParameter<double>("pf_maxAbsEta")),
          skRadius_(iConfig.getParameter<double>("sk_radius")),
          electronMinPt_(iConfig.getParameter<double>("electron_minPt")),
          rVeto_(iConfig.getParameter<double>("iso_rVeto")),
          rCone_(iConfig.getParameter<double>("iso_rCone")),
          era_(iConfig.getParameter<std::string>("era")),
          isoCorr_(getCorrection(iConfig, "iso_rho_correction")),
          hoeCorr_(getCorrection(iConfig, "hoecorrector")),
          isoModel_(getModel(iConfig, "file_isoModel", 9)),
          idModel_(getModel(iConfig, "file_idModel", 11)) {}
    ~HIElectronInfoProducer() override {};

    void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const override;

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    const edm::EDGetTokenT<pat::ElectronCollection> electronToken_;
    const edm::EDGetTokenT<reco::CandidateView> pfCandidateToken_;
    const edm::EDGetTokenT<int> centralityToken_;
    const edm::EDGetTokenT<std::vector<double>> etaToken_;
    const edm::EDGetTokenT<std::vector<double>> rhoToken_;
    const edm::EDPutTokenT<pat::ElectronCollection> patElectronPutToken_;

    const reco::PFCandidate convert_;
    const double pfMaxEta_, skRadius_, electronMinPt_, rVeto_, rCone_;
    const std::string era_;
    const std::shared_ptr<const correction::Correction> isoCorr_, hoeCorr_;
    const std::unique_ptr<const XGBooster> isoModel_, idModel_;

    std::shared_ptr<const correction::Correction> getCorrection(const edm::ParameterSet& iConfig,
                                                                const std::string& label) {
      const auto& csetIsoRhoCorrections =
          correction::CorrectionSet::from_file(iConfig.getParameter<edm::FileInPath>("file_corr").fullPath());
      return csetIsoRhoCorrections->at(label);
    }

    const XGBooster* getModel(const edm::ParameterSet& iConfig, const std::string& f, const int& nfeat) {
      auto model = new XGBooster(iConfig.getParameter<edm::FileInPath>(f).fullPath());
      for (int i = 0; i < nfeat; i++)
        model->addFeature(std::to_string(i));
      return model;
    }

    enum WP { WP95 = 0, WP90 = 1, WP85 = 4, WP80 = 2, WP70 = 3 };
    bool passMVAIso(const double&, const double&, const bool&, const WP& wp) const;
    bool passMVAId(const double&, const double&, const bool&, const WP& wp) const;
    bool passCutID(const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const bool&,
                   const WP&) const;
  };

}  // namespace pat

bool pat::HIElectronInfoProducer::passMVAIso(const double& mva,
                                             const double& cent,
                                             const bool& isEB,
                                             const WP& wp) const {
  double cut(10.);
  const auto cen = cent > 90. ? 90. : cent;
  const auto cen2 = cen * cen;
  const auto cen3 = cen * cen * cen;
  if (era_ == "Run3_2023_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 6.050705656931276e-07 * cen3 + -8.675509363314822e-05 * cen2 + 0.002218485908134624 * cen + 0.8117784878911797;
      else
        cut = -1.8611301873048183e-07 * cen3 + 1.1749047227407727e-05 * cen2 + -0.0004589054908512365 * cen + 0.9243796918741759;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.0706528567114571e-06 * cen3 + -0.00017034263298702041 * cen2 + 0.004158428420930109 * cen + 0.6678062332568974;
      else
        cut = -3.748291770902249e-07 * cen3 + 1.2264518183783658e-05 * cen2 + -0.0004954559134085261 * cen + 0.8648468182914509;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.2228391411360716e-06 * cen3 + -0.0001816689395238405 * cen2 + 0.0035566414371282634 * cen + 0.5514679545748985;
      else
        cut = -2.400909102332375e-07 * cen3 + -1.0779177540489446e-05 * cen2 + -0.0003609382150404037 * cen + 0.8110586630738115;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 1.1480925637812821e-06 * cen3 + -0.00016356985855249789 * cen2 + 0.0025657545636278297 * cen + 0.45146896982940105;
      else
        cut = -1.853993303378438e-08 * cen3 + -4.057544543903083e-05 * cen2 + 0.00020099222899365378 * cen + 0.7459822419135606;
    }
  } else if (era_ == "Run3_2024_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 7.109642951957174e-07 * cen3 + -8.872806476059474e-05 * cen2 + 0.002028107140882347 * cen + 0.8084472802958512;
      else
        cut = 2.2444480569042535e-07 * cen3 + -4.0312657816409935e-05 * cen2 + 0.0017399548982262318 * cen + 0.8944826095832374;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.0832974048376298e-06 * cen3 + -0.00015826155906626017 * cen2 + 0.0036083128567260254 * cen + 0.6603427035366111;
      else
        cut = 6.17753744613321e-08 * cen3 + -3.439725427500278e-05 * cen2 + 0.00151151895502841 * cen + 0.8303951838511106;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.063943232309302e-06 * cen3 + -0.00015177221779582225 * cen2 + 0.0024999629652588274 * cen + 0.5413676552774369;
      else
        cut = 1.2154591258860994e-07 * cen3 + -4.946728408749522e-05 * cen2 + 0.001717484272457839 * cen + 0.7663510371295376;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 9.467054319493435e-07 * cen3 + -0.000131267271452506 * cen2 + 0.0015101122911347423 * cen + 0.43685398485950283;
      else
        cut = 2.023863319133946e-07 * cen3 + -6.249490111207119e-05 * cen2 + 0.0018441998123990904 * cen + 0.6976312815797168;
    }
  } else if (era_ == "Run3_2025_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 7.179921220736989e-07 * cen3 + -7.843345530395499e-05 * cen2 + 0.0009126057644808109 * cen + 0.8678486378635938;
      else
        cut = 1.4436987260743327e-07 * cen3 + -1.9054215212222034e-05 * cen2 + -1.015591068994216e-05 * cen + 0.9359795950378803;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.0317426510189342e-06 * cen3 + -0.00013244055759707143 * cen2 + 0.0012883461960808379 * cen + 0.75565677374824;
      else
        cut = -1.8606909640214972e-07 * cen3 + 1.13343317554634e-05 * cen2 + -0.0018559084279929782 * cen + 0.9036739700841566;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.1161423274750503e-06 * cen3 + -0.00013685079700608832 * cen2 + -8.446582327315508e-05 * cen + 0.6566647762141241;
      else
        cut = -1.715442874273336e-07 * cen3 + 3.846606650552784e-06 * cen2 + -0.0025705803189852833 * cen + 0.8624304876126456;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 8.915341315484811e-07 * cen3 + -9.71015469449925e-05 * cen2 + -0.0022206189632738996 * cen + 0.5660440989273994;
      else
        cut = -1.0979502232509636e-08 * cen3 + -1.4973111858546348e-05 * cen2 + -0.002964382482739594 * cen + 0.8172068908467145;
    }
  } else
    throw std::logic_error("[ERROR] Wrong era for HIElectronInfoProducer");
  return mva < cut;
}

bool pat::HIElectronInfoProducer::passMVAId(const double& mva, const double& cen, const bool& isEB, const WP& wp) const {
  double cut(10.);
  const auto cen2 = cen * cen;
  const auto cen3 = cen * cen * cen;
  if (era_ == "Run3_2023_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.5240230468578694e-06 * cen3 + 0.0002423784162638523 * cen2 + -0.01331529410784093 * cen + 0.5418680077670319;
      else
        cut = -1.294249655224781e-06 * cen3 + 0.00021547562037982227 * cen2 + -0.01427649182374063 * cen + 0.8854035185153296;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -6.396975957346326e-07 * cen3 + 0.00010828855098015914 * cen2 + -0.006423750716195923 * cen + 0.2405424125484589;
      else
        cut = -1.7981901242892499e-06 * cen3 + 0.00029886869533678824 * cen2 + -0.017975261462461374 * cen + 0.7166095818301947;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -3.439056749932262e-07 * cen3 + 5.7946444409353315e-05 * cen2 + -0.003334025188592283 * cen + 0.11900357131088288;
      else
        cut = -1.184263124123819e-06 * cen3 + 0.0002046266340841097 * cen2 + -0.013146379531433829 * cen + 0.5180183882619553;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -1.6118542418468373e-07 * cen3 + 2.7232687402092295e-05 * cen2 + -0.001589681449002205 * cen + 0.06374074252135704;
      else
        cut = -7.77683827363002e-07 * cen3 + 0.00013986182808899114 * cen2 + -0.009559453036180034 * cen + 0.3795103614554748;
    }
  } else if (era_ == "Run3_2024_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.2970956820231533e-06 * cen3 + 0.00021201754249589331 * cen2 + -0.012397919536427148 * cen + 0.5426324088474989;
      else
        cut = -1.2757640348667187e-06 * cen3 + 0.00020678457465295516 * cen2 + -0.013300802612760298 * cen + 0.833232587490345;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -5.350792129539487e-07 * cen3 + 9.439527400459571e-05 * cen2 + -0.0060705860524204 * cen + 0.2425709435740952;
      else
        cut = -1.4408134003617199e-06 * cen3 + 0.0002404548628670886 * cen2 + -0.015025878791121038 * cen + 0.6458629577292293;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -2.839047394143468e-07 * cen3 + 5.080521341738257e-05 * cen2 + -0.0032480658785239104 * cen + 0.12244430934832529;
      else
        cut = -1.0077249048545508e-06 * cen3 + 0.0001767124348500872 * cen2 + -0.011750994486350573 * cen + 0.4746829057041775;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -1.462400410724609e-07 * cen3 + 2.6139369507962292e-05 * cen2 + -0.0016751593753953462 * cen + 0.06586320086110181;
      else
        cut = -7.24468729787579e-07 * cen3 + 0.0001317304649291509 * cen2 + -0.008970938384534681 * cen + 0.3458153561788365;
    }
  } else if (era_ == "Run3_2025_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.6024110361376762e-06 * cen3 + 0.000269154634846061 * cen2 + -0.015761743337362643 * cen + 0.5908818423705654;
      else
        cut = -7.195116194878053e-07 * cen3 + 0.0001448114214173892 * cen2 + -0.013480805317168734 * cen + 0.8485771334040719;
    }
	//Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -9.101204627530069e-07 * cen3 + 0.00015476001078157628 * cen2 + -0.00895337878308831 * cen + 0.2740293852367914;
      else
        cut = -1.43745963894517e-06 * cen3 + 0.00027474254919810325 * cen2 + -0.019490172700214574 * cen + 0.7056378012471021;
    }
	//Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -4.6822408339744547e-07 * cen3 + 8.096598944242232e-05 * cen2 + -0.004719869208044504 * cen + 0.1368715387267872;
      else
        cut = -1.6050923770591732e-06 * cen3 + 0.0002966068739554079 * cen2 + -0.01912831799575274 * cen + 0.5600477628073475;
    }
	//Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -2.581971015015844e-07 * cen3 + 4.449535582601623e-05 * cen2 + -0.002559121998722972 * cen + 0.07300559934765406;
      else
        cut = -1.4462748757177203e-06 * cen3 + 0.0002618422472592237 * cen2 + -0.01614492200964151 * cen + 0.4285804469411798;
    }
  } else
    throw std::logic_error("[ERROR] Wrong era for HIElectronInfoProducer");
  return mva < cut;
}

bool pat::HIElectronInfoProducer::passCutID(const double& sInIn,
                                            const double& adEta,
                                            const double& adPhi,
                                            const double& hOverE,
                                            const double& eOverP,
                                            const double& aD0,
                                            const double& aDz,
                                            const double& missH,
                                            const double& cen,
                                            const bool& isEB,
                                            const WP& wp) const {
  std::array<double, 4> max_sInIn{{0.}}, max_adEta{{0.}}, max_adPhi{{0.}}, max_hOverE{{0.}}, max_eOverP{{0.}},
      max_aD0{{0.}}, max_aDz{{0.}}, max_missH{{0}};
  if (isEB) {
    if (cen < 30.) {
      //            WP95     WP90     WP80     WP70
      max_sInIn = {{0.0131, 0.0125, 0.0106, 0.0106}};
      max_adEta = {{0.00389, 0.00365, 0.00343, 0.00342}};
      max_adPhi = {{0.0963, 0.0314, 0.0238, 0.0195}};
      max_hOverE = {{0.156, 0.155, 0.153, 0.124}};
      max_eOverP = {{0.421, 0.0547, 0.0285, 0.00837}};
      max_missH = {{2, 1, 1, 1}};
      max_aD0 = {{0.05, 0.05, 0.05, 0.05}};
      max_aDz = {{0.10, 0.10, 0.10, 0.10}};
    } else {
      max_sInIn = {{0.0105, 0.0103, 0.0101, 0.0101}};
      max_adEta = {{0.00457, 0.00377, 0.00322, 0.00305}};
      max_adPhi = {{0.0634, 0.0554, 0.0262, 0.0185}};
      max_hOverE = {{0.107, 0.0762, 0.0555, 0.0401}};
      max_eOverP = {{0.137, 0.0513, 0.0477, 0.0327}};
      max_missH = {{2, 1, 1, 1}};
      max_aD0 = {{0.05, 0.05, 0.05, 0.05}};
      max_aDz = {{0.10, 0.10, 0.10, 0.10}};
    }
  } else {
    if (cen < 30.) {
      max_sInIn = {{0.0382, 0.0329, 0.029, 0.0283}};
      max_adEta = {{0.00881, 0.00682, 0.00576, 0.00489}};
      max_adPhi = {{0.264, 0.19, 0.071, 0.024}};
      max_hOverE = {{0.178, 0.174, 0.172, 0.156}};
      max_eOverP = {{0.146, 0.133, 0.0585, 0.0174}};
      max_missH = {{3, 1, 1, 1}};
      max_aD0 = {{0.10, 0.10, 0.10, 0.10}};
      max_aDz = {{0.20, 0.20, 0.20, 0.20}};
    } else {
      max_sInIn = {{0.028, 0.0277, 0.0271, 0.0271}};
      max_adEta = {{0.0074, 0.00731, 0.00629, 0.0059}};
      max_adPhi = {{0.253, 0.0794, 0.0300, 0.0242}};
      max_hOverE = {{0.107, 0.075, 0.0639, 0.0338}};
      max_eOverP = {{0.142, 0.0462, 0.0144, 0.0122}};
      max_missH = {{3, 1, 1, 1}};
      max_aD0 = {{0.10, 0.10, 0.10, 0.10}};
      max_aDz = {{0.20, 0.20, 0.20, 0.20}};
    }
  }
  return (sInIn < max_sInIn[wp]) && (adEta < max_adEta[wp]) && (adPhi < max_adPhi[wp]) && (hOverE < max_hOverE[wp]) &&
         (eOverP < max_eOverP[wp]) && (missH <= max_missH[wp]) && (aD0 < max_aD0[wp]) && (aDz < max_aDz[wp]);
}

void pat::HIElectronInfoProducer::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  // extract input information
  const auto& electrons = iEvent.get(electronToken_);
  const auto& pfCandidates = iEvent.get(pfCandidateToken_);
  const auto& etaMap = iEvent.get(etaToken_);
  const auto& rhoMap = iEvent.get(rhoToken_);
  const double cent = iEvent.get(centralityToken_) / 2.0;

  // select PF candidates
  std::vector<std::tuple<double, double, double, int, int, double>> selPFCands;
  if (etaMap.size() > 1) {
    selPFCands.reserve(pfCandidates.size());
    std::vector<std::vector<fastjet::PseudoJet>> particlesForSK(etaMap.size() - 1);
    for (const auto& pf : pfCandidates) {
      // determine eta category
      int ieta(-1);
      for (size_t i = 1; i < etaMap.size(); i++)
        if (pf.eta() >= etaMap[i - 1] && pf.eta() < etaMap[i]) {
          ieta = i - 1;
          break;
        }
      if (ieta < 0)
        continue;
      // fill particles for soft killer
      particlesForSK[ieta].emplace_back(pf.px(), pf.py(), pf.pz(), pf.energy());
      // fill selected PF candidates
      const auto& id = convert_.translatePdgIdToType(pf.pdgId());
      if (id > 0 && id <= 5 && std::abs(pf.eta()) <= pfMaxEta_)
        selPFCands.emplace_back(pf.pt(), pf.eta(), pf.phi(), id, ieta, 0.0);
    }

    // compute soft killer thresholds
    std::vector<double> skThrs(etaMap.size() - 1);
    for (size_t i = 0; i < particlesForSK.size(); i++) {
      const auto& particles = particlesForSK[i];
      if (not particles.empty()) {
        fastjet::contrib::SoftKiller soft_killer(etaMap[i], etaMap[i + 1], skRadius_, skRadius_);
        std::vector<fastjet::PseudoJet> soft_killed_event;
        soft_killer.apply(particles, soft_killed_event, skThrs[i]);
      }
    }

    // add soft killer thresholds to selected PF candidates
    for (auto& cand : selPFCands)
      std::get<5>(cand) = skThrs[std::get<4>(cand)];
  }

  // initialize output electron collection
  pat::ElectronCollection output(electrons);

  // loop over output electrons
  for (auto& electron : output) {
    if (electron.pt() < electronMinPt_)
      continue;

    // associate rho value
    double rho(-1.);
    for (size_t i = 1; i < etaMap.size(); i++)
      if (electron.eta() >= etaMap[i - 1] && electron.eta() < etaMap[i]) {
        rho = rhoMap[i - 1];
        break;
      }
    if (rho < 0)
      continue;

    const auto absEta = std::abs(electron.eta());
    const bool isEB(absEta < 1.45);

    // compute the identification from MVA
    const auto& sigmaIetaIeta = electron.sigmaIetaIeta();
    const auto& dEtaSeedAtVtx = electron.deltaEtaSeedClusterTrackAtVtx();
    const auto& dPhiAtVtx = electron.deltaPhiSuperClusterTrackAtVtx();
    const auto& track = electron.gsfTrack();
    const auto& d0 = electron.dB(pat::Electron::PV2D);
    const auto& dz = electron.dB(pat::Electron::PVDZ);
    const double& missHits = electron.gsfTrack()->numberOfLostHits();
    const auto& ecalEnergy =
        electron.hasUserFloat("rawEcalEnergy") ? electron.userFloat("rawEcalEnergy") : electron.ecalEnergy();
    const auto& eOverPInv = 1. / ecalEnergy - 1. / electron.trackMomentumAtVtx().R();
    const auto& corHoverEBc = electron.hcalOverEcalBc() - hoeCorr_->evaluate({{rho}});
    const std::vector<double> inputsID(
        {absEta, electron.phi(), rho, sigmaIetaIeta, dEtaSeedAtVtx, dPhiAtVtx, d0, dz, missHits, eOverPInv, corHoverEBc});
    const std::vector<float> featuresID(inputsID.begin(), inputsID.end());
    const auto idValue = 1. - idModel_->predict(featuresID);
    electron.addUserFloat("hiMVAId", idValue);
    electron.addUserInt("hiMVAIdWP95", passMVAId(idValue, cent, isEB, WP95));
    electron.addUserInt("hiMVAIdWP90", passMVAId(idValue, cent, isEB, WP90));
    electron.addUserInt("hiMVAIdWP85", passMVAId(idValue, cent, isEB, WP85));
    electron.addUserInt("hiMVAIdWP80", passMVAId(idValue, cent, isEB, WP80));

    // compute IP3D significance
    const auto ip3DSig = std::abs(electron.dB(pat::Electron::PV3D)) / electron.edB(pat::Electron::PV3D);

    // compute PF and soft killer isolations
    double pfChIso(0.), pfNeuIso(0.), pfPhoIso(0.);
    double skPFChIso(0.), skPFNeuIso(0.), skPFPhoIso(0.);
    for (const auto& cand : selPFCands) {
      const auto& [pt, eta, phi, id, ieta, skThr] = cand;
      const auto dR2 = reco::deltaR2(electron.eta(), electron.phi(), eta, phi);
      if (dR2 >= rVeto_ * rVeto_ && dR2 <= rCone_ * rCone_) {
        (id == 5 ? pfNeuIso : (id == 4 ? pfPhoIso : pfChIso)) += pt;
        (id == 5 ? skPFNeuIso : (id == 4 ? skPFPhoIso : skPFChIso)) += pt * (pt > skThr);
      }
    }
    const auto& pfIso = pfChIso + pfNeuIso + pfPhoIso;
    const auto& skPFIso = skPFChIso + skPFNeuIso + skPFPhoIso;

    // correct the PF isolation variables
    const auto& pfRelIso = (pfIso - isoCorr_->evaluate({{"PFIso", "ele", rho}})) / electron.pt();
    const auto& pfChRelIso = (pfChIso - isoCorr_->evaluate({{"PFChIso", "ele", rho}})) / electron.pt();
    const auto& skPFRelIso = (skPFIso - isoCorr_->evaluate({{"skPFIso", "ele", rho}})) / electron.pt();
    const auto& skPFChRelIso = (skPFChIso - isoCorr_->evaluate({{"skPFChIso", "ele", rho}})) / electron.pt();

    // compute the isolation from MVA
    const std::vector<double> inputsISO(
        {absEta, electron.phi(), rho, ip3DSig, pfRelIso, pfChRelIso, skPFRelIso, skPFChRelIso, idValue});
    const std::vector<float> featuresISO(inputsISO.begin(), inputsISO.end());
    const auto isoValue = 1. - isoModel_->predict(featuresISO);
    electron.addUserFloat("hiMVAIso", isoValue);
    electron.addUserInt("hiMVAIsoWP95", passMVAIso(isoValue, cent, isEB, WP95));
    electron.addUserInt("hiMVAIsoWP90", passMVAIso(isoValue, cent, isEB, WP90));
    electron.addUserInt("hiMVAIsoWP85", passMVAIso(isoValue, cent, isEB, WP85));
    electron.addUserInt("hiMVAIsoWP80", passMVAIso(isoValue, cent, isEB, WP80));

    // compute the cut-based identification
    const auto& sInIn = electron.full5x5_sigmaIetaIeta();
    const auto& dEtaSeed = (electron.superCluster().isNonnull() && electron.superCluster()->seed().isNonnull())
                               ? (electron.deltaEtaSuperClusterTrackAtVtx() - electron.superCluster()->eta() +
                                  electron.superCluster()->seed()->eta())
                               : std::numeric_limits<float>::max();
    const auto adEta = std::abs(dEtaSeed);
    const auto adPhi = std::abs(dPhiAtVtx);
    const auto& hOverE = electron.full5x5_hcalOverEcalBc();
    const auto& ooEmooP = (1.0 - electron.eSuperClusterOverP()) / electron.ecalEnergy();
    const auto eOverP = (electron.ecalEnergy() > 0 && std::isfinite(electron.ecalEnergy())) ? std::abs(ooEmooP) : 1.e30;
    const auto aD0 = std::abs(d0);
    const auto aDz = std::abs(dz);
    electron.addUserInt("hiCutIdWP95",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP95));
    electron.addUserInt("hiCutIdWP90",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP90));
    electron.addUserInt("hiCutIdWP80",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP80));
    electron.addUserInt("hiCutIdWP70",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP70));
  }

  iEvent.emplace(patElectronPutToken_, std::move(output));
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::HIElectronInfoProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("electrons", edm::InputTag("slimmedElectrons"))->setComment("electron input collection");
  desc.add<edm::InputTag>("pfCandidates", edm::InputTag("packedPFCandidates"))
      ->setComment("PF candidate input collection");
  desc.add<edm::InputTag>("centrality", edm::InputTag("centralityBin:HFtowers"))->setComment("centrality");
  desc.add<edm::InputTag>("etaMap", edm::InputTag("hiFJRhoProducerFinerBins:mapEtaEdges"))
      ->setComment("eta ranges for rho and soft killer");
  desc.add<edm::InputTag>("rhoMap", edm::InputTag("hiFJRhoProducerFinerBins:mapToRho"))->setComment("rho");
  desc.add<double>("pf_maxAbsEta", 2.8)->setComment("Maximum absolute eta for PF candidates");
  desc.add<double>("sk_radius", 0.4)->setComment("Radius for soft killer threshold");
  desc.add<double>("electron_minPt", 0.0)->setComment("Electron minimum pt");
  desc.add<double>("iso_rVeto", 0.026)->setComment("Isolation veto radius");
  desc.add<double>("iso_rCone", 0.3)->setComment("Isolation cone radius");
  desc.add<std::string>("era", "")->setComment("Era");
  desc.add<edm::FileInPath>("file_idModel", {})->setComment("Path to identification model");
  desc.add<edm::FileInPath>("file_isoModel", {})->setComment("Path to isolation model");
  desc.add<edm::FileInPath>("file_corr", {})->setComment("Path to rho correction");
  descriptions.add("hiElectrons", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(HIElectronInfoProducer);
