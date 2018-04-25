# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.IncludeQuantities as iq


class quantities(dict):

    def __init__(self, nickname):
        pass

    def fourVectorQuantities(self):
        return [
            "leadingLepLV",
            "lep1LV",
            "posLepLV",
            "trailingLepLV",
            "lep2LV",
            "negLepLV",
            "leadingGenMatchedLepLV",
            "genMatchedLep1LV",
            "posGenMatchedLepLV",
            "leadingGenMatchedLepFound",
            "genMatchedLep1Found",
            "posGenMatchedLepFound",
            "trailingGenMatchedLepLV",
            "genMatchedLep2LV",
            "negGenMatchedLepLV",
            "trailingGenMatchedLepFound",
            "genMatchedLep2Found",
            "negGenMatchedLepFound",
            "diLepLV",
            "genDiLepLV",
            "genDiLepFound",
            "genDiTauLV",
            "genDiTauFound",
            "leadingJetLV",
            "trailingJetLV",
            "thirdJetLV",
            "fourthJetLV",
            "fifthJetLV",
            "sixthJetLV"
        ]

    def fakeFactorQuantities(self):
        return [
            "jetToTauFakeWeight_comb",
            "jetToTauFakeWeight_qcd_up",
            "jetToTauFakeWeight_qcd_down",
            "jetToTauFakeWeight_w_up",
            "jetToTauFakeWeight_w_down",
            "jetToTauFakeWeight_tt_corr_up",
            "jetToTauFakeWeight_tt_corr_down",
            "jetToTauFakeWeight_tt_stat_up",
            "jetToTauFakeWeight_tt_stat_down",
            "jetToTauFakeWeight_frac_w_up",
            "jetToTauFakeWeight_frac_w_down",
            "jetToTauFakeWeight_frac_qcd_up",
            "jetToTauFakeWeight_frac_qcd_down",
            "jetToTauFakeWeight_frac_tt_up",
            "jetToTauFakeWeight_frac_tt_down",
            "jetToTauFakeWeight_frac_dy_up",
            "jetToTauFakeWeight_frac_dy_down",
            "jetToTauFakeWeight_ff_qcd_ss",
            "jetToTauFakeWeight_ff_qcd_ss_up",
            "jetToTauFakeWeight_ff_qcd_ss_down",
            "jetToTauFakeWeight_ff_qcd_os",
            "jetToTauFakeWeight_ff_qcd_os_up",
            "jetToTauFakeWeight_ff_qcd_os_down",
            "jetToTauFakeWeight_ff_w",
            "jetToTauFakeWeight_ff_w_up",
            "jetToTauFakeWeight_ff_w_down",
            "jetToTauFakeWeight_ff_tt",
            "jetToTauFakeWeight_ff_tt_corr_up",
            "jetToTauFakeWeight_ff_tt_corr_down",
            "jetToTauFakeWeight_ff_tt_stat_up",
            "jetToTauFakeWeight_ff_tt_stat_down"
        ]

    def ExtraTauQuantities(self):
        return [
            "decayDistX_1",
            "decayDistX_2",
            "decayDistY_1",
            "decayDistY_2",
            "decayDistZ_1",
            "decayDistZ_2",
            "decayDistM_1",
            "decayDistM_2",
            "nPhoton_1",
            "nPhoton_2",
            "ptWeightedDetaStrip_1",
            "ptWeightedDetaStrip_2",
            "ptWeightedDphiStrip_1",
            "ptWeightedDphiStrip_2",
            "ptWeightedDrSignal_1",
            "ptWeightedDrSignal_2",
            "ptWeightedDrIsolation_1",
            "ptWeightedDrIsolation_2",
            "leadingTrackChi2_1",
            "leadingTrackChi2_2",
            "eRatio_1",
            "eRatio_2",
            "MVAdxy_sign_1",
            "MVAdxy_sign_2",
            "MVAdxy_abs_1",
            "MVAdxy_abs_2",
            "MVAdxy_signal_1",
            "MVAdxy_signal_2",
            "MVAdxy_ip3d_sign_1",
            "MVAdxy_ip3d_sign_2",
            "MVAdxy_ip3d_abs_1",
            "MVAdxy_ip3d_abs_2",
            "MVAdxy_ip3d_signal_1",
            "MVAdxy_ip3d_signal_2",
            "hasSecondaryVertex_1",
            "hasSecondaryVertex_2",
            "flightLengthSig_1",
            "flightLengthSig_2"
        ]

    def lheWeightsDYQuantities(self):
        return [
            "minPdfLheWeight",
            "maxPdfLheWeight",
            "meanPdfLheWeight",
            "stdevPdfLheWeight",
            "meanPdfLheWeightUp",
            "stdevPdfLheWeightUp",
            "meanPdfLheWeightDown",
            "stdevPdfLheWeightDown",
            "minAlphaSLheWeight",
            "maxAlphaSLheWeight",
            "meanAlphaSLheWeight",
            "stdevAlphaSLheWeight",
            "meanAlphaSLheWeightUp",
            "stdevAlphaSLheWeightUp",
            "meanAlphaSLheWeightDown",
            "stdevAlphaSLheWeightDown",
            "minScaleLheWeight",
            "maxScaleLheWeight",
            "meanScaleLheWeight",
            "stdevScaleLheWeight",
            "meanScaleLheWeightUp",
            "stdevScaleLheWeightUp",
            "meanScaleLheWeightDown",
            "stdevScaleLheWeightDown",
            "NNPDF30_lo_as_0130_LHgrid__Member_0",
            "NNPDF30_lo_as_0130_LHgrid__Member_1",
            "NNPDF30_lo_as_0130_LHgrid__Member_10",
            "NNPDF30_lo_as_0130_LHgrid__Member_100",
            "NNPDF30_lo_as_0130_LHgrid__Member_11",
            "NNPDF30_lo_as_0130_LHgrid__Member_12",
            "NNPDF30_lo_as_0130_LHgrid__Member_13",
            "NNPDF30_lo_as_0130_LHgrid__Member_14",
            "NNPDF30_lo_as_0130_LHgrid__Member_15",
            "NNPDF30_lo_as_0130_LHgrid__Member_16",
            "NNPDF30_lo_as_0130_LHgrid__Member_17",
            "NNPDF30_lo_as_0130_LHgrid__Member_18",
            "NNPDF30_lo_as_0130_LHgrid__Member_19",
            "NNPDF30_lo_as_0130_LHgrid__Member_2",
            "NNPDF30_lo_as_0130_LHgrid__Member_20",
            "NNPDF30_lo_as_0130_LHgrid__Member_21",
            "NNPDF30_lo_as_0130_LHgrid__Member_22",
            "NNPDF30_lo_as_0130_LHgrid__Member_23",
            "NNPDF30_lo_as_0130_LHgrid__Member_24",
            "NNPDF30_lo_as_0130_LHgrid__Member_25",
            "NNPDF30_lo_as_0130_LHgrid__Member_26",
            "NNPDF30_lo_as_0130_LHgrid__Member_27",
            "NNPDF30_lo_as_0130_LHgrid__Member_28",
            "NNPDF30_lo_as_0130_LHgrid__Member_29",
            "NNPDF30_lo_as_0130_LHgrid__Member_3",
            "NNPDF30_lo_as_0130_LHgrid__Member_30",
            "NNPDF30_lo_as_0130_LHgrid__Member_31",
            "NNPDF30_lo_as_0130_LHgrid__Member_32",
            "NNPDF30_lo_as_0130_LHgrid__Member_33",
            "NNPDF30_lo_as_0130_LHgrid__Member_34",
            "NNPDF30_lo_as_0130_LHgrid__Member_35",
            "NNPDF30_lo_as_0130_LHgrid__Member_36",
            "NNPDF30_lo_as_0130_LHgrid__Member_37",
            "NNPDF30_lo_as_0130_LHgrid__Member_38",
            "NNPDF30_lo_as_0130_LHgrid__Member_39",
            "NNPDF30_lo_as_0130_LHgrid__Member_4",
            "NNPDF30_lo_as_0130_LHgrid__Member_40",
            "NNPDF30_lo_as_0130_LHgrid__Member_41",
            "NNPDF30_lo_as_0130_LHgrid__Member_42",
            "NNPDF30_lo_as_0130_LHgrid__Member_43",
            "NNPDF30_lo_as_0130_LHgrid__Member_44",
            "NNPDF30_lo_as_0130_LHgrid__Member_45",
            "NNPDF30_lo_as_0130_LHgrid__Member_46",
            "NNPDF30_lo_as_0130_LHgrid__Member_47",
            "NNPDF30_lo_as_0130_LHgrid__Member_48",
            "NNPDF30_lo_as_0130_LHgrid__Member_49",
            "NNPDF30_lo_as_0130_LHgrid__Member_5",
            "NNPDF30_lo_as_0130_LHgrid__Member_50",
            "NNPDF30_lo_as_0130_LHgrid__Member_51",
            "NNPDF30_lo_as_0130_LHgrid__Member_52",
            "NNPDF30_lo_as_0130_LHgrid__Member_53",
            "NNPDF30_lo_as_0130_LHgrid__Member_54",
            "NNPDF30_lo_as_0130_LHgrid__Member_55",
            "NNPDF30_lo_as_0130_LHgrid__Member_56",
            "NNPDF30_lo_as_0130_LHgrid__Member_57",
            "NNPDF30_lo_as_0130_LHgrid__Member_58",
            "NNPDF30_lo_as_0130_LHgrid__Member_59",
            "NNPDF30_lo_as_0130_LHgrid__Member_6",
            "NNPDF30_lo_as_0130_LHgrid__Member_60",
            "NNPDF30_lo_as_0130_LHgrid__Member_61",
            "NNPDF30_lo_as_0130_LHgrid__Member_62",
            "NNPDF30_lo_as_0130_LHgrid__Member_63",
            "NNPDF30_lo_as_0130_LHgrid__Member_64",
            "NNPDF30_lo_as_0130_LHgrid__Member_65",
            "NNPDF30_lo_as_0130_LHgrid__Member_66",
            "NNPDF30_lo_as_0130_LHgrid__Member_67",
            "NNPDF30_lo_as_0130_LHgrid__Member_68",
            "NNPDF30_lo_as_0130_LHgrid__Member_69",
            "NNPDF30_lo_as_0130_LHgrid__Member_7",
            "NNPDF30_lo_as_0130_LHgrid__Member_70",
            "NNPDF30_lo_as_0130_LHgrid__Member_71",
            "NNPDF30_lo_as_0130_LHgrid__Member_72",
            "NNPDF30_lo_as_0130_LHgrid__Member_73",
            "NNPDF30_lo_as_0130_LHgrid__Member_74",
            "NNPDF30_lo_as_0130_LHgrid__Member_75",
            "NNPDF30_lo_as_0130_LHgrid__Member_76",
            "NNPDF30_lo_as_0130_LHgrid__Member_77",
            "NNPDF30_lo_as_0130_LHgrid__Member_78",
            "NNPDF30_lo_as_0130_LHgrid__Member_79",
            "NNPDF30_lo_as_0130_LHgrid__Member_8",
            "NNPDF30_lo_as_0130_LHgrid__Member_80",
            "NNPDF30_lo_as_0130_LHgrid__Member_81",
            "NNPDF30_lo_as_0130_LHgrid__Member_82",
            "NNPDF30_lo_as_0130_LHgrid__Member_83",
            "NNPDF30_lo_as_0130_LHgrid__Member_84",
            "NNPDF30_lo_as_0130_LHgrid__Member_85",
            "NNPDF30_lo_as_0130_LHgrid__Member_86",
            "NNPDF30_lo_as_0130_LHgrid__Member_87",
            "NNPDF30_lo_as_0130_LHgrid__Member_88",
            "NNPDF30_lo_as_0130_LHgrid__Member_89",
            "NNPDF30_lo_as_0130_LHgrid__Member_9",
            "NNPDF30_lo_as_0130_LHgrid__Member_90",
            "NNPDF30_lo_as_0130_LHgrid__Member_91",
            "NNPDF30_lo_as_0130_LHgrid__Member_92",
            "NNPDF30_lo_as_0130_LHgrid__Member_93",
            "NNPDF30_lo_as_0130_LHgrid__Member_94",
            "NNPDF30_lo_as_0130_LHgrid__Member_95",
            "NNPDF30_lo_as_0130_LHgrid__Member_96",
            "NNPDF30_lo_as_0130_LHgrid__Member_97",
            "NNPDF30_lo_as_0130_LHgrid__Member_98",
            "NNPDF30_lo_as_0130_LHgrid__Member_99",
            "NNPDF30_lo_as_0118_LHgrid__Member_0",
            "Central_scale_variation__mur_0_5_muf_0_5",
            "Central_scale_variation__mur_0_5_muf_1",
            #"Central_scale_variation__mur_0_5_muf_2",
            "Central_scale_variation__mur_1_muf_0_5",
            "Central_scale_variation__mur_1_muf_1",
            "Central_scale_variation__mur_1_muf_2",
            #"Central_scale_variation__mur_2_muf_0_5",
            "Central_scale_variation__mur_2_muf_1",
            "Central_scale_variation__mur_2_muf_2"
        ]

    def lheWeightsHTTQuantities(self):
        return [
            "minPdfLheWeight",
            "maxPdfLheWeight",
            "meanPdfLheWeight",
            "stdevPdfLheWeight",
            "meanPdfLheWeightUp",
            "stdevPdfLheWeightUp",
            "meanPdfLheWeightDown",
            "stdevPdfLheWeightDown",
            "minAlphaSLheWeight",
            "maxAlphaSLheWeight",
            "meanAlphaSLheWeight",
            "stdevAlphaSLheWeight",
            "meanAlphaSLheWeightUp",
            "stdevAlphaSLheWeightUp",
            "meanAlphaSLheWeightDown",
            "stdevAlphaSLheWeightDown",
            "minScaleLheWeight",
            "maxScaleLheWeight",
            "meanScaleLheWeight",
            "stdevScaleLheWeight",
            "meanScaleLheWeightUp",
            "stdevScaleLheWeightUp",
            "meanScaleLheWeightDown",
            "stdevScaleLheWeightDown",
            "PDF_variation__PDF_set___260001",
            "PDF_variation__PDF_set___260002",
            "PDF_variation__PDF_set___260003",
            "PDF_variation__PDF_set___260004",
            "PDF_variation__PDF_set___260005",
            "PDF_variation__PDF_set___260006",
            "PDF_variation__PDF_set___260007",
            "PDF_variation__PDF_set___260008",
            "PDF_variation__PDF_set___260009",
            "PDF_variation__PDF_set___260010",
            "PDF_variation__PDF_set___260011",
            "PDF_variation__PDF_set___260012",
            "PDF_variation__PDF_set___260013",
            "PDF_variation__PDF_set___260014",
            "PDF_variation__PDF_set___260015",
            "PDF_variation__PDF_set___260016",
            "PDF_variation__PDF_set___260017",
            "PDF_variation__PDF_set___260018",
            "PDF_variation__PDF_set___260019",
            "PDF_variation__PDF_set___260020",
            "PDF_variation__PDF_set___260021",
            "PDF_variation__PDF_set___260022",
            "PDF_variation__PDF_set___260023",
            "PDF_variation__PDF_set___260024",
            "PDF_variation__PDF_set___260025",
            "PDF_variation__PDF_set___260026",
            "PDF_variation__PDF_set___260027",
            "PDF_variation__PDF_set___260028",
            "PDF_variation__PDF_set___260029",
            "PDF_variation__PDF_set___260030",
            "PDF_variation__PDF_set___260031",
            "PDF_variation__PDF_set___260032",
            "PDF_variation__PDF_set___260033",
            "PDF_variation__PDF_set___260034",
            "PDF_variation__PDF_set___260035",
            "PDF_variation__PDF_set___260036",
            "PDF_variation__PDF_set___260037",
            "PDF_variation__PDF_set___260038",
            "PDF_variation__PDF_set___260039",
            "PDF_variation__PDF_set___260040",
            "PDF_variation__PDF_set___260041",
            "PDF_variation__PDF_set___260042",
            "PDF_variation__PDF_set___260043",
            "PDF_variation__PDF_set___260044",
            "PDF_variation__PDF_set___260045",
            "PDF_variation__PDF_set___260046",
            "PDF_variation__PDF_set___260047",
            "PDF_variation__PDF_set___260048",
            "PDF_variation__PDF_set___260049",
            "PDF_variation__PDF_set___260050",
            "PDF_variation__PDF_set___260051",
            "PDF_variation__PDF_set___260052",
            "PDF_variation__PDF_set___260053",
            "PDF_variation__PDF_set___260054",
            "PDF_variation__PDF_set___260055",
            "PDF_variation__PDF_set___260056",
            "PDF_variation__PDF_set___260057",
            "PDF_variation__PDF_set___260058",
            "PDF_variation__PDF_set___260059",
            "PDF_variation__PDF_set___260060",
            "PDF_variation__PDF_set___260061",
            "PDF_variation__PDF_set___260062",
            "PDF_variation__PDF_set___260063",
            "PDF_variation__PDF_set___260064",
            "PDF_variation__PDF_set___260065",
            "PDF_variation__PDF_set___260066",
            "PDF_variation__PDF_set___260067",
            "PDF_variation__PDF_set___260068",
            "PDF_variation__PDF_set___260069",
            "PDF_variation__PDF_set___260070",
            "PDF_variation__PDF_set___260071",
            "PDF_variation__PDF_set___260072",
            "PDF_variation__PDF_set___260073",
            "PDF_variation__PDF_set___260074",
            "PDF_variation__PDF_set___260075",
            "PDF_variation__PDF_set___260076",
            "PDF_variation__PDF_set___260077",
            "PDF_variation__PDF_set___260078",
            "PDF_variation__PDF_set___260079",
            "PDF_variation__PDF_set___260080",
            "PDF_variation__PDF_set___260081",
            "PDF_variation__PDF_set___260082",
            "PDF_variation__PDF_set___260083",
            "PDF_variation__PDF_set___260084",
            "PDF_variation__PDF_set___260085",
            "PDF_variation__PDF_set___260086",
            "PDF_variation__PDF_set___260087",
            "PDF_variation__PDF_set___260088",
            "PDF_variation__PDF_set___260089",
            "PDF_variation__PDF_set___260090",
            "PDF_variation__PDF_set___260091",
            "PDF_variation__PDF_set___260092",
            "PDF_variation__PDF_set___260093",
            "PDF_variation__PDF_set___260094",
            "PDF_variation__PDF_set___260095",
            "PDF_variation__PDF_set___260096",
            "PDF_variation__PDF_set___260097",
            "PDF_variation__PDF_set___260098",
            "PDF_variation__PDF_set___260099",
            "PDF_variation__PDF_set___260100",
            "PDF_variation__PDF_set___265000",
            "PDF_variation__PDF_set___266000",
            "scale_variation__muR_1_muF_1",
            "scale_variation__muR_1_muF_2",
            "scale_variation__muR_1_muF_0_5",
            "scale_variation__muR_2_muF_1",
            "scale_variation__muR_2_muF_2",
            #"scale_variation__muR_2_muF_0_5",
            "scale_variation__muR_0_5_muF_1",
            #"scale_variation__muR_0_5_muF_2",
            "scale_variation__muR_0_5_muF_0_5"
        ]

    # possibility to add options for adding only each subset with if statements
    def splitJecUncertaintyQuantities(self):
        splitJecUncertaintyQuantities_list = [
            "njetspt30_AbsoluteFlavMapUp",
            "njetspt30_AbsoluteMPFBiasUp",
            "njetspt30_AbsoluteScaleUp",
            "njetspt30_AbsoluteStatUp",
            "njetspt30_FlavorQCDUp",
            "njetspt30_FragmentationUp",
            "njetspt30_PileUpDataMCUp",
            "njetspt30_PileUpPtBBUp",
            "njetspt30_PileUpPtEC1Up",
            "njetspt30_PileUpPtEC2Up",
            "njetspt30_PileUpPtHFUp",
            "njetspt30_PileUpPtRefUp",
            "njetspt30_RelativeBalUp",
            "njetspt30_RelativeFSRUp",
            "njetspt30_RelativeJEREC1Up",
            "njetspt30_RelativeJEREC2Up",
            "njetspt30_RelativeJERHFUp",
            "njetspt30_RelativePtBBUp",
            "njetspt30_RelativePtEC1Up",
            "njetspt30_RelativePtEC2Up",
            "njetspt30_RelativePtHFUp",
            "njetspt30_RelativeStatECUp",
            "njetspt30_RelativeStatFSRUp",
            "njetspt30_RelativeStatHFUp",
            "njetspt30_SinglePionECALUp",
            "njetspt30_SinglePionHCALUp",
            "njetspt30_TimePtEtaUp",
            "njetspt30_TotalUp",
            "njetspt30_ClosureUp"]

        splitJecUncertaintyQuantities_list += [
            "mjj_AbsoluteFlavMapUp",
            "mjj_AbsoluteMPFBiasUp",
            "mjj_AbsoluteScaleUp",
            "mjj_AbsoluteStatUp",
            "mjj_FlavorQCDUp",
            "mjj_FragmentationUp",
            "mjj_PileUpDataMCUp",
            "mjj_PileUpPtBBUp",
            "mjj_PileUpPtEC1Up",
            "mjj_PileUpPtEC2Up",
            "mjj_PileUpPtHFUp",
            "mjj_PileUpPtRefUp",
            "mjj_RelativeBalUp",
            "mjj_RelativeFSRUp",
            "mjj_RelativeJEREC1Up",
            "mjj_RelativeJEREC2Up",
            "mjj_RelativeJERHFUp",
            "mjj_RelativePtBBUp",
            "mjj_RelativePtEC1Up",
            "mjj_RelativePtEC2Up",
            "mjj_RelativePtHFUp",
            "mjj_RelativeStatECUp",
            "mjj_RelativeStatFSRUp",
            "mjj_RelativeStatHFUp",
            "mjj_SinglePionECALUp",
            "mjj_SinglePionHCALUp",
            "mjj_TimePtEtaUp",
            "mjj_TotalUp",
            "mjj_ClosureUp"
        ]

        splitJecUncertaintyQuantities_list += [
            "jdeta_AbsoluteFlavMapUp",
            "jdeta_AbsoluteMPFBiasUp",
            "jdeta_AbsoluteScaleUp",
            "jdeta_AbsoluteStatUp",
            "jdeta_FlavorQCDUp",
            "jdeta_FragmentationUp",
            "jdeta_PileUpDataMCUp",
            "jdeta_PileUpPtBBUp",
            "jdeta_PileUpPtEC1Up",
            "jdeta_PileUpPtEC2Up",
            "jdeta_PileUpPtHFUp",
            "jdeta_PileUpPtRefUp",
            "jdeta_RelativeBalUp",
            "jdeta_RelativeFSRUp",
            "jdeta_RelativeJEREC1Up",
            "jdeta_RelativeJEREC2Up",
            "jdeta_RelativeJERHFUp",
            "jdeta_RelativePtBBUp",
            "jdeta_RelativePtEC1Up",
            "jdeta_RelativePtEC2Up",
            "jdeta_RelativePtHFUp",
            "jdeta_RelativeStatECUp",
            "jdeta_RelativeStatFSRUp",
            "jdeta_RelativeStatHFUp",
            "jdeta_SinglePionECALUp",
            "jdeta_SinglePionHCALUp",
            "jdeta_TimePtEtaUp",
            "jdeta_TotalUp",
            "jdeta_ClosureUp"
        ]

        splitJecUncertaintyQuantities_list += [
            "jdphi_AbsoluteFlavMapUp",
            "jdphi_AbsoluteMPFBiasUp",
            "jdphi_AbsoluteScaleUp",
            "jdphi_AbsoluteStatUp",
            "jdphi_FlavorQCDUp",
            "jdphi_FragmentationUp",
            "jdphi_PileUpDataMCUp",
            "jdphi_PileUpPtBBUp",
            "jdphi_PileUpPtEC1Up",
            "jdphi_PileUpPtEC2Up",
            "jdphi_PileUpPtHFUp",
            "jdphi_PileUpPtRefUp",
            "jdphi_RelativeBalUp",
            "jdphi_RelativeFSRUp",
            "jdphi_RelativeJEREC1Up",
            "jdphi_RelativeJEREC2Up",
            "jdphi_RelativeJERHFUp",
            "jdphi_RelativePtBBUp",
            "jdphi_RelativePtEC1Up",
            "jdphi_RelativePtEC2Up",
            "jdphi_RelativePtHFUp",
            "jdphi_RelativeStatECUp",
            "jdphi_RelativeStatFSRUp",
            "jdphi_RelativeStatHFUp",
            "jdphi_SinglePionECALUp",
            "jdphi_SinglePionHCALUp",
            "jdphi_TimePtEtaUp",
            "jdphi_TotalUp",
            "jdphi_ClosureUp"
        ]

        splitJecUncertaintyQuantities_list += [
            "njetspt30_AbsoluteFlavMapDown",
            "njetspt30_AbsoluteMPFBiasDown",
            "njetspt30_AbsoluteScaleDown",
            "njetspt30_AbsoluteStatDown",
            "njetspt30_FlavorQCDDown",
            "njetspt30_FragmentationDown",
            "njetspt30_PileUpDataMCDown",
            "njetspt30_PileUpPtBBDown",
            "njetspt30_PileUpPtEC1Down",
            "njetspt30_PileUpPtEC2Down",
            "njetspt30_PileUpPtHFDown",
            "njetspt30_PileUpPtRefDown",
            "njetspt30_RelativeBalDown",
            "njetspt30_RelativeFSRDown",
            "njetspt30_RelativeJEREC1Down",
            "njetspt30_RelativeJEREC2Down",
            "njetspt30_RelativeJERHFDown",
            "njetspt30_RelativePtBBDown",
            "njetspt30_RelativePtEC1Down",
            "njetspt30_RelativePtEC2Down",
            "njetspt30_RelativePtHFDown",
            "njetspt30_RelativeStatECDown",
            "njetspt30_RelativeStatFSRDown",
            "njetspt30_RelativeStatHFDown",
            "njetspt30_SinglePionECALDown",
            "njetspt30_SinglePionHCALDown",
            "njetspt30_TimePtEtaDown",
            "njetspt30_TotalDown",
            "njetspt30_ClosureDown"
        ]

        splitJecUncertaintyQuantities_list += [
            "mjj_AbsoluteFlavMapDown",
            "mjj_AbsoluteMPFBiasDown",
            "mjj_AbsoluteScaleDown",
            "mjj_AbsoluteStatDown",
            "mjj_FlavorQCDDown",
            "mjj_FragmentationDown",
            "mjj_PileUpDataMCDown",
            "mjj_PileUpPtBBDown",
            "mjj_PileUpPtEC1Down",
            "mjj_PileUpPtEC2Down",
            "mjj_PileUpPtHFDown",
            "mjj_PileUpPtRefDown",
            "mjj_RelativeBalDown",
            "mjj_RelativeFSRDown",
            "mjj_RelativeJEREC1Down",
            "mjj_RelativeJEREC2Down",
            "mjj_RelativeJERHFDown",
            "mjj_RelativePtBBDown",
            "mjj_RelativePtEC1Down",
            "mjj_RelativePtEC2Down",
            "mjj_RelativePtHFDown",
            "mjj_RelativeStatECDown",
            "mjj_RelativeStatFSRDown",
            "mjj_RelativeStatHFDown",
            "mjj_SinglePionECALDown",
            "mjj_SinglePionHCALDown",
            "mjj_TimePtEtaDown",
            "mjj_TotalDown",
            "mjj_ClosureDown"
        ]

        splitJecUncertaintyQuantities_list += [
            "jdeta_AbsoluteFlavMapDown",
            "jdeta_AbsoluteMPFBiasDown",
            "jdeta_AbsoluteScaleDown",
            "jdeta_AbsoluteStatDown",
            "jdeta_FlavorQCDDown",
            "jdeta_FragmentationDown",
            "jdeta_PileUpDataMCDown",
            "jdeta_PileUpPtBBDown",
            "jdeta_PileUpPtEC1Down",
            "jdeta_PileUpPtEC2Down",
            "jdeta_PileUpPtHFDown",
            "jdeta_PileUpPtRefDown",
            "jdeta_RelativeBalDown",
            "jdeta_RelativeFSRDown",
            "jdeta_RelativeJEREC1Down",
            "jdeta_RelativeJEREC2Down",
            "jdeta_RelativeJERHFDown",
            "jdeta_RelativePtBBDown",
            "jdeta_RelativePtEC1Down",
            "jdeta_RelativePtEC2Down",
            "jdeta_RelativePtHFDown",
            "jdeta_RelativeStatECDown",
            "jdeta_RelativeStatFSRDown",
            "jdeta_RelativeStatHFDown",
            "jdeta_SinglePionECALDown",
            "jdeta_SinglePionHCALDown",
            "jdeta_TimePtEtaDown",
            "jdeta_TotalDown",
            "jdeta_ClosureDown"
        ]

        splitJecUncertaintyQuantities_list += [
            "jdphi_AbsoluteFlavMapDown",
            "jdphi_AbsoluteMPFBiasDown",
            "jdphi_AbsoluteScaleDown",
            "jdphi_AbsoluteStatDown",
            "jdphi_FlavorQCDDown",
            "jdphi_FragmentationDown",
            "jdphi_PileUpDataMCDown",
            "jdphi_PileUpPtBBDown",
            "jdphi_PileUpPtEC1Down",
            "jdphi_PileUpPtEC2Down",
            "jdphi_PileUpPtHFDown",
            "jdphi_PileUpPtRefDown",
            "jdphi_RelativeBalDown",
            "jdphi_RelativeFSRDown",
            "jdphi_RelativeJEREC1Down",
            "jdphi_RelativeJEREC2Down",
            "jdphi_RelativeJERHFDown",
            "jdphi_RelativePtBBDown",
            "jdphi_RelativePtEC1Down",
            "jdphi_RelativePtEC2Down",
            "jdphi_RelativePtHFDown",
            "jdphi_RelativeStatECDown",
            "jdphi_RelativeStatFSRDown",
            "jdphi_RelativeStatHFDown",
            "jdphi_SinglePionECALDown",
            "jdphi_SinglePionHCALDown",
            "jdphi_TimePtEtaDown",
            "jdphi_TotalDown",
            "jdphi_ClosureDown"
        ]

        return splitJecUncertaintyQuantities_list

    def svfitSyncQuantities(self):
        return [
            "m_sv",
            "pt_sv",
            "eta_sv",
            "phi_sv",
            "#met_sv",
            "#m_sv_Up",
            "#m_sv_Down",

            "svfitAvailable",
            "svfitLV",
            "svfitTau1Available",
            "svfitTau1LV",
            "svfitTau1ERatio",
            "svfitTau2Available",
            "svfitTau2LV",
            "svfitTau2ERatio",

            "svfitM91Available",
            "svfitM91LV",
            "svfitM91Tau1Available",
            "svfitM91Tau1LV",
            "svfitM91Tau1ERatio",
            "svfitM91Tau2Available",
            "svfitM91Tau2LV",
            "svfitM91Tau2ERatio",

            "svfitM125Available",
            "svfitM125LV",
            "svfitM125Tau1Available",
            "svfitM125Tau1LV",
            "svfitM125Tau1ERatio",
            "svfitM125Tau2Available",
            "svfitM125Tau2LV",
            "svfitM125Tau2ERatio"
        ]

    def syncQuantities(self):
        return [
            "nickname",
            "input",
            "run",
            "lumi",
            "event",
            "evt",
            "npv",
            "npu",
            "rho",
            #"mcweight",
            "puweight",
            #"idweight_1",
            #"idweight_2",
            #"isoweight_1",
            #"isoweight_2",
            #"effweight",
            "weight",
            #"embeddedWeight",
            "m_vis",
            "H_mass",
            "H_pt",
            "diLepMass",
            "diLepMassSmearUp",
            "diLepMassSmearDown",
            "diLepGenMass",
            "diLepMetMt",
            "pt_1",
            "phi_1",
            "eta_1",
            "m_1",
            "q_1",
            "iso_1",
            #"mva_1",
            "d0_1",
            "dZ_1",
            #"passid_1",
            #"passiso_1",
            "mt_1",
            "pt_2",
            "phi_2",
            "eta_2",
            "m_2",
            "q_2",
            "iso_2",
            "d0_2",
            "dZ_2",
            #"mva_2",
            #"passid_2",
            #"passiso_2",
            "mt_2",
            "met",
            "metphi",
            #"l1met",
            #"l1metphi",
            #"l1metcorr",
            #"calomet",
            #"calometphi",
            #"calometcorr",
            #"calometphicorr",
            "mvamet",
            "mvametphi",
            "pzetavis",
            "pzetamiss",
            "pZetaMissVis",
            "metcov00",
            "metcov01",
            "metcov10",
            "metcov11",
            "mvacov00",
            "mvacov01",
            "mvacov10",
            "mvacov11",
            "jpt_1",
            "jeta_1",
            "jphi_1",
            "jm_1",
            "jmva_1",
            "jcsv_1",
            "bpt_1",
            "beta_1",
            "bphi_1",
            "bmva_1",
            "bcsv_1",
            "jpt_2",
            "jeta_2",
            "jphi_2",
            "jm_2",
            "jmva_2",
            "jcsv_2",
            "bpt_2",
            "beta_2",
            "bphi_2",
            "bmva_2",
            "bcsv_2",
            "mjj",
            "jdeta",
            "njetingap",
            "njetingap20",
            "jdphi",
            "dijetpt",
            "dijetphi",
            "hdijetphi",
            "ptvis",
            "nbtag",
            "njets",
            "njetspt20",
            "njetspt30",
            #"mva_gf",
            #"mva_vbf",
            "trigweight_1",
            "chargedIsoPtSum_1",
            "neutralIsoPtSum_1",
            "puCorrPtSum_1",
            "footprintCorrection_1",
            "photonPtSumOutsideSignalCone_1",
            "againstMuonLoose3_1",
            "againstMuonTight3_1",
            "againstElectronLooseMVA6_1",
            "againstElectronMediumMVA6_1",
            "againstElectronTightMVA6_1",
            "againstElectronVLooseMVA6_1",
            "againstElectronVTightMVA6_1",
            "byCombinedIsolationDeltaBetaCorrRaw3Hits_1",
            "byLooseCombinedIsolationDeltaBetaCorr3Hits_1",
            "byMediumCombinedIsolationDeltaBetaCorr3Hits_1",
            "byTightCombinedIsolationDeltaBetaCorr3Hits_1",
            "byIsolationMVArun2v1DBoldDMwLTraw_1",
            "byVLooseIsolationMVArun2v1DBoldDMwLT_1",
            "byLooseIsolationMVArun2v1DBoldDMwLT_1",
            "byMediumIsolationMVArun2v1DBoldDMwLT_1",
            "byTightIsolationMVArun2v1DBoldDMwLT_1",
            "byVTightIsolationMVArun2v1DBoldDMwLT_1",
            "byVVTightIsolationMVArun2v1DBoldDMwLT_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1raw_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1Tight_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1VTight_1",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight_1",
            "decayModeFinding_1",
            "decayModeFindingNewDMs_1",
            "trigweight_2",
            "chargedIsoPtSum_2",
            "neutralIsoPtSum_2",
            "puCorrPtSum_2",
            "footprintCorrection_2",
            "photonPtSumOutsideSignalCone_2",
            "againstMuonLoose3_2",
            "againstMuonTight3_2",
            "againstElectronLooseMVA6_2",
            "againstElectronMediumMVA6_2",
            "againstElectronTightMVA6_2",
            "againstElectronVLooseMVA6_2",
            "againstElectronVTightMVA6_2",
            "byCombinedIsolationDeltaBetaCorrRaw3Hits_2",
            "byLooseCombinedIsolationDeltaBetaCorr3Hits_2",
            "byMediumCombinedIsolationDeltaBetaCorr3Hits_2",
            "byTightCombinedIsolationDeltaBetaCorr3Hits_2",
            "byIsolationMVArun2v1DBoldDMwLTraw_2",
            "byVLooseIsolationMVArun2v1DBoldDMwLT_2",
            "byLooseIsolationMVArun2v1DBoldDMwLT_2",
            "byMediumIsolationMVArun2v1DBoldDMwLT_2",
            "byTightIsolationMVArun2v1DBoldDMwLT_2",
            "byVTightIsolationMVArun2v1DBoldDMwLT_2",
            "byVVTightIsolationMVArun2v1DBoldDMwLT_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1raw_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1Tight_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1VTight_2",
            "rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight_2",
            "decayModeFinding_2",
            "decayModeFindingNewDMs_2",
            "NUP",
            "id_m_loose_1",
            "id_m_medium_1",
            "id_m_tight_1",
            "id_m_highpt_1",
            "id_e_mva_nt_loose_1",
            "id_e_cut_veto_1",
            "id_e_cut_loose_1",
            "id_e_cut_medium_1",
            "id_e_cut_tight_1",
            "pt_tt",
            "dilepton_veto",
            "extraelec_veto",
            "extramuon_veto",
            "gen_match_1",
            "gen_match_2",
            "decayMode_1",
            "decayMode_2",
            "npartons",
            "genbosonmass",
            "leadingJetGenMatch",
            "trailingJetGenMatch"
        ]
