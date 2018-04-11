# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.Run2Quantities as r2q
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.Run2CPQuantities as r2cpq
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.SingleTauQuantities as stq


import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsElectronID as sEID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMuonID as sMID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauID as sTID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID 
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsSvfit as sSvfit
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter as sMPlF
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsMVATestMethods as sMVATM

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA

class mt_ArtusConfig(dict):

	def __init__(self):
		self.base_copy = copy.deepcopy(self)
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 

	def build_config(self, nickname):                #Maybe change this the arguments to process/year and DATA/MC
		"""
		"include" : [
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsVetoMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJEC.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJECUncertaintySplit.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJetID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsBTaggedJetID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsSvfit.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMinimalPlotlevelFilter_mt.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsMVATestMethods.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauES.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsTauPolarisationMva.json"
		],
		"""

		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		self.update(ElectronID_config)	

		MuonID_config = sMID.Muon_ID(nickname)
		MuonID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used
		MuonID_config.vetoMuon_ID(nickname)
		self.update(MuonID_config)	

		TauID_config = sTID.Tau_ID(nickname)			#here loose is not appended since loose tau ID is not used
		self.update(TauID_config)

		JEC_config = sJEC.JEC(nickname)  #Is allready in baseconfig, for now leave it in; possibly remove it 
		self.update(JEC_config)

		JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		self.update(JECUncertaintySplit_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)

		MinimalPlotlevelFilter_config = sMPlF.MinimalPlotlevelFilter()
		MinimalPlotlevelFilter_config.mt()
		self.update(MinimalPlotlevelFilter_config)
		
		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		TauES_config = sTES.TauES(nickname)
		self.update(TauES_config)
		
		TauPolarisationMva_config = sTPMVA.TauPolarisationMva()
		self.update(TauPolarisationMva_config)

		self["TauPolarisationTmvaWeights"] = [
			"/afs/cern.ch/user/m/mfackeld/public/weights_tmva/training.weights.xml",
			"/afs/cern.ch/user/m/mfackeld/public/weights_sklearn/training_mt.weights.xml"
		]
		self["Channel"] = "MT"
		self["MinNMuons"] = 1
		self["MinNTaus"] = 1
		self["HltPaths_comment"] = "The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer."

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] = ["HLT_IsoMu18"]
			self["NoHltFiltering"] = False
			self["DiTauPairNoHLT"] = False

		elif re.search("Run2016|Spring16|Summer16", nickname):
			self["HltPaths"] = [
					"HLT_IsoMu22",
					"HLT_IsoTkMu22",
					"HLT_IsoMu22_eta2p1",
					"HLT_IsoTkMu22_eta2p1",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"
				]
			self["NoHltFiltering"] = False
			self["DiTauPairNoHLT"] = False
				
		elif re.search("Embedding(2016|MC)", nickname):
			self["HltPaths"] = [""]
			self["NoHltFiltering"] = True
			self["DiTauPairNoHLT"] = True 
			
		self["TauID"] = "TauIDRecommendation13TeV"
		self["TauUseOldDMs"] = True

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["MuonLowerPtCuts"] = ["19.0"]

		else:
			self["MuonLowerPtCuts"] = ["20.0"]
		
		
		self["MuonUpperAbsEtaCuts"] = ["2.1"]
		self["TauLowerPtCuts"] = ["20.0"]
		self["TauUpperAbsEtaCuts"] = ["2.3"]
		self["TriggerObjectLowerPtCut"] = -1.0
		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["DiTauPairLepton1LowerPtCuts"] = [
					"HLT_IsoMu18_v:19.0"
				]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
					"HLT_IsoMu18_v"
				]
		elif re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["DiTauPairLepton1LowerPtCuts"] = [
					"HLT_IsoMu24_v:25.0",
					"HLT_IsoTkMu24_v:25.0"
				]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
					"HLT_IsoMu22_v",
					"HLT_IsoTkMu22_v",
					"HLT_IsoMu22_eta2p1_v",
					"HLT_IsoTkMu22_eta2p1_v",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"
				]
			
		else:                                         #I believe "Run2016|Spring16|Summer16|Embedding(2016|MC)" is everything else but for safety i did it here, 2017 not included yet
			self["DiTauPairLepton1LowerPtCuts"] = [
					"HLT_IsoMu24_v:25.0",
					"HLT_IsoTkMu24_v:25.0"
				]
		
		if re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["DiTauPairHLTLast"] = True
			self["HLTBranchNames"] = [
					"trg_singlemuon:HLT_IsoMu22_v",
					"trg_singlemuon:HLT_IsoTkMu22_v",
					"trg_singlemuon:HLT_IsoMu22_eta2p1_v",
					"trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
					"trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
					"trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"
				]

			self["MuonTriggerFilterNames"] = [
					"HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
					"HLT_IsoTkMu22_v:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
					"HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
					"HLT_IsoTkMu22_eta2p1_v:hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
				]

			self["TauTriggerFilterNames"] = [
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltPFTau20TrackLooseIsoAgainstMuon",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltPFTau20TrackLooseIsoAgainstMuon",
					"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
				]
	
		elif re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["MuonTriggerFilterNames"] = [
					"HLT_IsoMu18_v:hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09"
				]
		else:
			self["DiTauPairHLTLast"] = False
		
		self["EventWeight"] = "eventWeight"
		self["SaveRooWorkspaceTriggerWeightAsOptionalOnly"] = "true"
		self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		self["RooWorkspaceWeightNames"] = [
			"0:triggerWeight_singleMu",
			"0:idIsoWeight"
		]
		self["RooWorkspaceObjectNames"] = [
			"0:m_trgMu22OR_eta2p1_desy_ratio",
			"0:m_idiso0p15_desy_ratio"
		]
		self["RooWorkspaceObjectArguments"] = [
			"0:m_pt,m_eta",
			"0:m_pt,m_eta"
		]
		self["SaveMuTauTriggerWeightAsOptionalOnly"] = "true"
		self["MuTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		self["MuTauTriggerWeightWorkspaceWeightNames"] = [
			"0:triggerWeight_muTauCross",
			"1:triggerWeight_muTauCross"
		]
		self["MuTauTriggerWeightWorkspaceObjectNames"] = [
			"0:m_trgMu19leg_eta2p1_desy_ratio",
			"1:t_genuine_TightIso_mt_ratio,t_fake_TightIso_mt_ratio"
		]
		self["MuTauTriggerWeightWorkspaceObjectArguments"] = [
			"0:m_pt,m_eta",
			"1:t_pt,t_eta"
		]
	
		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_IsoMu18_fall15.root"]
			self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_IsoMu18_fall15.root"]

			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p1_fall15.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p1_fall15.root"]		

		else:
			self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu22OR_eta2p1_eff.root"]
			self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu22OR_eta2p1_eff.root"]

			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]


		self["TriggerEfficiencyMode"] = "multiply_weights"
		self["IdentificationEfficiencyMode"] = "multiply_weights"
		self["EleTauFakeRateWeightFile"] = [
			"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"
		]
		self["TauTauRestFrameReco"] =  "collinear_approximation"
		self["InvalidateNonMatchingElectrons"] =  False
		self["InvalidateNonMatchingMuons"] =  True
		self["InvalidateNonMatchingTaus"] =  True
		self["InvalidateNonMatchingJets"] =  False
		self["UseUWGenMatching"] =  "true"
		self["DirectIso"] =  True
		self["OSChargeLeptons"] = True
		self["AddGenMatchedParticles"] = True
		self["AddGenMatchedTaus"] = True
		self["AddGenMatchedTauJets"] = True
		self["BranchGenMatchedMuons"] = True
		self["BranchGenMatchedTaus"] = True
		self["Consumers"] = [
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer",
			"#CutFlowTreeConsumer",
			"#KappaMuonsConsumer",
			"#KappaTausConsumer",
			"#KappaTaggedJetsConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer",
			"#PrintGenParticleDecayTreeConsumer"
		]

		self["Quantities"]=[]
		if re.search("Run2015", nickname):  					#the same as tt
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities() 	#until here
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
		
		elif re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):	 #the same as tt
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantitiesSvfit()
			self["Quantities"] += stq.SingleTauQuantities()	#until here
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
			self["Quantities"] += ["tauSpinnerPolarisation",
					"trg_singlemuon",
					"trg_mutaucross",
					"triggerWeight_singleMu_1",
					"triggerWeight_muTauCross_1",
					"triggerWeight_muTauCross_2"]


		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16))", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
			
			self["Quantities"] += ["trg_singlemuon",
					"trg_mutaucross",
					"triggerWeight_singleMu_1",
					"triggerWeight_muTauCross_1",
					"triggerWeight_muTauCross_2"]    #commented out: "#tauPolarisationTMVA", "#tauPolarisationSKLEARN",

		elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
			
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.genQuantities()			
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):   #almost the same as 2016 signal, no splitJecUncertaintyQuantities()
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list

		elif re.search("Embedding2016", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list

			self["Quantities"] += ["triggerWeight_singleMu_1",
					"triggerWeight_muTauCross_1",
					"triggerWeight_muTauCross_2"]
		
		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()	
			self["Quantities"] += stq.SingleTauQuantities()	#until here		
			self["Quantities"] += r2cpq.recoCPQuantities()
			
			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list

			self["Quantities"] += ["triggerWeight_singleMu_1",
					"triggerWeight_muTauCross_1",
					"triggerWeight_muTauCross_2",
					"jetCorrectionWeight"]
		else:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantitiesSvfit()

			self["Quantities"] += ["nVetoMuons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
			
			self["Quantities"] += ["trg_singlemuon",
					"trg_mutaucross",
					"triggerWeight_singleMu_1",
					"triggerWeight_muTauCross_1",
					"triggerWeight_muTauCross_2"]

		self["Quantities"]=list(set(self["Quantities"])) #removes dublicates from list by making it a set and then again a list, dont know if it should be a list or can be left as a set

		self["Processors"]=[]
		if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:ZPtReweightProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:SimpleFitProducer"]
			self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuTauTriggerWeightProducer"]
			self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]
		elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["#producer:MELAProducer"]
			self["Processors"] += ["#producer:SimpleFitProducer"]
			self["Processors"] += ["producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["#producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:ZPtReweightProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["#producer:MELAProducer"]
			self["Processors"] += ["#producer:SimpleFitProducer"]
			self["Processors"] += ["producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["producer:EleTauFakeRateWeightProducer"]
			self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["#producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]
		elif re.search("Run2016", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:SimpleFitProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]
		elif re.search("Run2015", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["#producer:MELAProducer"]
			self["Processors"] += ["#producer:SimpleFitProducer"]
			self["Processors"] += ["#producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]
		elif re.search("Embedding201", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"#producer:MetCorrector",
					"#producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["#producer:MELAProducer"]
			self["Processors"] += ["#producer:TriggerWeightProducer"]
			self["Processors"] += ["#producer:IdentificationWeightProducer"]
			self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["#producer:SimpleFitProducer"]
			self["Processors"] += ["#producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuTauTriggerWeightProducer"]
			self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["#producer:MadGraphReweightingProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["#producer:SimpleFitProducer"]
			self["Processors"] += ["producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["producer:EleTauFakeRateWeightProducer"]
			self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["#producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:MadGraphReweightingProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]
		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:ZPtReweightProducer",
					"#filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuTauTriggerWeightProducer"]
			self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:EventWeightProducer"]
		else:
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidElectronsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidMTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoMuonsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoMuonVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter"] #I believe from here it is not that strict anymore with the ordering
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:SimpleFitProducer"]
			self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuTauTriggerWeightProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["#producer:TauPolarisationTmvaReader"]
			self["Processors"] += ["producer:LFVJetCorrection2016Producer"]
			self["Processors"] += ["producer:EventWeightProducer"]



