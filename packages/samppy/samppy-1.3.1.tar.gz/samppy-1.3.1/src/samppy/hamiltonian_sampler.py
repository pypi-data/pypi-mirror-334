"""Implementation of Hamiltonian Markov-Chain sampling.

Main Classes:
HamiltonianSampler: standard isotropic sampler
HamiltonianBoundedSampler: subclass allowing bounds on all vector elements.
(more general constraints to a manifold are not implemented.)

A HamiltonianSampler object
can generate samples of any continuous-valued random vector, defined only by
an un-normalized LOG-LIKELIHOOD function, and the GRADIENT of that function.

The sampler can store sample vectors either as rows (VECTOR_AXIS == 1)
or as columns (VECTOR_AXIS == 0) in a 2D array.
VECTOR_AXIS is a module-global variable that can be re-assigned by user,
at any time BEFORE a sampler instance is initialized.

Assume a random vector X has probability density p(x),
but p(x) can be calculated only up to some unknown scale factor.

Define functions neg_ll and grad_neg_ll, such that
LL = neg_ll(x, *args, **kwargs) is a scalar or row vector, with
LL(n) == - log p( x[n, :] ) + constant, (if VECTOR_AXIS==1) and
G = grad_neg_ll(x, *args, **kwargs) is an array with gradient vectors, as
G[n, i] == d neg_ll(x) / d x[n, i].

(NOTE: if VECTOR_AXIS == 0, the arrays are transposed,
and function neg_ll and grad_neg_ll must account for the chosen indexing method.)

neg_ll and grad_neg_ll must accept the first argument x as a 2D array with one or many vectors.
If these functions are defined using optional additional args and/or kwargs,
the arguments saved in properties args and kwargs are used at every call to method sample().

Therefore, if those arguments have changed between calls to the sample() method,
the sampler properties args and kwargs must first be explicitly assigned with the new values.

**** Usage Example:
* 1: Define sampler properties:
def neg_ll(x, a, b):
    ......
def grad_neg_ll(x, a, b):
    ......
x0 = ....
# = array of starting sample vectors with correct shape

* 2: Construct a sampler instance:

h = HamiltonianSampler(neg_ll, grad_neg_ll, x0,
    args=(a,),
    kwargs=dict(b=0.),
    epsilon=0.1,
    n_leap_frog_steps=10)

* 3: generate an array of samples:

x = h.sample(min_steps=10, max_steps=100)  # default n_samples like x0
# OR:
x = h.sample(min_steps=10, max_steps=100, n_samples=100)  # n_samples is optional
# OR:
x = h.safe_sample(n_samples=100, min_steps=10)
# automatically checking and adjusting h.epsilon for good accept_rate

# Sample row vectors x[n, :] are now (nearly) independent samples,
# drawn from distribution with density function p(x) propto exp(-neg_ll(x, a, b)).

# x.shape[VECTOR_AXIS] == X0.shape[VECTOR_AXIS]
# x.shape[1 - VECTOR_AXIS] = n_samples

# If an argument value has changed, re-assign the sampler property:
h.args = (a_new,)
x = h.sample(n_samples=100, min_steps=1, max_steps=10)

# The sample or safe_sample method can be called repeatedly, to get new batches of samples,
# nearly independent of the previous batch.

**** Settings:

The sampler properties epsilon and n_leapfrog_steps are CRITICAL!
epsilon should be roughly equal to the smallest dimension of p(x) effective support,
and epsilon * n_leapfrog_steps should correspond to the largest dimension.

It is recommended for the caller to check accept_rate after each sample call,
and adjust epsilon in case it is too small.
Anyway, the sampler raises an AcceptanceError,
if accept_rate falls below property min_accept_rate.

If the distribution has different scales for each coordinate,
epsilon may also be given as a vector,
with different algorithm step sizes for each dimension.

All sample vectors are processed in parallel,
as different independent 'particles' in Hamiltonian motion.

Method safe_sample checks accept_rate and adjusts epsilon automatically,
BUT samples before and after a change of epsilon
are then not guaranteed to be drawn from the same desired distribution.

Samples should then only be used from the last batch
resulting from a single safe_sample call,
preferably with large min_step parameter.
This adaptive approach may be useful especially when the sampler is used iteratively,
with several subsequent calls to safe_sample,
such that the probability of epsilon adjustments decreases toward zero
in later iterations.

The sample() method uses an ad-hoc check that the Markov Chain is
reasonably close to its stationary distribution,
and performs only as many Hamiltonian leapfrog trajectories as necessary,
within the limits (min_steps, max_steps).
This usually works well but it is no absolute guarantee
that the Markov chain has reached a stationary state.

Reference:
R M Neal (2011): MCMC using Hamiltonian dynamics. Ch. 5 in
Brooks et al. (eds) Handbook of Markov Chain Monte Carlo.
Chapman and Hall / CRC Press.

*** Version History:
New in version 1.2.1:
2021-09-28, stricter ad-hoc test for Markov chain stability
    User may adjust module-global criterion level THRESHOLD_P_STABLE

New in version 1.2.0:
2019-12-02, Changed signature for sampler __init__ method:
    By default, each sampler instance creates its own separate random generator.
    The user may also assign a random generator, e.g., with pre-defined seed,
    in case repeatable behavior is needed for testing.
    The same generator instance may be assigned to several sampler objects,
    but then the generator state is not preserved if samplers are run in separate processes
    in a multiprocessing application.

New in version 1.1.0:
2019-08-23, HamiltonianSampler uses numpy.random.Generator as internal property.
    This requires Numpy v. 1.17.
    HamiltonianSampler allows initial seed for reproducible behavior.
    HamiltonianSample.safe_sample can adapt epsilon both up and down,
    until min_accept_rate < accept_rate < max_accept_rate.
    Some other minor fixes.

Version 1.0.0, 2018-09-13, first published version

2017-04-29, allow both args and kwargs for potential-energy and gradient functions
2017-05-25, use logging
2017-06-16, minor update to allow instance to be saved as property of other class
2017-11-05, HamiltonianBoundedSampler use get/set methods for bounds property
2017-12-14, allow either ROW of COLUMN storage of random vectors.
2018-09-13, fix bug init_batch in HamiltonianBoundedSampler
"""

