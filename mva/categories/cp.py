from math import pi
from rootpy.tree import Cut
from .common import (
    Category_Preselection,
    Category_Preselection_PiPi,
    Category_Preselection_PiRho,
    Category_Preselection_RhoPi,
    Category_Preselection_RhoRho,
    CUTS_VBF, CUTS_VBF_CR,
    CUTS_BOOSTED, CUTS_BOOSTED_CR,
    DETA_TAUS)
from .mva import (
    Category_Preselection,
    Category_VBF,
    Category_Boosted)
from .truth import CUTS_TRUE_VBF, CUTS_TRUE_BOOSTED
from .features import features_vbf, features_boosted
from .. import CACHE_DIR
import os
import pickle

# get clf
with open(os.path.join(CACHE_DIR, 'binning/binning_vbf_125_12.pickle')) as f:
              binning_vbf_125_12 = pickle.load(f)
with open(os.path.join(CACHE_DIR, 'binning/binning_boosted_125_12.pickle')) as f:
              binning_boosted_125_12 = pickle.load(f)

CUTS_VBF_SCORE = 'BDTScore_vbf_1 >= {0}'
CUTS_BOOSTED_SCORE = 'BDTScore_boosted_1 >= {0}'
CUTS_VBF_SCORE_CR = 'BDTScore_vbf_1 < {0}'
CUTS_BOOSTED_SCORE_CR = 'BDTScore_boosted_1 < {0}'
SCOREBIN = 4

##### PiPi CHANNEL #####
class Category_VBF_PiPi_DEta_Control(Category_Preselection_PiPi):
    is_control = True
    name = 'vbf_pipi_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiPi
    cuts = CUTS_VBF_CR & Cut('dEta_jets > 2.0')

class Category_VBF_PiPi_LowScore_Control(Category_Preselection_PiPi):
    is_control = True
    name = 'vbf_pipi_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiPi
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE_CR.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN]))

class Category_VBF_PiPi_SR(Category_Preselection_PiPi):
    name = 'vbf_pipi'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#pi^{#pm}#pi^{#mp} VBF BDTScore High 3'
    latex = '\\textbf{\pi^{\pm}\pi^{\mp} VBF BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = Category_Preselection_PiPi.common_cuts
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_VBF
    features = features_vbf
    # train with only VBF mode
    signal_train_modes = ['VBF']
    norm_category = Category_Preselection_PiPi
    # controls = {'deta': Category_VBF_PiPi_DEta_Control, \
    #             'lowscore': Category_VBF_PiPi_LowScore_Control}

class Category_Boosted_PiPi_DEta_Control(Category_Preselection_PiPi):
    is_control = True
    name = 'boosted_pipi_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiPi
    cuts = (
        (- Category_VBF_PiPi_SR.cuts)
        & (- Category_VBF_PiPi_LowScore_Control.cuts)
        & CUTS_BOOSTED_CR
        )

class Category_Boosted_PiPi_LowScore_Control(Category_Preselection_PiPi):
    is_control = True
    name = 'boosted_pipi_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiPi
    cuts = (
        (- Category_VBF_PiPi_SR.cuts)
        & (- Category_VBF_PiPi_LowScore_Control.cuts)
        & CUTS_BOOSTED_SCORE_CR.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        & CUTS_BOOSTED
        )

