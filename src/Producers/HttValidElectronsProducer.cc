
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ParticleIsolation.h"


HttValidElectronsProducer::HttValidElectronsProducer(std::vector<KElectron*> product_type::*validElectrons,
                                                     std::vector<KElectron*> product_type::*invalidElectrons,
                                                     std::string (setting_type::*GetElectronID)(void) const,
                                                     std::string (setting_type::*GetElectronIDType)(void) const,
                                                     std::string (setting_type::*GetElectronIDName)(void) const,
                                                     float (setting_type::*GetElectronMvaIDCutEB1)(void) const,
                                                     float (setting_type::*GetElectronMvaIDCutEB2)(void) const,
                                                     float (setting_type::*GetElectronMvaIDCutEE)(void) const,
                                                     std::string (setting_type::*GetElectronIsoType)(void) const,
                                                     std::string (setting_type::*GetElectronIso)(void) const,
                                                     std::string (setting_type::*GetElectronReco)(void) const,
                                                     std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
                                                     std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
                                                     float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const,
                                                     float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const,
                                                     float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const,
                                                     float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const,
                                                     float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const,
                                                     float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const,
                                                     float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronIsoSignalConeSize)(void) const,
                                                     float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const,
                                                     float (setting_type::*GetElectronTrackDxyCut)(void) const,
                                                     float (setting_type::*GetElectronTrackDzCut)(void) const,
                                                     std::vector<std::string>& (setting_type::*GetElectronIDList)(void) const) :
	ValidElectronsProducer(validElectrons, invalidElectrons,
	                       GetElectronID, GetElectronIsoType, GetElectronIso, GetElectronReco,
	                       GetLowerPtCuts, GetUpperAbsEtaCuts),
	GetElectronIDType(GetElectronIDType),
	GetElectronIDName(GetElectronIDName),
	GetElectronMvaIDCutEB1(GetElectronMvaIDCutEB1),
	GetElectronMvaIDCutEB2(GetElectronMvaIDCutEB2),
	GetElectronMvaIDCutEE(GetElectronMvaIDCutEE),
	GetElectronChargedIsoVetoConeSizeEB(GetElectronChargedIsoVetoConeSizeEB),
	GetElectronChargedIsoVetoConeSizeEE(GetElectronChargedIsoVetoConeSizeEE),
	GetElectronNeutralIsoVetoConeSize(GetElectronNeutralIsoVetoConeSize),
	GetElectronPhotonIsoVetoConeSizeEB(GetElectronPhotonIsoVetoConeSizeEB),
	GetElectronPhotonIsoVetoConeSizeEE(GetElectronPhotonIsoVetoConeSizeEE),
	GetElectronDeltaBetaIsoVetoConeSize(GetElectronDeltaBetaIsoVetoConeSize),
	GetElectronChargedIsoPtThreshold(GetElectronChargedIsoPtThreshold),
	GetElectronNeutralIsoPtThreshold(GetElectronNeutralIsoPtThreshold),
	GetElectronPhotonIsoPtThreshold(GetElectronPhotonIsoPtThreshold),
	GetElectronDeltaBetaIsoPtThreshold(GetElectronDeltaBetaIsoPtThreshold),
	GetElectronIsoSignalConeSize(GetElectronIsoSignalConeSize),
	GetElectronDeltaBetaCorrectionFactor(GetElectronDeltaBetaCorrectionFactor),
	GetElectronIsoPtSumOverPtLowerThresholdEB(GetElectronIsoPtSumOverPtLowerThresholdEB),
	GetElectronIsoPtSumOverPtLowerThresholdEE(GetElectronIsoPtSumOverPtLowerThresholdEE),
	GetElectronIsoPtSumOverPtUpperThresholdEB(GetElectronIsoPtSumOverPtUpperThresholdEB),
	GetElectronIsoPtSumOverPtUpperThresholdEE(GetElectronIsoPtSumOverPtUpperThresholdEE),
	GetElectronTrackDxyCut(GetElectronTrackDxyCut),
	GetElectronTrackDzCut(GetElectronTrackDzCut),
	GetElectronIDList(GetElectronIDList)
{
}

void HttValidElectronsProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ValidElectronsProducer<HttTypes>::Init(settings, metadata);
	
	electronIDType = ToElectronIDType(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.*GetElectronIDType)())));

	electronIDInMetadata = false;
	electronIDListInMetadata = false;

	electronIDName = (settings.*GetElectronIDName)();
	electronIDList = (settings.*GetElectronIDList)();

	electronMvaIDCutEB1 = (settings.*GetElectronMvaIDCutEB1)();
	electronMvaIDCutEB2 = (settings.*GetElectronMvaIDCutEB2)();
	electronMvaIDCutEE = (settings.*GetElectronMvaIDCutEE)();

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingEleIso", [this](event_type const& event, product_type const& product) {
		return product.m_validElectrons.size() >= 1 ? SafeMap::GetWithDefault(product.m_electronIsolation, product.m_validElectrons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingEleIsoOverPt", [this](event_type const& event, product_type const& product) {
		return product.m_validElectrons.size() >= 1 ? SafeMap::GetWithDefault(product.m_electronIsolationOverPt, product.m_validElectrons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "id_e_mva_nt_loose_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(electronIDList.at(0), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "id_e_cut_veto_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(electronIDList.at(1), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "id_e_cut_loose_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(electronIDList.at(2), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "id_e_cut_medium_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(electronIDList.at(3), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "id_e_cut_tight_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(electronIDList.at(4), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
}

bool HttValidElectronsProducer::AdditionalCriteria(KElectron* electron,
                                                   event_type const& event, product_type& product,
                                                   setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_vertexSummary);
	
	bool validElectron = ValidElectronsProducer<HttTypes>::AdditionalCriteria(electron, event, product, settings, metadata);
	
	double isolationPtSum = DefaultValues::UndefinedDouble;
	
	// require no missing inner hits
	if (validElectron && electronReco == ElectronReco::USER) {
		validElectron = validElectron && (electron->track.nInnerHits == 0);
	}

	// custom WPs for electron ID
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID
	if (validElectron && electronID == ElectronID::USER) {
		if (electronIDType == ElectronIDType::SUMMER2013LOOSE)
		{
			validElectron = validElectron && IsMVANonTrigElectronHttSummer2013(&(*electron), event, false);
		}
		else if (electronIDType == ElectronIDType::SUMMER2013TIGHT)
		{
			validElectron = validElectron && IsMVANonTrigElectronHttSummer2013(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::SUMMER2013TTHLOOSE)
		{
			validElectron = validElectron && IsMVATrigElectronTTHSummer2013(&(*electron), event, false);
		}
		else if (electronIDType == ElectronIDType::SUMMER2013TTHTIGHT)
		{
			validElectron = validElectron && IsMVATrigElectronTTHSummer2013(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2015ANDLATER)
		{
			assert(CheckElectronMetadata(event.m_electronMetadata, electronIDName, electronIDInMetadata));
			assert(CheckElectronMetadata(event.m_electronMetadata, electronIDList, electronIDListInMetadata));
			validElectron = validElectron && IsCutBased(&(*electron), event, electronIDName);
		}
		else if (electronIDType == ElectronIDType::MVABASED2015ANDLATER)
		{
			assert(CheckElectronMetadata(event.m_electronMetadata, electronIDName, electronIDInMetadata));
			assert(CheckElectronMetadata(event.m_electronMetadata, electronIDList, electronIDListInMetadata));
			validElectron = validElectron && IsMVABased(&(*electron), event, electronIDName);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2015NOISOANDIPCUTSVETO)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.0114, 0.0152, 0.216, 0.181, 0.207, 2) :
					IsCutBased(&(*electron),event, 0.0352, 0.0113, 0.237, 0.116, 0.174, 3)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2015NOISOANDIPCUTSLOOSE)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.0103, 0.0105, 0.115, 0.104, 0.102, 2) :
					IsCutBased(&(*electron),event, 0.0301, 0.00814, 0.182, 0.0897, 0.126, 1)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2015NOISOANDIPCUTSMEDIUM)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.0101, 0.0103, 0.0366, 0.0876, 0.0174, 2) :
					IsCutBased(&(*electron),event, 0.0283, 0.00733, 0.114, 0.0678, 0.0898, 1)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2015NOISOANDIPCUTSTIGHT)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.0101, 0.00926, 0.0336, 0.0597, 0.012, 2) :
					IsCutBased(&(*electron),event, 0.0279, 0.00724, 0.0918, 0.0615, 0.00999, 1)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2016NOISOCUTSVETO)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.0115, 0.00749, 0.228, 0.356, 0.299, 2, 2016) :
					IsCutBased(&(*electron),event, 0.037, 0.00895, 0.213, 0.211, 0.15, 3, 2016)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2016NOISOCUTSLOOSE)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.011, 0.00477, 0.222, 0.298, 0.241, 1, 2016) :
					IsCutBased(&(*electron),event, 0.0314, 0.00868, 0.213, 0.101, 0.14, 1, 2016)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2016NOISOCUTSMEDIUM)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.00998, 0.00311, 0.103, 0.253, 0.134, 1, 2016) :
					IsCutBased(&(*electron),event, 0.0298, 0.00609, 0.045, 0.0878, 0.13, 1, 2016)
			);
		}
		else if (electronIDType == ElectronIDType::CUTBASED2016NOISOCUTSTIGHT)
		{
			validElectron = validElectron &&
			(
					std::abs(electron->superclusterPosition.Eta()) <= DefaultValues::EtaBorderEB ?
					IsCutBased(&(*electron), event, 0.00998, 0.00308, 0.0816, 0.0414, 0.0129, 1, 2016) :
					IsCutBased(&(*electron),event, 0.0292, 0.00605, 0.0394, 0.0641, 0.0129, 1, 2016)
			);
		}
		else if (electronIDType != ElectronIDType::NONE)
			LOG(FATAL) << "Electron ID type of type " << Utility::ToUnderlyingValue(electronIDType) << " not yet implemented!";
	}

	// custom electron isolation with delta beta correction
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_Muon_Isolation
	if (validElectron && electronIsoType == ElectronIsoType::USER) {
		if (product.m_pfChargedHadronsFromFirstPV.size() > 0 &&
		    product.m_pfNeutralHadronsFromFirstPV.size() > 0 &&
		    product.m_pfPhotonsFromFirstPV.size() > 0 &&
		    product.m_pfChargedHadronsNotFromFirstPV.size() > 0)
		{
			isolationPtSum = ParticleIsolation::IsolationPtSum(
					electron->p4, product,
					(settings.*GetElectronIsoSignalConeSize)(),
					(settings.*GetElectronDeltaBetaCorrectionFactor)(),
					(settings.*GetElectronChargedIsoVetoConeSizeEB)(),
					(settings.*GetElectronChargedIsoVetoConeSizeEE)(),
					(settings.*GetElectronNeutralIsoVetoConeSize)(),
					(settings.*GetElectronPhotonIsoVetoConeSizeEB)(),
					(settings.*GetElectronPhotonIsoVetoConeSizeEE)(),
					(settings.*GetElectronDeltaBetaIsoVetoConeSize)(),
					(settings.*GetElectronChargedIsoPtThreshold)(),
					(settings.*GetElectronNeutralIsoPtThreshold)(),
					(settings.*GetElectronPhotonIsoPtThreshold)(),
					(settings.*GetElectronDeltaBetaIsoPtThreshold)()
			);
		}
		else {
			isolationPtSum = electron->pfIso((settings.*GetElectronDeltaBetaCorrectionFactor)());
		}
		
		double isolationPtSumOverPt = isolationPtSum / electron->p4.Pt();
		
		product.m_leptonIsolation[electron] = isolationPtSum;
		product.m_leptonIsolationOverPt[electron] = isolationPtSumOverPt;
		product.m_electronIsolation[electron] = isolationPtSum;
		product.m_electronIsolationOverPt[electron] = isolationPtSumOverPt;
		
		if (std::abs(electron->p4.Eta()) < DefaultValues::EtaBorderEB)
		{
			if ((isolationPtSumOverPt > (settings.*GetElectronIsoPtSumOverPtLowerThresholdEB)()) &&
			    (isolationPtSumOverPt < (settings.*GetElectronIsoPtSumOverPtUpperThresholdEB)()))
			{
				validElectron = settings.GetDirectIso();
			}
			else
			{
				validElectron = (! settings.GetDirectIso());
			}
		}
		else
		{
			if ((isolationPtSumOverPt > (settings.*GetElectronIsoPtSumOverPtLowerThresholdEE)()) &&
			    (isolationPtSumOverPt < (settings.*GetElectronIsoPtSumOverPtUpperThresholdEE)()))
			{
				validElectron = settings.GetDirectIso();
			}
			else
			{
				validElectron = (! settings.GetDirectIso());
			}
		}
	}
	
	// (tighter) cut on impact parameters of track
	validElectron = validElectron
	                && ((settings.*GetElectronTrackDxyCut)() <= 0.0 || std::abs(electron->dxy) < (settings.*GetElectronTrackDxyCut)())
	                && ((settings.*GetElectronTrackDzCut)() <= 0.0 || std::abs(electron->dz) < (settings.*GetElectronTrackDzCut)());

	return validElectron;
}