# Future?:
# **** Use SHAKE + RATTLE method for general manifold constraint?
# Ref: B. Leimkuhler and S. Reich. Simulating Hamiltonian Dynamics.
#      Cambridge University Press, Cambridge UK, 2004.

import numpy as np
from scipy.stats import norm  # to check MCMC trend
# from scipy.stats import mannwhitneyu, ranksums  # to check MCMC trend
# from timeit import timeit  # *************

import logging
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** for TEST

# VECTOR_AXIS = 0
# random vectors are stored as COLUMNS in 2D arrays
VECTOR_AXIS = 1
# default: random vectors are stored as ROWS in 2D arrays

THRESHOLD_P_STABLE = 0.5
# = two-sided significance level for rejecting null hypothesis that Markov chain is STABLE
# = prob{abs(log-likelihood mean change) > THRESHOLD_Z}, given STABLE Markov chain
# OR prob{abs(log-likelihood variance change) > THRESHOLD_Z}
# Thus, smaller THRESHOLD_P_STABLE requires LARGER trend to conclude Markov chain is UNSTABLE

# Requirement for STABLE sample batch is that both mean and variance stay within threshold
# from one sampling step to the next.
# This check requires a batch with 3 or more sample trajectories in parallel,
# but this is no strong limitation, since usually we might run 1000 or so in parallel.

THRESHOLD_Z = - norm.ppf(THRESHOLD_P_STABLE / 2)
# = threshold on normalized test variable


# --------------------------------------- problems:
class AcceptanceError(RuntimeError):
    """Signal too few accepted trajectories
    """


class ArgumentError(RuntimeError):
    """Signal error in input arguments
    """