class Category_Boosted_PiPi_SR(Category_Preselection_PiPi):
    name = 'boosted_pipi'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#pi^{#pm}#pi^{#mp} Boosted BDTScore High 3'
    latex = '\\textbf{\pi^{\pm}\pi^{\mp} Boosted BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 5
    common_cuts = Category_Preselection_PiPi.common_cuts
    cuts = (
        (- Category_VBF_PiPi_SR.cuts)
        & (- Category_VBF_PiPi_LowScore_Control.cuts)
        & CUTS_BOOSTED
        & CUTS_BOOSTED_SCORE.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_BOOSTED
    features = features_boosted
    # train with only Boosted mode
    signal_train_modes = ['Boosted']
    norm_category = Category_Preselection_PiPi
    controls = {'deta': Category_Boosted_PiPi_DEta_Control,
                'lowscore': Category_Boosted_PiPi_LowScore_Control}

class Category_Rest_PiPi(Category_Preselection_PiPi):
    analysis_control = True
    name = 'rest_pipi'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#pi^{#pm}#pi^{#mp} Rest'
    latex = '\\textbf{\pi^{\pm}\pi^{\mp} Rest}'
    jk_number = 4
    common_cuts = Category_Preselection_PiPi.common_cuts
    cuts = (
        (- Category_Boosted_PiPi_SR.cuts)
        & (- Category_Boosted_PiPi_LowScore_Control.cuts)
        & (- Category_VBF_PiPi_SR.cuts)
        & (- Category_VBF_PiPi_LowScore_Control.cuts)
        & DETA_TAUS
        )
    norm_category = Category_Preselection_PiPi



##### Rho-Rho #####
class Category_VBF_RhoRho_DEta_Control(Category_Preselection_RhoRho):
    is_control = True
    name = 'vbf_rhorho_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection_RhoRho.common_cuts
    norm_category = Category_Preselection_RhoRho
    cuts = CUTS_VBF_CR & Cut('dEta_jets > 2.0')

class Category_VBF_RhoRho_LowScore_Control(Category_Preselection_RhoRho):
    is_control = True
    name = 'vbf_rhorho_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection_RhoRho.common_cuts
    norm_category = Category_Preselection_RhoRho
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE_CR.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN]))

class Category_VBF_RhoRho_SR(Category_Preselection_RhoRho):
    name = 'vbf_rhorho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#rho^{#mp} VBF BDTScore High 3'
    latex = '\\textbf{\rho^{\pm}\rho^{\mp} VBF BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = Category_Preselection_RhoRho.common_cuts
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_VBF
    features = features_vbf
    # train with only VBF mode
    signal_train_modes = ['VBF']
    norm_category = Category_Preselection_RhoRho
    controls = {'deta': Category_VBF_RhoRho_DEta_Control,
                'lowscore': Category_VBF_RhoRho_LowScore_Control}

class Category_VBF_RhoRho(Category_Preselection_RhoRho):
    name = 'vbf_rhorho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#rho^{#mp} VBF'
    latex = '\\textbf{\rho^{\pm}\rho^{\mp} VBF}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = Category_Preselection_RhoRho.common_cuts
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        )
    norm_category = Category_Preselection_RhoRho

class Category_Boosted_RhoRho_DEta_Control(Category_Preselection_RhoRho):
    is_control = True
    name = 'boosted_rhorho_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_RhoRho
    cuts = (
        (- Category_VBF_RhoRho_SR.cuts)
        & (- Category_VBF_RhoRho_LowScore_Control.cuts)
        & CUTS_BOOSTED_CR
        )

class Category_Boosted_RhoRho_LowScore_Control(Category_Preselection_RhoRho):
    is_control = True
    name = 'boosted_rhorho_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_RhoRho
    cuts = (
        (- Category_VBF_RhoRho_SR.cuts)
        & (- Category_VBF_RhoRho_LowScore_Control.cuts)
        & CUTS_BOOSTED_SCORE_CR.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        & CUTS_BOOSTED
        )