bool HttValidElectronsProducer::IsMVATrigElectronTTHSummer2013(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;
	
	validElectron = validElectron && electron->getId("mvaTrigV0", event.m_electronMetadata) > (tightID ? 0.5 : 0.5);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVANonTrigElectronHttSummer2013(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;
	
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID
	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > 0.925)
					|| (std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > 0.915)
					|| (std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > 0.965)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > (tightID ? 0.925 : 0.905))
					|| (std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > (tightID ? 0.975 : 0.955))
					|| (std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > (tightID ? 0.985 : 0.975))
				)
			)
		);

	return validElectron;
}

bool HttValidElectronsProducer::IsCutBased(KElectron* electron, event_type const& event, const std::string &idName) const
{
	bool validElectron = true;

	validElectron = validElectron
			&& electron->getId(idName, event.m_electronMetadata);

	return validElectron;
}

// This function uses the same criteria as the one above with the exception of
// isolation (and impact parameters for 2015 Id). Cut values are taken from
// https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
bool HttValidElectronsProducer::IsCutBased(KElectron* electron, event_type const& event,
			float full5x5_sigmaIetaIeta, float dEtaIn_Seed, float dPhiIn,
			float hOverE, float invEMinusInvP, int missingHits, int year) const
{
	bool validElectron = true;

	validElectron = validElectron && (! (electron->electronType & (1 << KElectronType::hasConversionMatch)));

	validElectron = validElectron &&
	(
		electron->full5x5_sigmaIetaIeta < full5x5_sigmaIetaIeta &&
		electron->dPhiIn < dPhiIn &&
		electron->hadronicOverEm < hOverE &&
		electron->invEMinusInvP() < invEMinusInvP &&
		electron->track.nInnerHits <= missingHits
	);

	if (year == 2016)
		validElectron = validElectron && (electron->dEtaInSeed < dEtaIn_Seed);
	else
		validElectron = validElectron && (electron->dEtaIn < dEtaIn_Seed);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const
{
	bool validElectron = true;

	// https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#General_Purpose_MVA_training_det
	// pT always greater than 10 GeV
	validElectron = validElectron &&
		(
			(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEB1)
			||
			(std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEB2)
			||
			(std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEE)
		);

	return validElectron;
}

bool HttValidElectronsProducer::CheckElectronMetadata(const KElectronMetadata *meta, std::string idName, bool &checkedAlready) const
{
	if(!checkedAlready && !Utility::Contains(meta->idNames, idName))
		LOG(FATAL) << "HttValidElectronsProducer::CheckElectronMetadata: could not find following Id in electron metadata. " << idName << std::endl;

	checkedAlready = true;

	return checkedAlready;
}

bool HttValidElectronsProducer::CheckElectronMetadata(const KElectronMetadata *meta, std::vector<std::string> idNames, bool &checkedAlready) const
{
	if(!checkedAlready)
	{
		for(auto idName : idNames)
		{
			if(!Utility::Contains(meta->idNames, idName))
				LOG(FATAL) << "HttValidElectronsProducer::CheckElectronMetadata: could not find following Id in electron metadata. " << idName << std::endl;
		}
	}

	checkedAlready = true;

	return checkedAlready;
}

HttValidLooseElectronsProducer::HttValidLooseElectronsProducer(
		std::vector<KElectron*> product_type::*validElectrons,
		std::vector<KElectron*> product_type::*invalidElectrons,
		std::string (setting_type::*GetElectronID)(void) const,
		std::string (setting_type::*GetElectronIDType)(void) const,
		std::string (setting_type::*GetElectronIDName)(void) const,
		float (setting_type::*GetElectronMvaIDCutEB1)(void) const,
		float (setting_type::*GetElectronMvaIDCutEB2)(void) const,
		float (setting_type::*GetElectronMvaIDCutEE)(void) const,
		std::string (setting_type::*GetElectronIsoType)(void) const,
		std::string (setting_type::*GetElectronIso)(void) const,
		std::string (setting_type::*GetElectronReco)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronIsoSignalConeSize)(void) const,
		float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetElectronTrackDxyCut)(void) const,
		float (setting_type::*GetElectronTrackDzCut)(void) const
) :
	HttValidElectronsProducer(validElectrons,
	                          invalidElectrons,
	                          GetElectronID,
	                          GetElectronIDType,
	                          GetElectronIDName,
	                          GetElectronMvaIDCutEB1,
	                          GetElectronMvaIDCutEB2,
	                          GetElectronMvaIDCutEE,
	                          GetElectronIsoType,
	                          GetElectronIso,
	                          GetElectronReco,
	                          GetLowerPtCuts,
	                          GetUpperAbsEtaCuts,
	                          GetElectronChargedIsoVetoConeSizeEB,
	                          GetElectronChargedIsoVetoConeSizeEE,
	                          GetElectronNeutralIsoVetoConeSize,
	                          GetElectronPhotonIsoVetoConeSizeEB,
	                          GetElectronPhotonIsoVetoConeSizeEE,
	                          GetElectronDeltaBetaIsoVetoConeSize,
	                          GetElectronChargedIsoPtThreshold,
	                          GetElectronNeutralIsoPtThreshold,
	                          GetElectronPhotonIsoPtThreshold,
	                          GetElectronDeltaBetaIsoPtThreshold,
	                          GetElectronIsoSignalConeSize,
	                          GetElectronDeltaBetaCorrectionFactor,
	                          GetElectronIsoPtSumOverPtLowerThresholdEB,
	                          GetElectronIsoPtSumOverPtLowerThresholdEE,
	                          GetElectronIsoPtSumOverPtUpperThresholdEB,
	                          GetElectronIsoPtSumOverPtUpperThresholdEE,
	                          GetElectronTrackDxyCut,
	                          GetElectronTrackDzCut)
{
}



