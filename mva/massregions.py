# rootpy imports
from rootpy.tree import Cut

# local imports
from . import MMC_MASS
from . import log; log = log[__name__]


DEFAULT_LOW_MASS = 100
DEFAULT_HIGH_MASS = 150


class MassRegions(object):

    def __init__(self,
            low=DEFAULT_LOW_MASS,
            high=DEFAULT_HIGH_MASS,
            high_sideband_in_control=True,
            mass_window_signal_region=False,
            train_signal_region=False,
            low_cutoff=None):
        # control region is low and high mass sidebands
        self.__control_region = Cut('%s < %d' % (MMC_MASS, low))
        if low_cutoff is not None:
            self.__control_region &= Cut('%s > %d' % (MMC_MASS, low_cutoff))
        if high_sideband_in_control:
            assert high > low
            self.__control_region |= Cut('%s > %d' % (MMC_MASS, high))

        if mass_window_signal_region:
            # signal region is the negation of the control region
            self.__signal_region = -self.__control_region
        else:
            # signal region is not restricted
            self.__signal_region = Cut()

        if train_signal_region:
            # train on only the signal region
            self.__train_region = self.__signal_region
        else:
            # train on everything
            self.__train_region = Cut()

        log.info("control region: %s" % self.__control_region)
        log.info("signal region: %s" % self.__signal_region)
        log.info("train region: %s" % self.__train_region)

    @property
    def control_region(self):
        # make a copy
        return Cut(self.__control_region)

    @property
    def signal_region(self):
        # make a copy
        return Cut(self.__signal_region)

    @property
    def train_region(self):
        # make a copy
        return Cut(self.__train_region)
