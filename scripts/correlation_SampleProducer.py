#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re

import Artus.Utility.jsonTools as jsonTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as import_binnings
import Artus.Utility.tools as aTools
import ROOT
import glob
import array
import itertools
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def calculate_partial_correlation(config):

	stored_files_list = []
	#construct list of rootfiles, if prepare samples is enabled, files are produced
	c_tree = ""
	c_tree_list = ROOT.TList()
	root_file_name_list = []
	root_storage_file = "%s/%s.root"%(config["storage_name_extension"], "NTuples")
	config["storage_file"] = root_storage_file
	config["storage_ntuple"]=config["folders"][0].replace("/ntuple", "")
	if config["prepare_samples"] and not (os.path.exists(root_storage_file) and not config["overwrite_samples"]):
		log.info("Recreate Sample %s"%root_storage_file)
		cuts = ""
		#find all physical files and store them in root_filename_list
		for i,nick in enumerate(config["nicks"]):
			if not bool(sum([x in nick for x in ["wmh", "wph", "zh"]])) and "noplot" in nick:
				continue
			#next line splits file_string into filenames, those could contain * -> use glob.glob to map * to real names, add the list to root_file_name_list
			map(root_file_name_list.__iadd__, map(glob.glob, map(config["root_input_dir"].__add__, config["files"][i].split(" "))))
			if (not cuts == "") and (not cuts == config["weights"][i]):
				log.error("can not decide which weight to use for sample %s nick %s" %(config["request_nick"],nick))
				log.error(config)
				sys.exit()
			cuts = config["weights"][i]

		for root_file_name in root_file_name_list:
			log.debug("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
			c_tree_list.append(ROOT.TChain())
			root_file_name = root_file_name + '/' + config["folders"][0]
			c_tree_list[-1].Add(root_file_name)
			c_tree_list[-1].SetName("list_tree")

		store_file = ROOT.TFile(root_storage_file, "RECREATE")
		selection_string = cuts.replace("eventWeight*", "")
		if config["request_nick"] in ["ztt", "zll"]:
			selection_string = cuts.replace("eventWeight*", "").replace("*stitchWeight%s"%(config["request_nick"].upper()), "")
		for index in range(len(c_tree_list)):
			log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], root_storage_file))
			c_tree_list[index]=c_tree_list[index].CopyTree(selection_string)
		log.debug("Merge Trees for Sample %s "%root_storage_file)
		if len(c_tree_list) > 1:
			c_tree = ROOT.TTree.MergeTrees(c_tree_list)
		elif len(c_tree_list) == 1:
			c_tree = c_tree_list[0]
		else:
			c_tree =ROOT.TChain()
		log.debug("Prepare Sample %s from %i files"%(root_storage_file,len(c_tree_list)))
		c_tree.SetName(config["folders"][0].replace("/ntuple", ""))
		for i in range(len(c_tree_list)):
			del c_tree_list[0]
		del c_tree_list
		store_file.Write()
		store_file.Close()
	#log.error("Reached Breakpoint, would start calculations next!")
	#sys.exit()
	root_histograms = {}
	corr_vars = {}
	binnings_dict = import_binnings.BinningsDict()
	nick_path = os.path.join(config["output_dir_path"], channel, category, requested_sample)
	if not os.path.exists(nick_path):
		os.makedirs(nick_path)
	root_inf = ROOT.TFile(config["storage_file"], "read")
	root_inst = root_inf.Get(config["storage_ntuple"])
	for variables in itertools.combinations(config["parameters_list"], 2):
		xbins_list = binnings_dict.get_binning("%s_"%config["channel"]+variables[0]).strip()
		ybins_list = binnings_dict.get_binning("%s_"%config["channel"]+variables[1]).strip()
		xbins = []
		ybins = []
		if "," in xbins_list:
			xbins_list = map(float, xbins_list.split(","))
			xbins += xbins_list
			xbins[0] = int(xbins[0])
		elif len(xbins_list.split(" ")) >= 2:
			a_bins_list = array.array('d',map(float, xbins_list.split(" ")))
			xbins_list.append(len(xbins_list.split(" "))-1)
			xbins.append(a_bins_list)
		else:
			xbins = [100,0.,0.]

		if "," in ybins_list:
			ybins_list = map(float, ybins_list.split(","))
			ybins += ybins_list
			ybins[0] = int(ybins[0])
		elif len(ybins_list.split(" ")) >= 2:
			a_bins_list = array.array('d',map(float, ybins_list.split(" ")))
			ybins.append(len(ybins_list.split(" "))-1)
			ybins.append(a_bins_list)
		else:
			ybins = [100,0.,0.]

		binnings = xbins + ybins
		log.debug("Generate RootHistogram TH2F: %s"%("+-+".join(variables)))
		log.debug(binnings)
		root_histograms["+-+".join(variables)] = ROOT.TH2F("+-+".join(variables),
													"correlation: %s vs %s"%variables, *binnings)
		corr_vars["+-+".join(variables)] = 0
		root_histograms["+-+".join(variables)].SetDirectory(0)
		ROOT.SetOwnership (root_histograms["+-+".join(variables)], False)
	for variable in config["parameters_list"]:
		xbins_list = binnings_dict.get_binning("%s_"%config["channel"]+variables[0])
		xbins = []
		if "," in xbins_list:
			xbins_list = map(float, xbins_list.split(","))
			xbins += xbins_list
			xbins[0] = int(xbins[0])
		elif len(xbins_list.split(" ")) >= 2 and xbins_list.split(" ")[1] != "":
			xbins_list = map(float, xbins_list.split(","))
			xbins.append(len(xbins_list.split(" "))-1)
			xbins.apped(a_bins_list)
		else:
			xbins = [100,0.,0.]

		binnings = xbins + xbins
		root_histograms["+-+".join([variable,variable])] = ROOT.TH2F("+-+".join([variable,variable]),
													"correlation: %s vs %s"%(variable,variable), *binnings)
		corr_vars["+-+".join([variable,variable])] = 0
		corr_vars[variable] = 0
		corr_vars["var_%s"%variable] = 0
		root_histograms["+-+".join([variable,variable])].SetDirectory(0)
		ROOT.SetOwnership (root_histograms["+-+".join([variable,variable])], False)
	log.info( "=================================================================================")
	log.info( "Calculate correlations in sample %s and make scatter plots for %i variable pairs."%(config["request_nick"],len(root_histograms)))
	log.info( "=================================================================================")

	i = 0.
	n = 0
	zero_vals = {}
	for event in root_inst:
		calced_means = []
		w = event.__getattr__("eventWeight")
		for varxy in root_histograms.iterkeys():
			varx, vary = map(str, varxy.split("+-+"))
			x, y = map(event.__getattr__, map(str, varxy.split("+-+")))
			root_histograms[varxy].Fill(x, y, w)

			if varx not in zero_vals:
				zero_vals[varx] = 0
			if vary not in zero_vals:
				zero_vals[vary] = 0

			if varx not in calced_means:
				#log.info( "calculate mean for %s" %varx)
				corr_vars[varx] += w*(x -zero_vals[varx])
				corr_vars["var_%s"%varx] += w*(x -zero_vals[varx])**2
				calced_means.append(varx)
			if vary not in calced_means:
				#log.info( "calculate mean for %s" %vary)
				corr_vars[vary] += w*(y - zero_vals[vary])
				corr_vars["var_%s"%vary] += w*(y - zero_vals[vary])**2
				calced_means.append(vary)
			corr_vars[varxy] += w*(x -zero_vals[varx]) * (y - zero_vals[vary])

		i += w
		n += 1
		if n%1000 == 0:
			log.info( "processed: %i events"%n)

	hist_file = ROOT.TFile(os.path.join(nick_path, "Histograms.root"),"RECREATE")
	for varxy in root_histograms.iterkeys():
		root_histograms[varxy].Write()
	corr_vars["weight_sum"] = i
	corr_vars["n"] = n
	hist_file.Write()
	hist_file.Close()
	root_inf.Close()
	config["correlations"] = corr_vars
	jsonTools.JsonDict(config).save(os.path.join(nick_path,"Correlations.json"),indent=4)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Produce reduced samples and calculate correlations",
									 parents=[logger.loggingParser])
	parser.add_argument("-A", "--artus-input", default=None, help="merged folder of ArtusOutput please have a look at --reduced-input [Default=%(default)s]")
	parser.add_argument("-R", "--reduced-input", default=None, help="reduced input from Artus, already processed by this script[Default=%(default)s] --- If artus-input and reduced-input is given, reproduce missing reduceded samplesin artus-input directory")
	parser.add_argument("-O", "--overwrite-samples", action="store_true", default=False,
						help="specify if you already produced reduced files and want to overwrite them. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	#parser.add_argument("-M", "--Mvas", nargs="+",
						#default=[],
						#help="Calculate correlation within each bin of every MVA. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
						help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
						default="$CMSSW_BASE/src/plots/correlations",
						help="Output directory. [Default: %(default)s]")
	parser.add_argument("-f", "--filename",
						default="Correlation",
						help="Output filename. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=[],
						choices=["pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2", "mt"],
						help="""Exclude (default) selection cuts.
						[Default: %(default)s]""")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=["inclusive"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--higgs-masses", nargs="+", default=["125"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--add-vars", nargs="+", default=[],
						help="add variables which were not used for training MVAs to correlation calculatioin. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
						help="""Additional weight (cut) expression.
						[Default: %(default)s]""")
	parser.add_argument("-m", "--mva-variables", action="store_true", default=False,
						help="use the variables defined in MVATestMethods settings of artus run. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	plot_configs = []
	from datetime import datetime as dt

	output_dir_path = os.path.join(os.path.expandvars(args.output_dir), str(dt.utcnow().strftime("%Y_%m_%d_%H-%M"))+"_%s"%args.filename)
	if args.artus_input is None and args.reduced_input is None:
		log.error("Need input folder!")
		sys.exit()
	elif not args.artus_input is None and not args.reduced_input is None:
		root_input_dir = os.path.expandvars(args.artus_input)
		storage_name_extension = os.path.join(args.reduced_input, "storage")
		prepare_samples = True
		overwrite_samples = args.overwrite_samples
	elif args.artus_input is not None:
		root_input_dir = os.path.expandvars(args.artus_input)
		storage_name_extension = os.path.join(output_dir_path, "storage")
		prepare_samples = True
		overwrite_samples = False
	elif args.reduced_input is not None:
		root_input_dir = os.path.expandvars(args.reduced_input)
		storage_name_extension = os.path.join(args.reduced_input, "storage")
		prepare_samples = False
		overwrite_samples = False

	if output_dir_path is None:
		pass
	elif not os.path.exists(output_dir_path):
		os.makedirs(output_dir_path)
		os.makedirs(output_dir_path+"/storage")
	elif not os.path.exists(output_dir_path+"/storage"):
		os.makedirs(output_dir_path+"/storage")

	sample_settings = samples.Samples()
	#get all configs
	for channel in args.channels:
		for category in args.categories:
			if category != None:
				if(args.mssm):
					category_string = "catHttMSSM13TeV"
				if args.mva:
					category_string = "catMVAStudies"
				else:
					category_string = "catHtt13TeV"
				category_string = (category_string + "_{channel}_{category}").format(channel=channel, category=category)
			for requested_sample in args.samples:
				list_of_samples = [getattr(samples.Samples, requested_sample)]
				config = sample_settings.get_config(
						samples=list_of_samples,
						channel=channel,
						category=category_string,
						higgs_masses=args.higgs_masses,
						normalise_signal_to_one_pb=False,
						ztt_from_mc=False,
						weight=args.weight,
						exclude_cuts=args.exclude_cuts,
						stack_signal=False,
						scale_signal=1.0,
						mssm=False
						)
				config["category"] = category_string
				config["request_nick"] = requested_sample
				config["channel"] = channel
				config["prepare_samples"] = prepare_samples
				config["overwrite_samples"] = overwrite_samples
				config["storage_name_extension"] = os.path.join(storage_name_extension, channel, category, requested_sample)
				if not os.path.exists(config["storage_name_extension"]):
					os.makedirs(config["storage_name_extension"])
				config["output_filename"] = args.filename
				config["output_dir_path"] = output_dir_path
				config["root_input_dir"] = root_input_dir
				plot_configs.append(config)

	#artus =jsonTools.JsonDict(glob.glob(os.path.join(config["input_dir"], "artus_*.json")))
	#find all correlations to be calculated and plottet
	for config in plot_configs:
		parsed_parameters = []
		#if args.mva_variables:
			#unparsed_ParameterList = []
			#map(unparsed_ParameterList.__iadd__,
				#map(lambda b: b[1].split(","), map(lambda s: s.split(";"),
													#artus["Pipelines"][config["folders"][0].replace("/ntuple", "")]["MVATestMethodsInputQuantities"])))
			#for unsplitted_vars in unparsed_ParameterList:
				#if ":=" in unsplitted_vars:
					#var = unsplitted_vars.split(":=")[1]
				#else:
					#var = unsplitted_vars
				#if not var in parsed_parameters:
					#parsed_parameters.append(var)
		for additional_var in args.add_vars:
			if not additional_var in parsed_parameters:
				parsed_parameters.append(additional_var)
		config["parameters_list"] = parsed_parameters

	aTools.parallelize(calculate_partial_correlation, plot_configs, n_processes=args.n_processes)