# -------------------------------------------------
class HamiltonianSampler:
    """Standard Hamiltonian sampler with isotropic kinetic-energy function,
    and no bounds for sample vector elements.

    The interface is similar to scipy.optimize.minimize.
    The sampler can use the same objective function and jacobian as scipy minimize.
    """

    def __init__(self, fun, jac, x,
                 args=(),
                 kwargs=None,
                 epsilon=0.1,
                 n_leapfrog_steps=10,
                 min_accept_rate=0.8,
                 max_accept_rate=0.95,
                 rng=None
                 ):
        """
        :param fun: potential energy function = negative log pdf of sampled distribution,
            except for an arbitrary additive log-normalization constant.
            Will be called as fun(x, *args, **kwargs), with
            x = 2D array of tentative sample vectors.
            Must return 1D array of potential-energy values
            fun(x).shape == (sampler.n_samples,)
                == (x.shape[1],) if VECTOR_AXIS == 0, else == (x.shape[0],)
        :param jac: gradient of fun
            Will be called as jac(x, *args, **kwargs), with
            x = 2D array of tentative sample column vectors.
            jac(x).shape == x.shape
        :param x: 2D array with starting values for all desired sample vectors.
            x[i, n] = i-th element of n-th sample vector if VECTOR_AXIS == 0, OR
            x[n, i] = i-th element of n-th sample vector if VECTOR_AXIS == 1
        :param args: (optional) tuple with positional arguments for fun and jac.
        :param kwargs: (optional) dict with keyword arguments for fun and jac. 
        :param epsilon: (optional) scalar Hamiltonian leapfrog step size
            MUST be carefully selected to match the scale of the sampled distribution.
            Should be roughly equal to the standard deviation of the distribution
            in the spatial direction where the deviation is SMALLEST.
            epsilon may also be a single vector,
            with epsilon.shape == (sampler.len_vector,) if VECTOR_AXIS == 1,
                OR epsilon.shape == (sampler.len_vector, 1) if VECTOR_AXIS == 0.
            (Neal, 2011, eqs. 4.14 - 4.16)
            May be adjusted externally, based on observed accept_rate,
            but then older samples with different epsilon should be discarded.
        :param n_leapfrog_steps: (optional) number of steps in each Hamilton trajectory
        :param min_accept_rate: (optional) limit to raise AcceptanceError in method sample
        :param max_accept_rate: (optional) upper limit used in method safe_sample
        :param rng: (optional) non-default internal random number generator.
        """
        self._fun = fun
        self._jac = jac
        self.args = tuple(args)
        if kwargs is None:
            kwargs = dict()
        self.kwargs = dict(kwargs)

        # trajectory parameters:
        self.epsilon = epsilon
        self.n_leapfrog_steps = n_leapfrog_steps

        # initial state for sampler:
        self.x = np.asarray(x)
        self.U = None  # self.potential(self.x)
        # = 1D array with U[n] = potential energy for n-th particle
        # to be updated by each call to self.sample
        # self.U_old = None  # *** only for ranksums / Mann-Whitney test in method unstable()
        self.mean_U_old = 0.
        self.var_U_old = 0.
        # updated by one_sample_step, to allow check for trend of mean_U and var_U
        self.n_accepted = 0
        # = total number of accepted trajectories so far
        self.n_trajectories = 0
        # total number of trajectories tried so far
        self.min_accept_rate = min_accept_rate
        # = limit to raise AcceptanceError
        self.max_accept_rate = max_accept_rate
        # = limit for increasing self.epsilon in safe_sample
        if rng is None:
            rng = np.random.default_rng()
        self._rng = rng
        # = random number generator,
        # CHECK: state preserved even when used in multi-processing ????? ******

    @property
    def accept_rate(self):
        return self.n_accepted / self.n_trajectories

    @property
    def n_samples(self):
        return self.x.shape[1-VECTOR_AXIS]

    @property
    def len_sample_vector(self):
        return self.x.shape[VECTOR_AXIS]

    @property
    def n_steps(self):
        return self.n_trajectories / self.n_samples

    def potential(self, x):
        """call external potential-energy function
        """
        return self._fun(x, *self.args, **self.kwargs)

    def grad_potential(self, x):
        """call external gradient function
        """
        return self._jac(x, *self.args, **self.kwargs)

    def safe_sample(self, n_samples=None,
                    min_steps=3, max_steps=100):
        """Run a series of trajectories to generate a new sample batch.
        Check that min_accept_rate < accept_rate < max_accept_rate
        and adjust epsilon until accept_rate is OK.
        :param n_samples: (optional) desired number of samples
            if None, start only from self.x
        :param min_steps: (optional) min number of Hamiltonian trajectories
        :param max_steps: (optional) max number of Hamiltonian trajectories
        :return: x = 2D array with new sample vectors, stored according to VECTOR_AXIS

        Result: saved internal state for next sample call
        """
        epsilon_start = 0. + self.epsilon  # must copy
        while self.epsilon > epsilon_start / 10.:
            try:
                self.sample(n_samples, min_steps, max_steps)
                if self.accept_rate > self.max_accept_rate:
                    self.epsilon *= 1.3  # *** ad-hoc increase
                    logger.debug(f'High accept_rate; increased epsilon = {self.epsilon}')
                return self.x  # OK result
            except AcceptanceError as e:
                logger.debug(e)
                self.epsilon *= (0.7 + 0.2 * self._rng.random())
        # Giving up: no success even with much reduced epsilon:
        msg = f'Low accept_rate= {self.accept_rate:.1%}. epsilon = {self.epsilon}'
        raise AcceptanceError(msg)  # again!

    def sample(self, n_samples=None,
               min_steps=3, max_steps=100):
        """Run a series of trajectories to generate a new sample batch.
        :param n_samples: (optional) desired number of samples
            if None, start only from self.x
        :param min_steps: (optional) min number of Hamiltonian trajectories
        :param max_steps: (optional) max number of Hamiltonian trajectories
        :return: x = 2D array with new sample vectors, stored according to VECTOR_AXIS

        Result: saved internal state for next sample call

        Method:
        The actual number of trajectories will range between min_steps and max_steps.
        New trajectories are included until the sample distribution
        seems to have reached a reasonably stationary state.
        Higher min_steps reduces the risk for undetected initial periodicity
        of Hamiltonian trajectories.
        """
        if n_samples is not None and n_samples != self.n_samples:
            self.init_batch(n_samples)
        self.U = self.potential(self.x)
        # must initialize self.U here in case self.potential or args or kwargs have changed
        self.n_accepted = 0
        self.n_trajectories = 0
        # count acceptance rate for each call of sample()
        min_steps = max(1, min_steps)
        self.one_sample_step()
        done_steps = 1
        while (done_steps < min_steps
               or (done_steps < max_steps and self.unstable())):
            self.one_sample_step()
            done_steps += 1
        if self.accept_rate < self.min_accept_rate:
            msg = f'Low accept_rate = {self.accept_rate:.1%}. epsilon = {self.epsilon}'
            raise AcceptanceError(msg)
        # ***** raise UnstableError if done_steps >= max_steps ??? ************
        return self.x

    # --------------------------------- internal functions:

    def init_batch(self, n_samples):
        """Re-sample initial state to desired batch size
        i.e., such that self.n_samples == n_samples
        :return: None
        """
        i = self._rng.integers(0, self.n_samples, size=n_samples)
        self.x = self.x[:, i] if VECTOR_AXIS == 0 else self.x[i, :]
        self.x += self.epsilon * self._rng.standard_normal(size=self.x.shape)

    def one_sample_step(self):
        """Run one Hamilton trajectory,
        and check acceptance for detailed balance
        Starting from self.x, with potential energy self.U
        :return: None

        Result: updated self.x, self.U, self.n_accepted, self.n_trajectories
        """
        self.mean_U_old = np.mean(self.U)
        self.var_U_old = np.var(self.U)
        # self.U_old = self.U.copy()  # *** temp fix only for Mann-Whitney test
        # save for later stability check
        x0 = self.x
        p0 = self.random_momentum(x0)
        h0 = self.U + self.kinetic_energy(p0)
        # = 1D array of Hamiltonians at starting points
        (x, p) = self.trajectory(x0, p0,
                                 self.random_epsilon,
                                 self.random_leapfrog_steps)
        # p = -p  # not needed because kinetic_energy is symmetric
        u1 = self.potential(x)
        h1 = u1 + self.kinetic_energy(p)
        accept = self._rng.random(size=len(h1)) < np.exp(h0 - h1)
        if VECTOR_AXIS == 0:
            self.x[:, accept] = x[:, accept]
        else:
            self.x[accept, :] = x[accept, :]
        self.U[accept] = u1[accept]
        # not_accept = np.logical_not(accept)
        # self.U = u1
        # self.U[not_accept] = self.U_old[not_accept]
        self.n_accepted += np.sum(accept)
        self.n_trajectories += self.n_samples

    def trajectory(self, x, p, dt, leap_steps):
        """Run one leapfrog trajectory with all particles in parallel in the sample batch.
        :param x: 2D array with start position vectors
        :param p: 2D array with start momentum vectors
        :param dt: scalar leapfrog step size
            OR 2D array with shape broadcast-compatible with x
        :param leap_steps: integer number of leapfrog steps
        :return: tuple (x, p); updated copy versions of x and p
        """
        # self.Q.append(x[:, 0].copy()) # for TEST display only
        p = p - 0.5 * dt * self.grad_potential(x)
        x = x + dt * p
        # do not assign in place, because we must work on a copy
        # self.Q.append(x[:, 0].copy())
        for _ in range(1, leap_steps):
            p -= dt * self.grad_potential(x)
            x += dt * p
            # self.Q.append(x[:, 0].copy())
        p -= 0.5 * dt * self.grad_potential(x)
        return x, p

    def unstable(self):
        """Ad-hoc check for stability of sampling Markov Chain.
        :return: boolean = True, if mean_U or var_U trend is large,
            with 'large' defined as > THRESHOLD_Z * estimated St.Dev
        NOTE: needs self.n_samples >> 1 for variance estimate
        """
        # **** use Mann-Whitney to test trend of self.U and self.U**2 ?
        # **** NO, the faster mean, var test most often gives same result
        if self.accept_rate < self.min_accept_rate:
            return True
        (mean_u, var_mean_u, var_u, var_var_u) = _stability_measures(self.U)
        # mean_u = mean of current self.U; var_mean_u = estimated variance of mean_u
        # var_u = variance of current self.U; var_var_u = estimated variance of var_u
        d_mean = np.abs(self.mean_U_old - mean_u) / self.accept_rate
        # scaled up to compensate for zero diff for rejected trajectories
        std_d_mean = np.sqrt(var_mean_u * 2)
        # = expected std.dev of d_mean, estimated from current batch of samples
        unstable_mean = d_mean > THRESHOLD_Z * std_d_mean
        if var_var_u is None:
            logger.warning('Batch must have at least 3 samples to check stable variance')
            unstable_var = False  # cannot test var_u, assume stable
        else:
            d_var = np.abs(var_u - self.var_U_old) / self.accept_rate
            # scaled up to compensate for zero diff for rejected trajectories
            std_d_var = np.sqrt(var_var_u * 2)
            unstable_var = d_var > THRESHOLD_Z * std_d_var
        # # ---------- tests 2021-09-29:
        # def test_time_mean_var():
        #     _stability_measures(self.U)
        # print(f'mean_var test time = {timeit(test_time_mean_var, number=1000)} ms per test')
        # # this faster test took about 0.1 ms per sample
        # def test_time_mw():
        #     mannwhitneyu(self.U, self.U_old)
        #     mannwhitneyu((self.U - np.mean(self.U)) ** 2,
        #                  (self.U_old - self.mean_U_old) ** 2)
        # print(f'MW time = {timeit(test_time_mw, number=1000)} ms per test')
        # # mannwhitneyu takes only about 1.3 ms, perhaps OK to check it this way ?
        # # although about 15 times slower than the simple mean_u, var_u test
        # def test_time_ranksum():
        #     ranksums(self.U, self.U_old)
        #     ranksums((self.U - np.mean(self.U)) ** 2,
        #                  (self.U_old - self.mean_U_old) ** 2)
        # print(f'ranksums time = {timeit(test_time_ranksum, number=1000)} ms per test')
        # # ranksums test takes only about 1.0 ms per test
        # # but still about 10 times slower than the simple mean_u, var_u test
        # # ----------------------------------------------
        # (_, mean_p) = mannwhitneyu(self.U, self.U_old,
        #                            alternative='two-sided')
        # (_, mean_p) = ranksums(self.U, self.U_old)
        # mean_p = prob{change mean_U} given null hypothesis STABLE
        # (_, var_p) = mannwhitneyu((self.U - np.mean(self.U))**2,
        #                           (self.U_old - self.mean_U_old)**2,
        #                           alternative='two-sided')
        # (_, var_p) = ranksums((self.U - np.mean(self.U))**2,
        #                       (self.U_old - self.mean_U_old)**2)
        # var_p = prob{change var_U} given null hypothesis STABLE
        # print(f'unstable?: mean, var test = ({unstable_mean} or {unstable_var}). '
        #       # + f'MW = ({mean_p < THRESHOLD_P_STABLE} or {var_p < THRESHOLD_P_STABLE}). '
        #       # + f'M-Whitney mean_p = {mean_p:.4}. var_p = {var_p:.4}'
        #       )
        # return mean_p < THRESHOLD_P_STABLE or var_p < THRESHOLD_P_STABLE
        return unstable_mean or unstable_var

    @property
    def random_epsilon(self):
        """Slightly random variations on epsilon.
        Ref: Neal (2011) recommended +- 20% randomization
        :return: scalar epsilon
        """
        r_range = 0.2
        # = random range of relative epsilon variations
        r = self._rng.random() * 2 * r_range - r_range
        return self.epsilon * (1 + r)

    @property
    def random_leapfrog_steps(self):
        """ Slightly random variations around nominal self.n_leapfrog_steps
        Ref: Neal (2011)
        :return: scalar integer
        """
        r_range = 0.2
        # = random range of relative variations
        r = self._rng.random() * 2 * r_range - r_range
        return int(self.n_leapfrog_steps * (1 + r))

    def random_momentum(self, x):
        """Generate random momentum vectors corresponding to x
        Returns: p = 2D array with standard Gaussian momentum vectors
            p.shape == self.x.shape
        """
        return self._rng.standard_normal(size=x.shape)

    @staticmethod
    def kinetic_energy(p):
        """Kinetic energy for momentum p
        Input: p = 2D array with momentum column vectors
        Returns: Kinetic = 1D array with kinetic energy
            Kinetic[n] = kinetic energy of n-th sample of p
        """
        return np.sum(p**2, axis=VECTOR_AXIS) / 2


