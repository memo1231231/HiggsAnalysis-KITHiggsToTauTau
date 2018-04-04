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

class em_ArtusConfig(dict):

	def __init__(self):
		self.base_copy = copy.deepcopy(self)
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 

	def build_config(self, nickname): 
               #Maybe change this the arguments to process/year and DATA/MC

		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		self.update(ElectronID_config)	

		MuonID_config = sMID.Muon_ID(nickname)
		MuonID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used
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
		MinimalPlotlevelFilter_config.em()
		self.update(MinimalPlotlevelFilter_config)
		
		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		



		self["Channel"] = "EM"
		self["MinNElectrons"] = 1
		self["MinNMuons"] = 1
		self["HltPaths_comment"] = "The first path must be one with the higher pt cut on the electron. The second and last path must be one with the higher pt cut on the muon. Corresponding Pt cuts are implemented in the Run2DecayChannelProducer."

		self["NoHltFiltering"] = False #*default
		self["DiTauPairLepton1LowerPtCuts"] = [								     # **default
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:24.0"
				]

		self["DiTauPairLepton2LowerPtCuts"] = [								# ***default
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:24.0",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:24.0"
				]
		self["DiTauPairNoHLT"] = False
		
		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] = [
					"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL",
					"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"
				]
			self["DiTauPairLepton1LowerPtCuts"] = [							#**
					"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:18.0"
				]
			self["DiTauPairLepton2LowerPtCuts"] = [
					"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v:18.0"
				]



		elif re.search("Run2016(B|C|D|E|F)|Spring16|Summer16", nickname):
			self["HltPaths"] = [
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"
				]

		elif re.search("Run2016(G|H)", nickname):
			self["HltPaths"] = [
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
				]
			self["DiTauPairLepton1LowerPtCuts"] = [							#**
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:24.0"
				]

		elif re.search("Embedding(2016|MC)", nickname):
			self["HltPaths"] = []
			self["NoHltFiltering"] = True 								#*if "Embedding(2016|MC)"
			self["DiTauPairLepton1LowerPtCuts"] = [                                         	 #**
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:-1.0",
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"
				]
			self["DiTauPairLepton2LowerPtCuts"] = [							#***
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:-1.0",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"
				]
			self["DiTauPairNoHLT"] = True
			self["LowerCutHardLepPt"] = 24.0
			
		
		self["ElectronLowerPtCuts"] = [
			"13.0"
		]
		self["ElectronUpperAbsEtaCuts"] = [
			"2.5"
		]
		self["MuonLowerPtCuts"] = [
			"10.0"
		]
		self["MuonUpperAbsEtaCuts"] = [
			"2.4"
		]
		self["DeltaRTriggerMatchingElectrons"] = 0.4
		self["DeltaRTriggerMatchingMuons"] = 0.4
		self["DiTauPairMinDeltaRCut"] = 0.3
		self["DiTauPairIsTauIsoMVA"] = True




		
		self["EventWeight"] = "eventWeight"
		self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		self["RooWorkspaceWeightNames"] = [
			"0:idIsoWeight",
			"1:idIsoWeight"
		]
		self["RooWorkspaceObjectNames"] = [
			"0:e_idiso0p15_desy_ratio",
			"1:m_idiso0p20_desy_ratio"
		]
		self["RooWorkspaceObjectArguments"] = [
			"0:e_pt,e_eta",
			"1:m_pt,m_eta"
		]





		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["TriggerEfficiencyData"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele12_fall15.root",         	 #2 times 0:... and 1:...
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele17_fall15.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root"
				]

			self["TriggerEfficiencyMc"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12_fall15.root",
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele17_fall15.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root"
				]

			self["IdentificationEfficiencyData"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
				]
			self["IdentificationEfficiencyMc"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p15_fall15.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root"
				]

		else:
			self["TriggerEfficiencyData"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele12leg_eff.root",      		 #2 times 0:... and 1:...
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele23leg_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu8leg_2016BtoH_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu23leg_2016BtoH_eff.root"
				] 		
			self["TriggerEfficiencyMc"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12leg_eff.root",
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23leg_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8leg_2016BtoH_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu23leg_2016BtoH_eff.root"
				]
		
			self["IdentificationEfficiencyData"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
				]
			self["IdentificationEfficiencyMc"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p15_eff.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
				]

		
		self["TriggerEfficiencyMode"] = "correlate_triggers"
		self["IdentificationEfficiencyMode"] = "multiply_weights"
		self["TauTauRestFrameReco"] = "collinear_approximation"


		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["ElectronTriggerFilterNames"] = [
					"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
					"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter"
				]
			self["MuonTriggerFilterNames"] = [
					"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered17",
					"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8"
				]

		elif re.search("Run2016(B|C|D|E|F)|Spring16|Summer16", nickname):
			self["ElectronTriggerFilterNames"] = [
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter"
				]
			self["MuonTriggerFilterNames"] = [
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8"
				]

		elif re.search("Run2016(G|H)". nickname):
			self["ElectronTriggerFilterNames"] = [
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter"
				]
			self["MuonTriggerFilterNames"] = [
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
					"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8",
					"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter"
				]

		
	
		self["InvalidateNonMatchingElectrons"] = True
		self["InvalidateNonMatchingMuons"] = True
		self["InvalidateNonMatchingTaus"] = False
		self["InvalidateNonMatchingJets"] = False
		self["DirectIso"] = True


		self["AddGenMatchedParticles"] = True
		self["BranchGenMatchedElectrons"] = True
		self["BranchGenMatchedMuons"] = True
		self["Consumers"] = [
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer",
			"#CutFlowTreeConsumer",
			"#KappaElectronsConsumer",
			"#KappaMuonsConsumer",
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
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]

		elif re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2q.lheWeightsDYQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantitiesSvfit()
			self["Quantities"] += stq.SingleTauQuantities()
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates",
					"tauSpinnerPolarisation"]

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
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]
		elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):	
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.genQuantities()			
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates",
					"tauSpinnerPolarisation"]


		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname): 
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]
		elif re.search("Embedding2016", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates",
					"tauSpinnerPolarisation"]

		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantities()		
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]
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
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]


		self["Quantities"]=list(set(self["Quantities"])) #removes dublicates from list by making it a set and then again a list, dont know if it should be a list or can be left as a set

		if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ElectronCorrectionsProducer",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:ZPtReweightProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]

		elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:RecoElectronGenParticleMatchingProducer",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:RecoMuonGenParticleMatchingProducer",
					"producer:MatchedLeptonsProducer",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
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
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"#producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:RecoElectronGenParticleMatchingProducer",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:RecoMuonGenParticleMatchingProducer",
					"producer:MatchedLeptonsProducer",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
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
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"#producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]
		elif re.search("Run2016", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]
		elif re.search("Run2015", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"#producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]
		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ElectronCorrectionsProducer",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:TriggerWeightProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:MadGraphReweightingProducer",
					"producer:EventWeightProducer"
				]
		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:RecoElectronGenParticleMatchingProducer",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:RecoMuonGenParticleMatchingProducer",
					"producer:MatchedLeptonsProducer",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
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
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:MadGraphReweightingProducer",
					"producer:EventWeightProducer"
				]
		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			 self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ElectronCorrectionsProducer",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:ZPtReweightProducer",
					"#filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"producer:TriggerWeightProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]
		else:
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ElectronCorrectionsProducer",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"filter:ValidMuonsFilter",
					"producer:MuonTriggerMatchingProducer",
					"filter:MinMuonsCountFilter",
					"producer:ValidTausProducer",
					"producer:ValidEMPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:EventWeightProducer"
				]





