HttValidVetoElectronsProducer::HttValidVetoElectronsProducer(
		std::vector<KElectron*> product_type::*validElectrons,
		std::vector<KElectron*> product_type::*invalidElectrons,
		std::string (setting_type::*GetElectronID)(void) const,
		std::string (setting_type::*GetElectronIDType)(void) const,
		std::string (setting_type::*GetElectronIDName)(void) const,
		float (setting_type::*GetElectronMvaIDCutEB1)(void) const,
		float (setting_type::*GetElectronMvaIDCutEB2)(void) const,
		float (setting_type::*GetElectronMvaIDCutEE)(void) const,
		std::string (setting_type::*GetElectronIsoType)(void) const,
		std::string (setting_type::*GetElectronIso)(void) const,
		std::string (setting_type::*GetElectronReco)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronIsoSignalConeSize)(void) const,
		float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetElectronTrackDxyCut)(void) const,
		float (setting_type::*GetElectronTrackDzCut)(void) const
) :
	HttValidElectronsProducer(validElectrons,
	                          invalidElectrons,
	                          GetElectronID,
	                          GetElectronIDType,
	                          GetElectronIDName,
	                          GetElectronMvaIDCutEB1,
	                          GetElectronMvaIDCutEB2,
	                          GetElectronMvaIDCutEE,
	                          GetElectronIsoType,
	                          GetElectronIso,
	                          GetElectronReco,
	                          GetLowerPtCuts,
	                          GetUpperAbsEtaCuts,
	                          GetElectronChargedIsoVetoConeSizeEB,
	                          GetElectronChargedIsoVetoConeSizeEE,
	                          GetElectronNeutralIsoVetoConeSize,
	                          GetElectronPhotonIsoVetoConeSizeEB,
	                          GetElectronPhotonIsoVetoConeSizeEE,
	                          GetElectronDeltaBetaIsoVetoConeSize,
	                          GetElectronChargedIsoPtThreshold,
	                          GetElectronNeutralIsoPtThreshold,
	                          GetElectronPhotonIsoPtThreshold,
	                          GetElectronDeltaBetaIsoPtThreshold,
	                          GetElectronIsoSignalConeSize,
	                          GetElectronDeltaBetaCorrectionFactor,
	                          GetElectronIsoPtSumOverPtLowerThresholdEB,
	                          GetElectronIsoPtSumOverPtLowerThresholdEE,
	                          GetElectronIsoPtSumOverPtUpperThresholdEB,
	                          GetElectronIsoPtSumOverPtUpperThresholdEE,
	                          GetElectronTrackDxyCut,
	                          GetElectronTrackDzCut)
{
}

