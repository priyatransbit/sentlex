from __future__ import absolute_import
try:
    import sentlex.sentanalysis_taboada as sentdoc
except Exception:
    import sentanalysis_taboada as sentdoc

try:
    import sentlex.sentlex as sentlex
except Exception:
    import sentlex as sentlex

import sys
import os
import unittest

#####
#
# Unit Testing for doc sentiment analysis
#
####

#
# Data
#
TESTDOC_ADJ = 'good/JJ good/JJ good/JJ good/JJ good/JJ good/JJ good/JJ good/JJ good/JJ good/JJ'
TESTDOC_UNTAGGED = 'this cookie is good. it is very good indeed'
TESTDOC_BADADJ = 'bad_JJ Bad_JJ bAd_JJ'
TESTDOC_NEGATED = 'not/DT bad/JJ movie/NN ./. blah/NN blah/NN not/DT really/RR good/JJ either/DT ./.'
TESTDOC_CORRUPT = 'this_DT doc_NN is_VB not_DT not_DT not_DT in great/JJ shape/JJ good_JJ good_JJ good_JJ'
TESTDOC_EMPTY = ''

# T0 - Basic Class functionality


class T0_parameter_setting(unittest.TestCase):

    def runTest(self):
        # empty list
        ds = sentdoc.TaboadaDocSentiScore()
        ds.verbose = False

        ds.set_active_pos(True, False, False, False)
        ds.set_parameters(negation_shift=0.5, negation=True, negation_window=15)

        self.assertEqual((ds.a, ds.v, ds.n, ds.r), (True, False,
                                                    False, False), 'Failed set POS parameters')
        self.assertEqual((ds.negation, ds.negation_window), (True, 15), 'Failed set negation')
        self.assertEqual(ds.score_mode, ds.BACKOFF, 'Backoff parameter is not correctly set')


class T1_scoring_documents(unittest.TestCase):

    def runTest(self):
        # load lexicon
        L = sentlex.MobyLexicon()
        self.assertTrue(L.is_loaded, 'Test lexicon did not load correctly')

        # create a class that scores only adjectives
        ds = sentdoc.TaboadaDocSentiScore()
        ds.verbose = False
        ds.set_active_pos(True, False, False, False)
        ds.set_parameters(score_freq=False, negation=True, negation_shift=0.5)
        ds.set_lexicon(L)

        # separator ok?
        self.assertEqual(ds._detect_tag(TESTDOC_ADJ), '/', 'Unable to detect correct separator')

        # now score!
        (dpos, dneg) = ds.classify_document(TESTDOC_ADJ, verbose=False)
        self.assertTrue(ds.resultdata and 'doc' in ds.resultdata and 'annotated_doc' in ds.resultdata
                        and 'resultpos' in ds.resultdata and 'resultneg' in ds.resultdata, 'Did not populate resultdata after scoring doc')

        self.assertTrue(dpos > 0.0, 'Did not find positive words on positive doc')

        # again, for negative text
        (dpos, dneg) = ds.classify_document(TESTDOC_BADADJ, verbose=False)
        self.assertTrue(dneg > 0.0, 'Did not find negative words on negative doc')

        # negated text
        (dpos, dneg) = ds.classify_document(TESTDOC_NEGATED, verbose=False)

        # currupt data - should still work
        (dpos, dneg) = ds.classify_document(TESTDOC_CORRUPT, verbose=False)
        self.assertTrue(dpos > dneg, 'Did not process corrupt document correctly')


class T4_sample_classes(unittest.TestCase):

    def runTest(self):
        # load lexicon
        L = sentlex.MobyLexicon()
        self.assertTrue(L.is_loaded, 'Test lexicon did not load correctly')
        for algo in [sentdoc.AV_LightTabSentiScore(L),
                     sentdoc.AV_AggressiveTabSentiScore(L),
                     ]:
            algo.verbose = False
            (p, n) = algo.classify_document(TESTDOC_NEGATED, verbose=False)

#
# Runs unit testing if module is called directly
#
if __name__ == "__main__":

    # Run those guys
    unittest.main()