from mva.analysis import Analysis
from mva.samples import Higgs, QCD
from mva.categories import Category_VBF, Category_Boosted, Category_Preselection
from mva.defaults import TARGET_REGION
from rootpy.plotting import Hist
from root_numpy import fill_hist
from numpy.testing import assert_almost_equal
from numpy.testing import assert_array_equal
from nose.tools import assert_equal


def check_partition(sample, category, region):
    rec = sample.merged_records(
        category, region)
    left, right = sample.partitioned_records(category, region)
    assert_equal(left.shape[0] + right.shape[0], rec.shape[0])


def check_events(analysis, sample, category, region):
    clf = analysis.get_clf(category, mass=125, load=True)
    scores, weights = sample.scores(
        clf, category, region,
        systematics=False)['NOMINAL']
    rec = sample.merged_records(
        category, region)
    sample_events = sample.events(category, region)[1].value
    hist = Hist(5, scores.min() - 1, scores.max() + 1)
    fill_hist(hist, scores, weights)
    clf_events = hist.integral()

    # test events consistency
    assert_equal(weights.shape[0], rec['weight'].shape[0])
    assert_array_equal(weights, rec['weight'])
    assert_almost_equal(clf_events, weights.sum(), 1)
    assert_almost_equal(sample_events, rec['weight'].sum(), 1)
    assert_almost_equal(sample_events, clf_events, 1)

    # test draw_array
    hist = Hist(1, -1000, 1000)
    sample.draw_array({'tau1_charge': hist}, category, region)
    assert_almost_equal(hist.integral(), sample_events, 1)

    # test scaling
    orig_scale = sample.scale
    sample.scale *= 2.
    scores, weights = sample.scores(
        clf, category, region,
        systematics=False)['NOMINAL']
    hist.Reset()
    fill_hist(hist, scores, weights)
    scale_clf_events = hist.integral()
    assert_almost_equal(scale_clf_events, weights.sum(), 1)
    assert_almost_equal(scale_clf_events, 2. * clf_events, 1)
    scale_sample_events = sample.events(category, region)[1].value
    assert_almost_equal(scale_sample_events, 2. * sample_events, 1)
    sample.scale = orig_scale


def test_samples():
    for year in 2011, 2012:
        analysis = Analysis(year)
        analysis.normalize(Category_Preselection)
        for sample in analysis.backgrounds + [analysis.higgs_125]:
            for category in (Category_VBF, Category_Boosted):
                for region in ('OS_ISOL', 'OS', 'nOS_ISOL'):
                    if not isinstance(sample, QCD):
                        yield check_partition, sample, category, region
                    yield check_events, analysis, sample, category, region


if __name__ == "__main__":
    import nose
    nose.runmodule()
