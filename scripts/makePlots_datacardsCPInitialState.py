#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import pprint
import numpy

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.initialstatecpstudiesdatacards as initialstatecpstudiesdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for SM HTT analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("--cpstudy", nargs="+", required=True,
	                    default=["initial"],
	                    choices=["initial", "final"],
	                    help="Choose which CP study to do: initial state or final state. [Default: %(default)s]")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["et", "mt", "tt", "em"],
	                    help="Channel. This argument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append",
	                    default=[["inclusive"]],
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--cp-mixings", nargs="+", type=float,
	                    default=list(numpy.arange(0.0, 1.001, 0.1)),
	                    help="CP mixing angles alpha_tau (in units of pi/2) to be probed. [Default: %(default)s]")
	parser.add_argument("--cp-mixing-scan-points", type=int, default=((len(parser.get_default("cp_mixings"))-1)*4)+1,
	                    help="Number of points for CP mixing angles alpha_tau (in units of pi/2) to be scanned. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="jdphi",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=False,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--auto-rebin", action="store_true", default=False,
	                    help="Do auto rebinning [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--do-not-normalize-by-bin-width", default=False, action="store_true",
	                    help="Turn off normalization by bin width [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("-b", "--background-method", default="new",
	                    help="Background estimation method to be used. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/htt_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--scale-lumi", default=False,
	                    help="Scale datacard to luminosity specified. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
	                    help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--use-rateParam", action="store_true", default=False,
	                    help="Use rate parameter to estimate ZTT normalization from ZMM. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--x-bins", default=None,
	                    help="Manualy set the binning. Default is taken from configuration files.")
	parser.add_argument("--debug-plots", default=False, action="store_true",
	                    help="Produce debug Plots [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--no-shape-uncs", default=False, action="store_true",
	                    help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--no-syst-uncs", default=False, action="store_true",
	                    help="Do not include systematic uncertainties. This should only be used together with --use-asimov-dataset. [Default: %(default)s]")
	parser.add_argument("--steps", nargs="+",
	                    default=["maxlikelihoodfit", "prefitpostfitplots", "pvalue", "likelihoodScan"],
	                    choices=["maxlikelihoodfit", "prefitpostfitplots", "pvalue", "nuisanceimpacts", "likelihoodScan", "yields"],
	                    help="Steps to perform. [Default: %(default)s]")
	parser.add_argument("--use-shape-only", action="store_true", default=False,
	                    help="Use only shape to distinguish between cp hypotheses. [Default: %(default)s]")
	parser.add_argument("--production-mode", nargs="+",
	                    default=["ggh", "qqh"],
	                    choices=["ggh", "qqh"],
	                    help="Choose the production modes. Option needed for initial state studies. [Default: %(default)s]")
	parser.add_argument("--hypothesis", nargs="+",
	                    default=["susycpodd"],
	                    choices=["susycpodd", "cpodd", "cpmix"],
	                    help="Choose the hypothesis to test against CPeven hypothesis. Option needed for final state studies. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	elif args.era == "2016":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)
	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)
	
	# preparation of CP mixing angles alpha_tau/(pi/2)
	args.cp_mixings.sort()
	cp_mixing_angles = ["{mixing:03d}".format(mixing=int(mixing*100)) for mixing in args.cp_mixings]
	cp_mixings_str = cp_mixing_angles
	
	cp_mixings_scan = list(numpy.arange(args.cp_mixings[0], args.cp_mixings[-1]+0.001, (args.cp_mixings[-1]-args.cp_mixings[0])/(args.cp_mixing_scan_points-1)))
	cp_mixings_combine_range_min = (3*cp_mixings_scan[0]-cp_mixings_scan[1]) / 2.0
	cp_mixings_combine_range_max = (3*cp_mixings_scan[-1]-cp_mixings_scan[-2]) / 2.0
	
	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []
	signal_processes = []

	# set the signal processes
	# initial state studies
	if "initial" in args.cpstudy:
		if "ggh" in args.production_mode:
			signal_processes.append("ggHsm")
			#signal_processes.append("ggHps_ALT")
		if "qqh" in args.production_mode:
			signal_processes.append("qqHsm")
			#signal_processes.append("qqHps_ALT")
	# final state studies
	if "final" in args.cpstudy:
		if "susycpodd" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("SUSYCPODD_ALT")
		if "cpodd" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("CPODD_ALT")
		if "cpmix" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("CPMIX_ALT")
	
	datacards = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(cp_mixings_str, higgs_masses=args.higgs_masses,useRateParam=args.use_rateParam,year=args.era, signal_processes=signal_processes) # TODO: derive own version from this class DONE
		
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = [
		"datacards/individual/${CHANNEL}/${BINID}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
		#"datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
		#"datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt",
		"datacards/combined/${ANALYSIS}_${ERA}.txt",
	]
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"

	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]

	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]

	# catch if on command-line only one set has been specified and repeat it
	if(len(args.categories) == 1):
		args.categories = [args.categories[0]] * len(args.channel)

	#restriction to CH
	datacards.cb.channel(args.channel)

	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_shape_uncs or args.no_syst_uncs:
		log.debug("Deactivate shape uncertainties")
		datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()
			
	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		# include channel prefix
		categories= [channel + "_" + category for category in categories]
		# prepare category settings based on args and datacards
		categories_save = sorted(categories)
		categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		if(categories_save != sorted(categories)):
			log.fatal("CombineHarverster removed the following categories automatically. Was this intended?")
			log.fatal(list(set(categories_save) - set(categories)))
			sys.exit(1)
		
		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
	
		for category in categories:			
			exclude_cuts = args.exclude_cuts
			# higgs_masses = [mass for mass in datacards.cb.mass_set() if mass != "*"]
			higgs_masses = args.higgs_masses[:1]
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="htt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
			))
			#merged_output_files.append(output_file)
			output_files.append(output_file)
			tmp_output_files = []
			
			for shape_systematic, list_of_samples in datacards.get_samples_per_shape_systematic(channel, category).iteritems():
				nominal = (shape_systematic == "nominal")
				list_of_bkg_samples = [datacards.configs.process2sample(process) for process in list_of_samples if process in datacards.cb.cp().channel([channel]).bin([category]).cp().backgrounds().process_set()]
				list_of_sig_samples = [datacards.configs.process2sample(process) for process in list_of_samples if process in datacards.cb.cp().channel([channel]).bin([category]).cp().signals().process_set()]

				# list_of_samples = (["data"] if nominal else []) + [datacards.configs.process2sample(process) for process in list_of_samples]

				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
										
					config={}
					
					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
							samples="\", \"".join(list_of_samples),
							channel=channel,
							category=category,
							systematic=systematic
					))
						
					# prepare plotting configs for retrieving the input histograms
					
					# bkg and data do not need a reweighting so seperate sig and bkg.
					config_bkg = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in (["data"] if nominal else []) + list_of_bkg_samples],
							channel=channel,
							category="catHtt13TeV_"+category,
							weight=args.weight,
							lumi = args.lumi * 1000,
							exclude_cuts=exclude_cuts,
							cut_type="cp2016",
							estimationMethod=args.background_method
					)
			
					# config the labels used for the different systematics.
					config_bkg["labels"] = [(bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template).replace("$", "").format(
						PROCESS=datacards.configs.sample2process(sample),
						BIN=category,
						SYSTEMATIC=systematic
					) for sample in config_bkg["labels"]]
					
					config = samples.Samples.merge_configs(config, config_bkg)
					
					# Set up the config for the signal samples for each given cp_mixing angle. 				
					for cp_mixing, cp_mixing_angle, cp_mixing_str in zip(args.cp_mixings, cp_mixing_angles, cp_mixings_str):
						
						log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
								samples="\", \"".join(list_of_sig_samples),
								channel=channel,
								category=category,
								systematic=systematic
						))	 
						# print("Make config for mixing: " + str(cp_mixing) + " Angle: " + str(cp_mixing_angle) )
						# reweight according to the cp study
						if "final" in args.cpstudy:
							signal_reweighting_factor = "*"+"tauSpinnerWeightInvSample"+"*tauSpinnerWeight"+cp_mixing_angle
							print(signal_reweighting_factor)
						else:
							signal_reweighting_factor = "*(madGraphWeightSample>-899)"+"*madGraphWeightInvSample"+"*madGraphWeight"+cp_mixing_angle
						
						config_sig = sample_settings.get_config(
								samples=[getattr(samples.Samples, sample) for sample in list_of_sig_samples],
								channel=channel,
								category="catHtt13TeV_"+category,
								nick_suffix="_"+cp_mixing_str,
								weight=args.weight+signal_reweighting_factor,
								lumi=args.lumi * 1000,
								exclude_cuts=exclude_cuts,
								higgs_masses=higgs_masses,
								cut_type = "cp2016"
						)
						# config labels need the MASS keyword to find the right histograms.
						config_sig["labels"] = [(sig_histogram_name_template if nominal else sig_syst_histogram_name_template).replace("$", "").format(
								PROCESS=datacards.configs.sample2process(sample).replace("120", "").replace("125", "").replace("130", ""),
								BIN=category,
								MASS=cp_mixing_str,
								SYSTEMATIC=systematic
						) for sample in config_sig["labels"]]
							
						config = samples.Samples.merge_configs(config, config_sig, additional_keys=["shape_nicks", "yield_nicks", "shape_yield_nicks"])
					
					systematics_settings = systematics_factory.get(shape_systematic)(config)
					
					# TODO: evaluate shift from datacards.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					config["qcd_subtract_shape"] = [args.qcd_subtract_shapes]
					config["x_expressions"] =  [args.quantity]

					if "initial" in args.cpstudy:
						binnings_key = "tt_absjdphi"
					if "final" in args.cpstudy:
						binnings_key = "tt_phiStarCP"
					if (binnings_key in binnings_settings.binnings_dict) and args.x_bins == None:
						config["x_bins"] = [binnings_key]
					elif args.x_bins != None:
						config["x_bins"] = [args.x_bins]
					else:
						log.fatal("binnings key " + binnings_key + " not found in binnings_dict! Available binnings are (see HiggsAnalysis/KITHiggsToTauTau/python/plotting/configs/binnings.py):")
						for key in binnings_settings.binnings_dict:
							log.debug(key)
						sys.exit()
					# set quantity x depending on the category
					if "final" in args.cpstudy:
						if all(["RHOmethod" in c for c in categories]):
							config["x_expressions"] = ["recoPhiStarCP_rho_merged"]
							args.quantity = "recoPhiStarCP_rho_merged"
						elif all(["COMBmethod" in c for c in categories]):
							config["x_expressions"] = ["recoPhiStarCPCombMerged"]
							args.quantity = "recoPhiStarCPCombMerged"
						else:
							log.fatal("YOU SHALL NOT PASS different types of category (COMB and RHO) to the same channel. Repeat the channel for the each type of category.")
							raise ValueError("You shall not pass different types of category (COMB and RHO) to the same channel. Repeat the channel for the each type of category.")


					config["directories"] = [args.input_dir]
					
					# histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					# config["labels"] = [histogram_name_template.replace("$", "").format(
					# 		PROCESS=datacards.configs.sample2process(sample.replace("wh125", "wh").replace("zh125", "zh")),
					# 		BIN=category,
					# 		SYSTEMATIC=systematic
					# ) for sample in config["labels"]]
					tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
							ANALYSIS="htt",
							CHANNEL=channel,
							BIN=category,
							SYSTEMATIC=systematic,
							ERA="13TeV"
					))
					tmp_output_files.append(tmp_output_file)
					config["output_dir"] = os.path.dirname(tmp_output_file)
					config["filename"] = os.path.splitext(os.path.basename(tmp_output_file))[0]
				
					config["plot_modules"] = ["ExportRoot"]
					config["file_mode"] = "UPDATE"
			
					if "legend_markers" in config:
						config.pop("legend_markers")
					
					plot_configs.append(config)
			
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
					DST=output_file,
					SRC=" ".join(tmp_output_files)
			))
			merged_output_files.append(output_file)

	if log.isEnabledFor(logging.DEBUG):
		pprint.pprint(plot_configs)
	
	# delete existing output files
	tmp_output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	for output_file_iterator in tmp_output_files:
		if os.path.exists(output_file_iterator):
			os.remove(output_file_iterator)
			log.debug("Removed file \""+output_file_iterator+"\" before it is recreated again.")
	output_files = list(set(output_files))
	
	# create input histograms with HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
	if args.n_plots[0] != 0:
		tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	if args.debug_plots:
		debug_plot_configs = []
		for output_file in merged_output_files:
			debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
		higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
			os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
			bkg_histogram_name_template, sig_histogram_name_template,
			bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
			update_systematics=True
	)
	
	# add bin-by-bin uncertainties
	if args.add_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.1, merge_threshold=0.5, fix_norm=True
		)
	
	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_syst_uncs:
		log.debug("Deactivate systematic uncertainties")
		if not args.use_asimov_dataset:
			log.warning("Fitting MC to data without systematic uncertainties can lead to unreasonable results.")
		datacards.cb.FilterSysts(lambda systematic : True)
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()
	
	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
	
	def matching_process(obj1, obj2):
		matches = (obj1.bin() == obj2.bin())
		matches = matches and (obj1.process() == obj2.process())
		matches = matches and (obj1.signal() == obj2.signal())
		matches = matches and (obj1.analysis() == obj2.analysis())
		matches = matches and (obj1.era() == obj2.era())
		matches = matches and (obj1.channel() == obj2.channel())
		matches = matches and (obj1.bin_id() == obj2.bin_id())
		matches = matches and (obj1.mass() == obj2.mass())
		return matches
		
	def remove_procs_and_systs_with_zero_yield(proc):
		# TODO: find out why zero yield should be ok in control regions. until then remove them
		#null_yield = not (proc.rate() > 0. or is_control_region(proc))
		null_yield = not proc.rate() > 0.
		if null_yield:
			datacards.cb.FilterSysts(lambda systematic: matching_process(proc,systematic))
		return null_yield
	
	# TODO: comment out the following two commands if you want to use
	#       the SM HTT data card creation method in CombineHarvester
	datacards.cb.FilterProcs(remove_procs_and_systs_with_zero_yield)	
		
	# First, we need to choose two hypothesis to test.
	# The histogram with mixing angle 0.00 is the standard model = null hypothesis.
	# TODO: For inital state and final state the string for the two hypothesis might be different.
	# TODO: Someone might be interested in testing other mixings angles against SM prediction.
	
	# Use an asimov dataset. This line must be here, because otherwise we 
	if args.use_asimov_dataset:
		datacards.replace_observation_by_asimov_dataset(signal_mass="000")
	
	"""
	This option calculates the yields and signal to background ratio for each channel and category defined -c and --categories.
	It considers the 
	"""

	"""
	# TODO: WIP: More elegant programming style planned.
	if "yields" in args.steps:
		for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
			categories= [channel + "_" + category for category in categories]
			# prepare category settings based on args and datacards
			categories_save = sorted(categories)
			categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
			if(categories_save != sorted(categories)):
				log.fatal("CombineHarvester removed the following categories automatically. Was this intended?")
				log.fatal(list(set(categories_save) - set(categories)))
				sys.exit(1)
			
			# restrict CombineHarvester to configured categories:
			datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
			for category in categories:
				bkg_yield = {}
				sig_yield = {}
				print("\n"+ "Channel: "+str(channel)+ " Category: "+str(category)+"\n")
				bkg_procs = datacards.cb.cp().channel([channel]).bin([category]).cp().backgrounds().process_set()
				sig_procs = datacards.cb.cp().channel([channel]).bin([category]).cp().signals().process_set()
				for bkg in bkg_procs:
					bkg_yield[bkg] = datacards.cb.cp().channel([channel]).bin([category]).process([bkg]).no_norm_rate()
				tot_bkg = sum(bkg_yield.values())
				for sig in sig_procs:
					sig_yield[sig] = datacards.cb.cp().channel([channel]).bin([category]).process([sig]).no_norm_rate()
				tot_sig = sum(sig_yield.values())
				print("TotalBkg: "+str(tot_bkg)+ " TotalSig: "+str(tot_sig)+"\n")
				for sig in sig_procs:
					print(str(sig)+"/tot_bkg: ", str(sig_yield[sig]/tot_bkg))
					print(str(sig)+"/tot_sig: ", str(sig_yield[sig]/tot_sig))
		
	if args.auto_rebin:
		datacards.auto_rebin(bin_threshold = 1.0, rebin_mode = 0)

	
	datacards.create_morphing_signals("cpmixing", 0.0, 0.0, 1.0)
	
	# write datacards and call text2workspace
	datacards_cbs = {}
	for datacard_filename_template in datacard_filename_templates:
		datacards_cbs.update(datacards.write_datacards(
				datacard_filename_template.replace("{", "").replace("}", ""),
				output_root_filename_template.replace("{", "").replace("}", ""),
				args.output_dir
		))
	datacards_poi_ranges = {}
	for datacard, cb in datacards_cbs.iteritems():
		channels = cb.channel_set()
		categories = cb.bin_set()
		if len(channels) == 1:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [-100.0, 100.0]
			else:
				datacards_poi_ranges[datacard] = [-50.0, 50.0]
		else:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [-50.0, 50.0]
			else:
				datacards_poi_ranges[datacard] = [-25.0, 25.0]
		
	if "likelihoodScan" in args.steps:
		datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
		
		datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, args.n_processes, "-M MaxLikelihoodFit "+datacards.stable_options+" -n \"\"")
		# -M MaxLikelihoodFit is no longer supported. Indtead MultiDimFit should be used. Without specifying any --algo it perfoerms the usual MLF. 					
		if "prefitpostfitplots" in args.steps:
			datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
			datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : args.quantity}, n_processes=args.n_processes)

			datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["cpmixing"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
			datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="cpmixing"))
							
		datacards.combine(
				datacards_cbs,
				datacards_workspaces,
				None,
				args.n_processes,
				"-M MultiDimFit --algo grid --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setPhysicsModelParameters cpmixing=0.0 --setPhysicsModelParameterRanges cpmixing={RANGE} --points {POINTS} {STABLE} -n \"\"".format(
						STABLE=datacards.stable_options,
						RANGE="{0:f},{1:f}".format(cp_mixings_combine_range_min, cp_mixings_combine_range_max),
						POINTS=args.cp_mixing_scan_points
				)	
		)
		result_plot_configs = []
		for datacard, workspace in datacards_workspaces.iteritems():
			config = jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/likelihood_ratio_alphatau.json"))
			config["directories"] = [os.path.dirname(workspace)]
			config["labels"] = ["TODO"]
			config["output_dir"] = os.path.join(os.path.dirname(workspace), "plots")
			config["filename"] = "likelihoodScan"
			result_plot_configs.append(config)
		
		higgsplot.HiggsPlotter(list_of_config_dicts=result_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes)


	"""
	Pvalue determination to be modified. Treating the mixing angle as MASS the file pattern does not work anymore.
	"""	 	
		# custom physics model
		# datacards_workspaces = datacards.text2workspace(
		# 		datacards_cbs,
		# 		args.n_processes,
		# 		"-P {MODEL} {MODEL_PARAMETERS}".format(
		# 			MODEL="HiggsAnalysis.KITHiggsToTauTau.datacards.higgsmodels:HiggsCPI",
		# 			MODEL_PARAMETERS=""
		# 		)
		# )
	
	#annotation_replacements = {channel : index for (index, channel) in enumerate(["combined", "tt", "mt", "et", "em"])}
	# Max. likelihood fit and postfit plots
	
	#datacards.annotate_trees(
			#datacards_workspaces,
			#"higgsCombine*MaxLikelihoodFit*mH*.root",
			#[[os.path.join(os.path.dirname(template.replace("${CHANNEL}", "(.*)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "channel" in template][0]],
			#annotation_replacements,
			#args.n_processes,
			#None,
			#"-t limit -b channel"
	#)
	#datacards.annotate_trees(
			#datacards_workspaces,
			#"higgsCombine*MaxLikelihoodFit*mH*.root",
			#[[os.path.join(os.path.dirname(template.replace("combined", "(combined)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "combined" in template][0]],
			#annotation_replacements,
			#args.n_processes,
			#None,
			#"-t limit -b channel"
	#)

	# Asymptotic limits
	if "pvalue" in args.steps:	
		# Physics model used for H->ZZ spin/CP studies
		# https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/74x-root6/python/HiggsJPC.py
		datacards_workspaces = datacards.text2workspace(
				datacards_cbs,
				args.n_processes,
				"-P {MODEL} {MODEL_PARAMETERS}".format(
					MODEL="HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs",
					MODEL_PARAMETERS=(("--PO=muFloating" if args.use_shape_only else "") + " --altSignal=100")
				)
		)
				
		datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, " -M HybridNew --testStat=TEV --saveHybridResult --generateNuis=0 --singlePoint 1  --fork 8 -T 20000 -i 1 --clsAcc 0 --fullBToys --generateExt=1 -n \"\"") # TODO: change to HybridNew in the old: --expectSignal=1 -t -1
		#-M HybridNew --testStat=TEV --generateExt=1 --generateNuis=0 fixedMu.root --singlePoint 1 --saveHybridResult --fork 40 -T 1000 -i 1 --clsAcc 0 --fullBToys

		#datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-M ProfileLikelihood -t -1 --expectSignal 1 --toysFrequentist --significance -s %s\"\""%index) # TODO: maybe this can be used to get p-values
		if "prefitpostfitplots" in args.steps:
			datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else "")) 
			datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : args.quantity, "normalize" : not(args.do_not_normalize_by_bin_width), "era" : args.era}, n_processes=args.n_processes,signal_stacked_on_bkg=True)
			datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["x"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
			datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="x") )
			if "nuisanceimpacts" in args.steps:
				datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes)
				
		datacards_hypotestresult=datacards.hypotestresulttree(datacards_cbs, n_processes=args.n_processes, poiname="x" )
		log.info(datacards_hypotestresult)
		if args.use_shape_only:
			datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, " -M HybridNew --testStat=TEV --saveHybridResult --generateNuis=0 --singlePoint 1  --fork 8 -T 20000 -i 1 --clsAcc 0 --fullBToys --generateExt=1 -n \"\"")
		# TODO: I think this line should be deleted.
		pconfig_plots=[]
		for filename in datacards_hypotestresult.values():
			log.info(filename)
			pconfigs={}
			pconfigs["files"]= [filename]
			pconfigs["nicks"]= ["noplot","alternative_hypothesis","null_hypothesis", "q_obs"]
			pconfigs["tree_draw_options"]=["","","","TGraph"]
			#pconfigs[ "marker_sizes"]=[5]
			#pconfigs["marker_styles"]=[34]
			pconfigs[ "markers"]=["line","line","line"]

			pconfigs["y_expressions"]=["None","None","None","0"]
			pconfigs["folders"]=["q"]
			pconfigs["weights"]=["1","type<0","type>0","type==0"]
			pconfigs["x_expressions"]=["q"]
			pconfigs[ "output_dir"]=str(os.path.dirname(filename))
			pconfigs["x_bins"]=["500,-3.15,3.15"]
			if "final" in args.cpstudy:
				pconfigs["x_bins"] = ["500,0,6.28"]

			#pconfigs["scale_factors"]=[1,1,1,900]
			#pconfig["plot_modules"] = ["ExportRoot"]

			pconfigs["analysis_modules"]=["PValue"]
			pconfigs["p_value_alternative_hypothesis_nicks"]=["alternative_hypothesis"]
			pconfigs["p_value_null_hypothesis_nicks"]=["null_hypothesis"]
			pconfigs["p_value_observed_nicks"]=["q_obs"]
			pconfigs["legend"]=[0.7,0.6,0.9,0.88]
			pconfigs["labels"]=["CP-even", "CP-odd", "observed"]
			pconfig_plots.append(pconfigs)
			if "final" in args.cpstudy:
				if "susycpodd" or "cpodd" in args.hypothesis:
					pconfigs["labels"]=["CP-even", "CP-odd", "observed"]
					if args.use_asimov_dataset:
						pconfigs["labels"]=["CP-even", "CP-odd", "asimov"]
				if "cpmix" in args.hypothesis:
					pconfigs["labels"]=["CP-even", "CP-mix", "observed"]
					if args.use_asimov_dataset:
						pconfigs["labels"]=["CP-even", "CP-mix", "asimov"]
			higgsplot.HiggsPlotter(list_of_config_dicts=pconfig_plots, list_of_args_strings=[args.args], n_processes=args.n_processes)