# -----------------------------------------------------------------------
class HamiltonianBoundedSampler(HamiltonianSampler):
    """Hamiltonian sampler with isotropic momentum function,
    with lower and/or upper coordinate bounds for each element of sample vectors
    """
    def __init__(self, fun, jac, x,
                 bounds=None,
                 **kwargs):
        """
        :param fun: potential energy function = negative log pdf
        :param jac: gradient of fun
        :param x: 2D array with starting values for all desired sample vectors.
            x[i, n] = i-th element of n-th sample vector if VECTOR_AXIS=0, OR
            x[n, i] = i-th element of n-th sample vector if VECTOR_AXIS=1
        :param bounds: sequence of pairs (x_min, x_max)
            with low and high bounds for each sample vector element.
            Either x_min or x_max may be None.
            x_min may be -inf; x_max may be +inf
            len(bounds) == sample vector length == self.len_sample_vector
        :param kwargs: any other keyword arguments for superclass constructor.
        """
        super().__init__(fun, jac, x, **kwargs)
        if bounds is None:
            bounds = [(-np.inf, np.inf) for _ in range(x.shape[VECTOR_AXIS])]
        if len(bounds) != x.shape[VECTOR_AXIS]:
            raise ArgumentError('bounds must match vector length')
        # *** or allow single bound pair?
        self._bounds = [self.check_bound(*b) for b in bounds]
        x_elements = self.x if VECTOR_AXIS == 0 else self.x.T
        for (x_i, (l_i, h_i)) in zip(x_elements, self.bounds):
            np.maximum(x_i, l_i, out=x_i)
            np.minimum(x_i, h_i, out=x_i)
            # just clip data to bounds, storing results in place

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, b):
        """Check and adjust, in case user explicitly assigns new bounds.
        :param b: list of tuples (l_i, h_i) with (low, high) bounds
            l_i == None is recoded as l_i = -inf
            h_i == None is recoded as h_i = +inf
        """
        if len(bounds) != self.x.shape[VECTOR_AXIS]:
            raise ArgumentError('bounds must match vector length')
        self._bounds = [self.check_bound(*b_i) for b_i in b]

    def init_batch(self, n_samples):
        """Re-sample initial state to desired batch size of particles
        i.e., such that self.n_samples == n_samples
        and make sure all generated samples are within bounds.
        Arne Leijon, 2018-09-13
        """
        super().init_batch(n_samples)
        (self.x, _) = self.keep_within_bounds(self.x, np.zeros_like(self.x))

    def trajectory(self, x, p, dt, leap_steps):
        """Run one leapfrog trajectory for each particle,
        :param x: 2D array with start position vectors
        :param p: 2D array wth start momentum vectors
        :param dt: scalar leapfrog step size
            OR 2D array with shape broadcast-compatible with x
        :param leap_steps: integer number of leapfrog steps
        :return: tuple (x, p); updated copy versions of x and p
        """
        p = p - 0.5 * dt * self.grad_potential(x)
        x = x + dt * p
        # do not assign in place, because we must make copy
        (x, p) = self.keep_within_bounds(x, p)
        for _ in range(1, leap_steps):
            p -= dt * self.grad_potential(x)
            x += dt * p
            (x, p) = self.keep_within_bounds(x, p)
        p -= 0.5 * dt * self.grad_potential(x)
        return x, p

    def keep_within_bounds(self, x, p):
        """Reflect particle trajectories at coordinate bounds,
        to make sure that all low_i <= x_i <= high_i.
        :param x: 2D array with start position vectors
        :param p: 2D array wth start momentum vectors
        :return: tuple (x, p); updated copy versions of x and p

        Ref: Neal (2011) Fig 8
        """
        (x_work, p_work) = (x.T, p.T) if VECTOR_AXIS == 1 else (x, p)
        for (x_i, p_i, (l_i, h_i)) in zip(x_work, p_work, self.bounds):
            outside_h = x_i > h_i
            outside_l = x_i < l_i
            while np.any(outside_l) or np.any(outside_h):
                x_i[outside_h] -= 2*(x_i[outside_h] - h_i)
                p_i[outside_h] *= -1
                x_i[outside_l] -= 2*(x_i[outside_l] - l_i)
                p_i[outside_l] *= -1
                outside_h = x_i > h_i
                outside_l = x_i < l_i
        return (x_work.T, p_work.T) if VECTOR_AXIS == 1 else (x_work, p_work)

    @staticmethod
    def check_bound(low, high):
        """Ensure that bounds (low, high) are ordered as b.low < b.high,
        (otherwise the bound reflection algorithm will never terminate).
        Any bound == None is replaced by -inf or +inf
        :param low: scalar real
        :param high: scalar real
        :return: tuple (low, high) with checked bounds in correct order
        """
        if low is None:
            low = -np.inf
        if high is None:
            high = np.inf
        if low > high:
            (low, high) = (high, low)
        if np.isclose(low, high):  # low == high:
            raise ArgumentError('All (low, high) bounds must be separated')
        return low, high


