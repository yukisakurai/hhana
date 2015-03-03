#!/usr/bin/env python
"""
This is the main driver script for the analysis
"""
from mva.cmd import get_parser

args = get_parser(actions=False).parse_args()
year = args.year

# stdlib imports
import math

# rootpy imports
from rootpy.io import root_open
from rootpy.plotting import Canvas, Hist, Legend

# local imports
from mva import log, variables, MMC_MASS, plot_dir
from mva.plotting import draw_channel_array, draw_channel, hist_scores, draw_ratio
from mva.classify import histogram_scores
from mva.systematics import get_systematics, parse_systematics
from mva.categories import CATEGORIES
from mva.massregions import MassRegions
from mva.analysis import get_analysis
from mva.defaults import TARGET_REGION

from statstools.histfactory import uniform_channel
from statstools.utils import efficiency_cut


SYSTEMATICS = get_systematics(year)
args.systematics_components = parse_systematics(args.systematics_components)
systematics = SYSTEMATICS if args.systematics else None

mass_regions = MassRegions(
    low=args.low_mass_cut,
    high=args.high_mass_cut,
    high_sideband_in_control=args.high_sideband_in_control,
    mass_window_signal_region=False, #args.no_mmc,
    # not enough events to only train in signal region
    train_signal_region=False)

control_region = mass_regions.control_region
signal_region = mass_regions.signal_region
#signal_region = control_region # for creating control workspaces
train_region = mass_regions.train_region

categories = CATEGORIES[args.categories]
category_names = args.category_names

analysis = get_analysis(args)
target_region = analysis.target_region
region = target_region
output_suffix = analysis.get_suffix()

cat_defs = [args.categories]
if args.categories != 'presel':
    cat_defs.append(args.controls)

UNBLIND = {
    2012: {
        'vbf': 3,
        'boosted': 1},
    2011: {
        'vbf': 2,
        'boosted': 2}
}


def plot_bdt(category, workspace_binning=True):
    # create BDT validation plots
    clf = analysis.get_clf(category, load=True, mass=125, transform=True)
    suffix = clf.output_suffix

    if workspace_binning:
        bins = clf.binning(analysis.year)
        suffix += '_workspace_binning'
        unblind_bins = UNBLIND[year][category.name]
    else:
        bins = 10
        unblind_bins = 0.5
    if args.unblind:
        suffix += '_unblind'

    signal_scale=20.
    region = TARGET_REGION