class Category_Boosted_RhoRho_SR(Category_Preselection_RhoRho):
    name = 'boosted_rhorho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#rho^{#mp} Boosted BDTScore High 3'
    latex = '\\textbf{\rho^{\pm}\rho^{\mp} Boosted BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 5
    common_cuts = Category_Preselection_RhoRho.common_cuts
    cuts = (
        (- Category_VBF_RhoRho_SR.cuts)
        & (- Category_VBF_RhoRho_LowScore_Control.cuts)
        & CUTS_BOOSTED
        & CUTS_BOOSTED_SCORE.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_BOOSTED
    features = features_boosted
    # train with only Boosted mode
    signal_train_modes = ['Boosted']
    norm_category = Category_Preselection_RhoRho
    controls = {'deta': Category_Boosted_RhoRho_DEta_Control,
                'lowscore': Category_Boosted_RhoRho_LowScore_Control}

class Category_Boosted_RhoRho(Category_Preselection_RhoRho):
    name = 'Boosted_rhorho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#rho^{#mp} Boosted'
    latex = '\\textbf{\rho^{\pm}\rho^{\mp} Boosted}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = Category_Preselection_RhoRho.common_cuts
    cuts = (
        (- Category_VBF_RhoRho_SR.cuts)
        & CUTS_BOOSTED
        & Cut('dEta_jets > 2.0')
        )
    norm_category = Category_Preselection_RhoRho

class Category_Rest_RhoRho(Category_Preselection_RhoRho):
    analysis_control = True
    name = 'rest_rhorho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#rho^{#mp} Rest'
    latex = '\\textbf{\rho^{\pm}\rho^{\mp} Rest}'
    jk_number = 4
    common_cuts = Category_Preselection_RhoRho.common_cuts
    cuts = (
        (- Category_Boosted_RhoRho_SR.cuts)
        & (- Category_Boosted_RhoRho_LowScore_Control.cuts)
        & (- Category_VBF_RhoRho_SR.cuts)
        & (- Category_VBF_RhoRho_LowScore_Control.cuts)
        & DETA_TAUS
        )
    norm_category = Category_Preselection_RhoRho


##### Pi-Rho #####
class Category_VBF_PiRho_DEta_Control(Category_Preselection_PiRho):
    is_control = True
    name = 'vbf_pirho_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiRho
    cuts = CUTS_VBF_CR & Cut('dEta_jets > 2.0')

class Category_VBF_PiRho_LowScore_Control(Category_Preselection_PiRho):
    is_control = True
    name = 'vbf_pirho_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiRho
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE_CR.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN]))

class Category_VBF_PiRho_SR(Category_Preselection_PiRho):
    name = 'vbf_pirho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#pi^{#pm}#rho^{#mp} VBF BDTScore High 3'
    latex = '\\textbf{\pi^{\pm}\rho^{\mp} VBF BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = Category_Preselection_PiRho.common_cuts
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_VBF
    features = features_vbf
    # train with only VBF mode
    signal_train_modes = ['VBF']
    norm_category = Category_Preselection_PiRho
    controls = {'deta': Category_VBF_PiRho_DEta_Control,
                'lowscore': Category_VBF_PiRho_LowScore_Control}

class Category_Boosted_PiRho_DEta_Control(Category_Preselection_PiRho):
    is_control = True
    name = 'boosted_pirho_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiRho
    cuts = (
        (- Category_VBF_PiRho_SR.cuts)
        & (- Category_VBF_PiRho_LowScore_Control.cuts)
        & CUTS_BOOSTED_CR
        )

class Category_Boosted_PiRho_LowScore_Control(Category_Preselection_PiRho):
    is_control = True
    name = 'boosted_pirho_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_PiRho
    cuts = (
        (- Category_VBF_PiRho_SR.cuts)
        & (- Category_VBF_PiRho_LowScore_Control.cuts)
        & CUTS_BOOSTED_SCORE_CR.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        & CUTS_BOOSTED
        )

class Category_Boosted_PiRho_SR(Category_Preselection_PiRho):
    name = 'boosted_pirho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#pi^{#pm}#rho^{#mp} Boosted BDTScore High 3'
    latex = '\\textbf{\pi^{\pm}\rho^{\mp} Boosted BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 5
    common_cuts = Category_Preselection_PiRho.common_cuts
    cuts = (
        (- Category_VBF_PiRho_SR.cuts)
        & (- Category_VBF_PiRho_LowScore_Control.cuts)
        & CUTS_BOOSTED
        & CUTS_BOOSTED_SCORE.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_BOOSTED
    features = features_boosted
    # train with only Boosted mode
    signal_train_modes = ['Boosted']
    norm_category = Category_Preselection_PiRho
    controls = {'deta': Category_Boosted_PiRho_DEta_Control,
                'lowscore': Category_Boosted_PiRho_LowScore_Control}

class Category_Rest_PiRho(Category_Preselection_PiRho):
    analysis_control = True
    name = 'rest_pirho'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#pi^{#pm}#rho^{#mp} Rest'
    latex = '\\textbf{\pi^{\pm}\rho^{\mp} Rest}'
    jk_number = 4
    common_cuts = Category_Preselection_PiRho.common_cuts
    cuts = (
        (- Category_Boosted_PiRho_SR.cuts)
        & (- Category_Boosted_PiRho_LowScore_Control.cuts)
        & (- Category_VBF_PiRho_SR.cuts)
        & (- Category_VBF_PiRho_LowScore_Control.cuts)
        & DETA_TAUS
        )
    norm_category = Category_Preselection_PiRho


##### Rho-Pi #####
class Category_VBF_RhoPi_DEta_Control(Category_Preselection_RhoPi):
    is_control = True
    name = 'vbf_rhopi_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_RhoPi
    cuts = CUTS_VBF_CR & Cut('dEta_jets > 2.0')

class Category_VBF_RhoPi_LowScore_Control(Category_Preselection_RhoPi):
    is_control = True
    name = 'vbf_rhopi_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_RhoPi
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE_CR.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN]))

