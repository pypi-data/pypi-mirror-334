"""This package includes modules for standard Hamiltonian MCMC sampling
and for some analyses of the posterior distribution
defined by an array of (possibly Hamiltonian-generated) samples.

*** Version history:
* Version 1.3.1:
2025-03-09, Minor update to module credibility_pd.py for compatibility with Pandas v. 2.1 and future

* Version 1.3.0:
2023-04-16, new module credibility_pd.py, for Pandas input data format

* Version 1.2.2:
2021-11-03, removed logger.setlevel(DEBUG), to inherit __main__ logger level

* Version 1.2.1:
2021-09-12, cleanup doc and some bugfix in module credibility
2021-09-29, stricter test for Markov chain stability in module hamiltonian_sampler

* Version 1.2.0:
2019-12-01, HamiltonianSampler.__init__ has slightly changed signature,
    using module-global random-number generator by default.

* Version 1.1.0:
2019-08-24, HamiltonianSampler objects have separate random-number generator,
    Require Generator class from numpy.random v 1.17

* Version 1.0.5, 2018-09-13, minor cleanup, fixes

* Version 1.0.3, 2018-08-15, first published version
"""
__name__ = 'samppy'
__version__ = '1.3.1'
__all__ = ['hamiltonian_sampler', 'credibility', 'credibility_pd', 'sample_entropy']