# ---------------------------------------------- module help function
def _stability_measures(u):
    """Estimate sample variance and variance of the variance estimate
    :param u: 1D array of neg log-likelihood samples
    :return: tuple (mean_u, var_mean_u, var_u, var_var_u),
        mean_u = unbiased sample mean estimate
        var_mean_u = unbiased estimated variance of mean_u
        var_u = unbiased sample variance estimate
        var_var_u = unbiased estimated variance of var_u
    """
    n = len(u)
    mean_u = np.mean(u)
    if n <= 1:
        var_u = None
        var_mean_u = None
    else:
        var_u = np.var(u)
        # = sum_n{(u_n - mean_u)**2 / (n-1)} = unbiased var estimate
        var_mean_u = var_u / n
    if n < 3:
        var_var_u = None
    else:
        mom_4 = np.mean((u - np.mean(u))**4)
        var_var_u = (mom_4 - var_u**2 * (n-3) / (n-1)) / n  # **** CHECK !
        # https://math.stackexchange.com/questions/72975/variance-of-sample-variance
    return mean_u, var_mean_u, var_u, var_var_u


# ------------------------------------------------------ TEST:
if __name__ == '__main__':
    # from scipy.stats import norm

    VECTOR_AXIS = 1
    import matplotlib.pyplot as plt

    # print('*** Testing scipy mannwhitneyu and ranksums')
    # x = norm.rvs(size=1000)
    # y = x + 0.1 + 0.000001 * norm.rvs(size=1000)
    # (u, p) = mannwhitneyu(x, y, alternative='two-sided')
    # print(f'mannwhitney p = {p}. NOTE: default alternative changed after scipy v.1.5.4!')
    # (u, p) = ranksums(x, y)
    # print(f'ranksums p = {p}. NOTE: argument alternative NOT in scipy v.1.5.4!')

    print(f'*** Testing HamiltonianSampler with 2-dim Gaussian; VECTOR_AXIS={VECTOR_AXIS} ***\n')
    print('NOTE: some settings can cause periodic trajectories!')
    print('turn off epsilon and leapfrog randomization to see this problem more often')
    print('TEST: sigma = np.array([10., 3.]); epsilon=3.; n_leapfrog_steps=9, or 12, or ...\n')
    # fixed single starting point, no epsilon randomization
    sigma = np.array([10., 3.])
    hamilton_scale = np.min(sigma)
    hamilton_steps = max(10, int(np.max(sigma) / hamilton_scale))
    # prec = 1. / (sigma**2).reshape((-1,1))

    # = column principal vectors:
    P = np.array([[1., 1.],
                  [1., -1.]]) / np.sqrt(2.)
    # P = np.eye(2)
    # = principal-vector matrix

    def neg_ll(x, sigma):
        if VECTOR_AXIS == 0:
            z = np.dot(P.T, x) / sigma.reshape((-1, 1))
        else:
            z = np.dot(P.T, x.T) / sigma.reshape((-1, 1))
        # projection on Principal axes
        return np.sum(z**2, axis=0) / 2.

    def grad_neg_ll(x, sigma):
        if VECTOR_AXIS == 0:
            z = np.dot(P.T, x)
            return np.dot(P / sigma**2, z)
        else:
            z = np.dot(x, P)
            return np.dot(z / sigma**2, P.T)

    def sample(n_samples):
        x = np.dot(sigma * P, norm.rvs(size=(2, n_samples)))
        if VECTOR_AXIS == 0:
            return x
        else:
            return x.T

    def plot_samples(ax, x):
        b = 2 * np.max(sigma)
        if VECTOR_AXIS == 0:
            ax.plot(x[0, :], x[1, :], '.b')
        else:
            ax.plot(x[:, 0], x[:, 1], '.b')
        ax.set_xlim([-b, b])
        ax.set_ylim([-b, b])

    def plot_sample_state(ax, h):
        """plot state of sampler h
        """
        plot_samples(ax, h.x)

    scipy_x = sample(1000)
    print('scipy_x.mean = ', np.mean(scipy_x, axis=1-VECTOR_AXIS))
    print('scipy_x.std = ', np.std(scipy_x, axis=1-VECTOR_AXIS))
    print('scipy_x mean LL = ', - np.mean(neg_ll(scipy_x, sigma)))

    # --------------------------------------- check gradient:
    # from scipy.optimize import check_grad, approx_fprime
    #
    # def test(x):
    #     if VECTOR_AXIS == 0:
    #         return neg_ll(x.reshape((-1, 1)), sigma)[0]
    #     else:
    #         return neg_ll(x.reshape((1, -1)), sigma)[0]
    #
    # def grad_test(x):
    #     if VECTOR_AXIS == 0:
    #         xt = x.reshape((-1,1))
    #         return grad_neg_ll(xt, sigma).reshape((-1,))
    #     else:
    #         return grad_neg_ll(x, sigma)
    #
    # test_x = scipy_x[:,0]
    # test_x = np.array([-5., +5.])
    # err = check_grad(test, grad_test, test_x)
    # print('\nGradient test:')
    # print('test_x =', test_x)
    # print('test =', test(test_x))
    # print('grad_test =', grad_test(test_x))
    # print('approx_grad = ', approx_fprime(test_x, test, epsilon=1e-6))
    # print('check_grad err = ', err)
    # print()
    # # --------------------------------------------------

    x0 = np.zeros((2, 2000))
    if VECTOR_AXIS == 1:
        x0 = x0.T
    h = HamiltonianSampler(neg_ll, grad_neg_ll, x0,
                           kwargs=dict(sigma=sigma),
                           min_accept_rate=0.9,
                           epsilon=hamilton_scale,
                           n_leapfrog_steps=9)  # 3, 6, 9,  12 for high risk of periodicity
    ham_x = h.sample(min_steps=1, n_samples=1000)
    # print('h.trajectory:', np.array(h.Q))
    print()
    print('ham_x.mean = ', np.mean(ham_x, axis=1-VECTOR_AXIS))
    print('ham_x.std = ', np.std(ham_x, axis=1-VECTOR_AXIS))
    print('ham_x mean LL = ', - np.mean(neg_ll(ham_x, sigma)))
    print('ham.accept_rate= ', h.accept_rate)
    print('ham.n_steps= ', h.n_steps)

    f1, ax1 = plt.subplots()
    plot_samples(ax1, scipy_x)
    ax1.set_title('Scipy Gaussian Samples')
    f1.show()

    f2, ax2 = plt.subplots()
    plot_sample_state(ax2, h)
    ax2.set_title('Hamiltonian Samples')

    plt.show()

    # ------------------------------------------------------------------------
    print('\n*** Testing HamiltonianSampler reproducible with seed ***')
    h = HamiltonianSampler(neg_ll, grad_neg_ll, x0,
                           kwargs=dict(sigma=sigma),
                           min_accept_rate=0.9,
                           epsilon=hamilton_scale,
                           n_leapfrog_steps=12,
                           rng=np.random.default_rng(seed=12345))
    ham_x = h.sample(min_steps=1, n_samples=5)
    print('ham_x = ', ham_x)
    h = HamiltonianSampler(neg_ll, grad_neg_ll, x0,
                           kwargs=dict(sigma=sigma),
                           min_accept_rate=0.9,
                           epsilon=hamilton_scale,
                           n_leapfrog_steps=12,
                           rng=np.random.default_rng(seed=12345))
    ham_x = h.sample(min_steps=1, n_samples=5)
    print('ham_x should be same = ', ham_x)

    # ------------------------------------------------------------------------
    print('\n*** Testing HamiltonianBoundedSampler ***')
    bounds = [(-3., +5.), (None, 10.)]
    x0 = np.zeros((2, 1000))  # + np.array([2., -2.]).reshape((-1,1))
    if VECTOR_AXIS == 1:
        x0 = x0.T
    h = HamiltonianBoundedSampler(neg_ll, grad_neg_ll, x0,
                                  args=(sigma,),
                                  bounds=bounds,
                                  min_accept_rate=0.7,
                                  epsilon=hamilton_scale,
                                  n_leapfrog_steps=12)  # hamilton_steps)
    ham_x = h.sample(min_steps=1)
    # print('h.trajectory:', np.array(h.Q))
    print()
    print('ham_x.mean = ', np.mean(ham_x, axis=1-VECTOR_AXIS))
    print('ham_x.std = ', np.std(ham_x, axis=1-VECTOR_AXIS))
    print('ham_x mean LL = ', - np.mean(neg_ll(ham_x, sigma)))
    print('ham.accept_rate= ', h.accept_rate)
    print('ham.n_steps= ', h.n_steps)

    fb1, ax1 = plt.subplots()
    plot_samples(ax1, scipy_x)
    ax1.set_title('Scipy Unbounded Gaussian Samples')
    fb1.show()

    fb2, ax2 = plt.subplots()
    plot_sample_state(ax2, h)
    ax2.set_title('Hamiltonian Bounded Samples')
    plt.show()
