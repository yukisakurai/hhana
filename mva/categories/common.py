from rootpy.tree import Cut
from math import pi

from .base import Category
from .. import MMC_MASS
# All basic cut definitions are here

TAU1_MEDIUM = Cut('tau1_JetBDTSigMedium==1')
TAU2_MEDIUM = Cut('tau2_JetBDTSigMedium==1')
TAU1_TIGHT = Cut('tau1_JetBDTSigTight==1')
TAU2_TIGHT = Cut('tau2_JetBDTSigTight==1')

ID_MEDIUM = TAU1_MEDIUM & TAU2_MEDIUM
ID_TIGHT = TAU1_TIGHT & TAU2_TIGHT
ID_MEDIUM_TIGHT = (TAU1_MEDIUM & TAU2_TIGHT) | (TAU1_TIGHT & TAU2_MEDIUM)
# ID cuts for control region where both taus are medium but not tight
ID_MEDIUM_NOT_TIGHT = (TAU1_MEDIUM & -TAU1_TIGHT) & (TAU2_MEDIUM & -TAU2_TIGHT)

CUTS_TAU1_0_PI0 = Cut('tau1_pi0_n==0')
CUTS_TAU2_0_PI0 = Cut('tau2_pi0_n==0')
CUTS_TAU1_N_PI0 = Cut('tau1_pi0_n>0')
CUTS_TAU2_N_PI0 = Cut('tau2_pi0_n>0')

CUTS_TAU1_PI0_LEADTRK = Cut('tau1_pt - tau1_lead_track_pt > 0')

CUTS_TAU1_NUMTRACK = Cut('tau1_numTrack==1')
CUTS_TAU2_NUMTRACK = Cut('tau2_numTrack==1')

TAU_SAME_VERTEX = Cut('tau_same_vertex')

LEAD_TAU_35 = Cut('tau1_pt > 35000')
SUBLEAD_TAU_25 = Cut('tau2_pt > 25000')

LEAD_JET_50 = Cut('jet1_pt > 50000')
SUBLEAD_JET_30 = Cut('jet2_pt > 30000')
AT_LEAST_1JET = Cut('jet1_pt > 30000')

CUTS_2J = LEAD_JET_50 & SUBLEAD_JET_30
CUTS_1J = LEAD_JET_50 & (- SUBLEAD_JET_30)
CUTS_0J = (- LEAD_JET_50)

MET = Cut('MET_et > 20000')
DR_TAUS = Cut('0.8 < dR_tau1_tau2 < 2.4')
DETA_TAUS = Cut('dEta_tau1_tau2 < 1.5')
DETA_TAUS_CR = Cut('dEta_tau1_tau2 > 1.5')
RESONANCE_PT = Cut('resonance_pt > 100000')

# use .format() to set centality value
MET_CENTRALITY = 'MET_bisecting || (dPhi_min_tau_MET < {0})'

# common weight cut for cp analysis
CP_WEIGHT = Cut('cp_even_weight!=0.0')
CP_WEIGHT = CP_WEIGHT & Cut('cp_odd_weight/cp_even_weight<50')

# common preselection cuts
PRESELECTION = (
    LEAD_TAU_35 & SUBLEAD_TAU_25
    & ID_MEDIUM_TIGHT
    & MET
    & Cut('%s > 0' % MMC_MASS)
    & DR_TAUS
    & TAU_SAME_VERTEX
    & CP_WEIGHT
    )

# VBF category cuts
CUTS_VBF = (
    CUTS_2J
    & DETA_TAUS
    )

CUTS_VBF_CR = (
    CUTS_2J
    & DETA_TAUS_CR
    )

# Boosted category cuts
CUTS_BOOSTED = (
    RESONANCE_PT
    & DETA_TAUS
    )

CUTS_BOOSTED_CR = (
    RESONANCE_PT
    & DETA_TAUS_CR
    )


class Category_Preselection_NO_MET_CENTRALITY(Category):
    name = 'preselection'
    label = '#tau_{had}#tau_{had} Preselection'
    common_cuts = PRESELECTION


class Category_Preselection(Category):
    name = 'preselection'
    label = '#tau_{had}#tau_{had} Preselection'
    common_cuts = (
        PRESELECTION
        & Cut(MET_CENTRALITY.format(pi / 4))
        )

class Category_Preselection_DEta_Control(Category_Preselection):
    is_control = True
    name = 'preselection_deta_control'


class Category_1J_Inclusive(Category_Preselection):
    name = '1j_inclusive'
    label = '#tau_{had}#tau_{had} Inclusive 1-Jet'
    common_cuts = Category_Preselection.common_cuts
    cuts = AT_LEAST_1JET
    norm_category = Category_Preselection

class Category_Preselection_1P(Category):
    name = 'presel_1p'
    label = '#tau_{had}#tau_{had} Preselection 1-Prong'
    latex = '\\textbf{Preselection 1-Prong}}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = (
        PRESELECTION
        & Cut(MET_CENTRALITY.format(pi / 4))
        & CUTS_TAU1_NUMTRACK
        & CUTS_TAU2_NUMTRACK
        )

class Category_Preselection_PiPi(Category):
    name = 'presel_pipi'
    label = '#tau_{had}#tau_{had} Preselection #pi^{#pm}-#pi^{#mp}'
    latex = '\\textbf{Preselection \pi^{\pm}-\pi^{\mp}}}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = (
        PRESELECTION
        & Cut(MET_CENTRALITY.format(pi / 4))
        & CUTS_TAU1_NUMTRACK
        & CUTS_TAU2_NUMTRACK
        & CUTS_TAU1_0_PI0
        & CUTS_TAU2_0_PI0
        )

class Category_Preselection_RhoRho(Category):
    name = 'presel_rhorho'
    label = '#tau_{had}#tau_{had} Preselection #rho-#rho'
    latex = '\\textbf{Preselection \rho-\rho}}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = (
        PRESELECTION
        & Cut(MET_CENTRALITY.format(pi / 4))
        & CUTS_TAU1_NUMTRACK
        & CUTS_TAU2_NUMTRACK
        & CUTS_TAU1_N_PI0
        & CUTS_TAU2_N_PI0
        )

class Category_Preselection_PiRho(Category):
    name = 'presel_pirho'
    label = '#tau_{had}#tau_{had} Preselection #pi^{#pm}-#rho'
    latex = '\\textbf{Preselection \pi^{\pm}-\rho}}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    common_cuts = (
        PRESELECTION
        & Cut(MET_CENTRALITY.format(pi / 4))
        & CUTS_TAU2_NUMTRACK
        & CUTS_TAU1_0_PI0
        & CUTS_TAU2_N_PI0
        )

class Category_Preselection_RhoPi(Category_Preselection):
    name = 'presel_rhopi'
    label = '#tau_{had}#tau_{had} Preselection #rho-#pi^{#pm}'
    latex = '\\textbf{Preselection \rho-\pi^{\pm}}'
    color = 'red'
    linestyle = 'dotted'
    jk_number = 6
    cuts = (
        PRESELECTION
        & Cut(MET_CENTRALITY.format(pi / 4))
        & CUTS_TAU1_NUMTRACK
        & CUTS_TAU2_NUMTRACK
        & CUTS_TAU1_N_PI0
        & CUTS_TAU2_0_PI0
        )