class Category_VBF_RhoPi_SR(Category_Preselection_RhoPi):
    name = 'vbf_rhopi'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#pi^{#mp} VBF BDTScore High 3'
    latex = '\\textbf{\rho^{\pm}\pi^{\mp} VBF BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = Category_Preselection_RhoPi.common_cuts
    cuts = (
        CUTS_VBF
        & Cut('dEta_jets > 2.0')
        & CUTS_VBF_SCORE.format(binning_vbf_125_12[len(binning_vbf_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_VBF
    features = features_vbf
    # train with only VBF mode
    signal_train_modes = ['VBF']
    norm_category = Category_Preselection_RhoPi
    controls = {'deta': Category_VBF_RhoPi_DEta_Control,
                'lowscore': Category_VBF_RhoPi_LowScore_Control}

class Category_Boosted_RhoPi_DEta_Control(Category_Preselection_RhoPi):
    is_control = True
    name = 'boosted_rhopi_deta_control'
    plot_label = 'Multijet CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_RhoPi
    cuts = (
        (- Category_VBF_RhoPi_SR.cuts)
        & (- Category_VBF_RhoPi_LowScore_Control.cuts)
        & CUTS_BOOSTED_CR
        )

class Category_Boosted_RhoPi_LowScore_Control(Category_Preselection_RhoPi):
    is_control = True
    name = 'boosted_rhopi_lowscore_control'
    plot_label = 'Low Score CR'
    common_cuts = Category_Preselection.common_cuts
    norm_category = Category_Preselection_RhoPi
    cuts = (
        (- Category_VBF_RhoPi_SR.cuts)
        & (- Category_VBF_RhoPi_LowScore_Control.cuts)
        & CUTS_BOOSTED_SCORE_CR.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        & CUTS_BOOSTED
        )

class Category_Boosted_RhoPi_SR(Category_Preselection_RhoPi):
    name = 'boosted_rhopi'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#pi^{#mp} Boosted BDTScore High 3'
    latex = '\\textbf{\rho^{\pm}\pi^{\mp} Boosted BDTScore High 3}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 5
    common_cuts = Category_Preselection_RhoPi.common_cuts
    cuts = (
        (- Category_VBF_RhoPi_SR.cuts)
        & (- Category_VBF_RhoPi_LowScore_Control.cuts)
        & CUTS_BOOSTED
        & CUTS_BOOSTED_SCORE.format(binning_boosted_125_12[len(binning_boosted_125_12)-SCOREBIN])
        )
    cuts_truth = CUTS_TRUE_BOOSTED
    features = features_boosted
    # train with only Boosted mode
    signal_train_modes = ['Boosted']
    norm_category = Category_Preselection_RhoPi
    controls = {'deta': Category_Boosted_RhoPi_DEta_Control,
                'lowscore': Category_Boosted_RhoPi_LowScore_Control}

class Category_Rest_RhoPi(Category_Preselection_RhoPi):
    analysis_control = True
    name = 'rest_rhopi'
    label = '#tau_{had}^{#pm}#tau_{had}^{#mp}#rightarrow#rho^{#pm}#pi^{#mp} Rest'
    latex = '\\textbf{\rho^{\pm}\pi^{\mp} Rest}'
    jk_number = 4
    common_cuts = Category_Preselection_RhoPi.common_cuts
    cuts = (
        (- Category_Boosted_RhoPi_SR.cuts)
        & (- Category_Boosted_RhoPi_LowScore_Control.cuts)
        & (- Category_VBF_RhoPi_SR.cuts)
        & (- Category_VBF_RhoPi_LowScore_Control.cuts)
        & DETA_TAUS
        )
    norm_category = Category_Preselection_RhoPi
