# stdlib imports
from cStringIO import StringIO
from collections import OrderedDict
from multiprocessing import Process,Manager
import pickle
import os

# root/rootpy imports
import ROOT
import rootpy
from rootpy.io import root_open
from rootpy.utils.lock import lock
from rootpy import asrootpy
from rootpy.plotting import Hist
from rootpy.stats.histfactory import HistoSys, split_norm_shape
from rootpy.stats import Workspace
from rootpy.extern.tabulartext import PrettyTable
from rootpy.extern.pyparsing import (Literal, Word, Combine,
                                     Optional, delimitedList,
                                     oneOf, alphas, nums, Suppress)
# local imports
from .import log; log = log[__name__]

class highlighted_string(unicode):
    def __new__(self, content):
        if isinstance(content, basestring):
            return unicode.__new__(self, "\033[93m%s\033[0m"%str(content))
        else:
            return unicode.__new__(self, "\033[93m%0.2f\033[0m"%content)
            
    def __len__(self):
        ESC = Literal('\x1b')
        integer = Word(nums)
        escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + oneOf(list(alphas)))
        return unicode.__len__(Suppress(escapeSeq).transformString(str(self)))        

class prettyfloat(float):
    def __repr__(self):
        #         if self<0:
        #             return stripped_str("\033[93m%0.2f\033[0m"%self)
        #         elif self==0:
        #             return stripped_str("\033[91m%0.2f\033[0m" % self)
        #         else:
        return "%1.1f" % self
    def __str__(self):
        return repr(self)


            
class workspaceinterpretor:
    """
    A class to read and retrieve HSG4-type WS components
    - Parameters:
       - A HSG4 workspace
    """
    # ---------------------------------------
    def __init__(self,ws):
        obsData = ws.data('obsData')
        # --> Get the Model Config object
        mc = ws.obj("ModelConfig")
        # --> Get the simultaneous PDF
        simPdf = mc.GetPdf()
        # --> Get the dictionary of nominal hists
        self.hists = self.get_nominal_hists_array(obsData, mc, simPdf)
        # --> Start the log 
        log.info('\n')
        log.info('------- START OF THE SANITY CHECK -----------')
        log.info('------- START OF THE SANITY CHECK -----------')
        log.info('------- START OF THE SANITY CHECK -----------')
        log.info('\n')
        for cat, hlist in self.hists.items():
            self.PrintHistsContents(cat, hlist)


    
#     Integral_bkg_total = pdfmodel.createIntegral(ROOT.RooArgSet(obs))
#     Yield_bkg_total = Integral_bkg_total.getVal() * binWidth.getVal()



    # ---------------------------------------
    def get_nominal_hists_array(self, obsData, mc, simPdf):
        hists_array={}
        # --> get the list of categories index and iterate over
        catIter = simPdf.indexCat().typeIterator()
        while True:
            cat = catIter.Next()
            if not cat:
                break
            log.info("Scanning category {0}".format(cat.GetName()))
            hists_comp = []

            # --> Get the total model pdf, the observables and the POI
            pdftmp = simPdf.getPdf(cat.GetName())
            obstmp  = pdftmp.getObservables(mc.GetObservables())
            obs = obstmp.first()
            poi =  mc.GetParametersOfInterest().first()

            # --> Create the data histogram
            datatmp = obsData.reduce("{0}=={1}::{2}".format(simPdf.indexCat().GetName(),
                                                            simPdf.indexCat().GetName(),
                                                            cat.GetName()))
            datatmp.__class__=ROOT.RooAbsData # --> Ugly fix !!!
            log.info("Retrieve the data histogram")
            hists_comp.append(('data', asrootpy(datatmp.createHistogram('',obs))))

            # --> Create the total model histogram
            log.info("Retrieve the total background")
            poi.setVal(0.0)
            hists_comp.append(('background', asrootpy(pdftmp.createHistogram("cat_%s"%cat.GetName(),obs))))

            # --> Create the total model histogram
            log.info("Retrieve the total model (signal+background)")
            poi.setVal(1.0)
            hists_comp.append(('background+signal', asrootpy(pdftmp.createHistogram("model_cat_%s"%cat.GetName(),obs))))
            poi.setVal(0.0)

            comps = pdftmp.getComponents()
            compsIter = comps.createIterator()
            while True:
                comp = compsIter.Next()
                if not comp:
                    break
                # ---> loop only over the nominal histograms
                if 'nominal' not in comp.GetName():
                    continue

                log.info('Retrieve component {0}'.format(comp.GetName()))
                hists_comp.append( (comp.GetName()[:14], asrootpy(comp.createHistogram('%s_%s'%(cat.GetName(),comp.GetName()),obs))) )
            hists_array[cat.GetName()]=hists_comp
        return hists_array

    # ------------------------------------------------
    def PrintHistsContents(self, cat, hlist):
        log.info(cat)
        row_template = [cat]+list(hlist[0][1].bins_range())
        out = StringIO()
        table = PrettyTable(row_template)
        for pair in hlist:
            pretty_bin_contents=map(prettyfloat,pair[1].y())
            table.add_row([pair[0]]+pretty_bin_contents) 
        print >> out, '\n'
        print >> out, table.get_string(hrules=1)
        log.info(out.getvalue())



