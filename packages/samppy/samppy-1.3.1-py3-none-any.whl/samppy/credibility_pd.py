"""This module calculates jointly credible differences
between elements of random vectors, represented by
sample vectors drawn from a multivariate distribution.

Input and output data are Pandas DataFrame or Series objects.
Tested with Pandas v. 2.2.3

Method reference:
A. Leijon, G. E. Henter, and M. Dahlquist.
Bayesian analysis of phoneme confusion matrices.
IEEE Transactions on Audio, Speech, and Language Processing 24(3):469–482, 2016.

*** Version History:
* Version 1.3.1:
2025-03-09, minor changes in cred_diff, to avoid Pandas.FutureWarning

* Version 1.3.0:
2023-04-16, New module adapted for Pandas data format.
            Otherwise, same functionality as original module credibility.py
"""
import numpy as np
from itertools import combinations, product
import pandas as pd
import logging

logger = logging.getLogger(__name__)

RNG = np.random.default_rng()


# ----------------------------------------------------------
def cred_diff(x, diff_axis, case_axis=(),
              p_lim=0.6, threshold=0.):
    """Find a sequence of pairs of jointly credible differences between
    random-vector elements in one or more case conditions.
    Distributions are represented by an array of RELATED SAMPLES.

    Elements are compared between pairs of categories in diff_axis.
    Each vector sample may include different cases,
    represented by one or more dimensions in the case_axis.
    Any row index axis not included in case_axis is handled as independent sample elements.

    :param x: a pd.Series or pd.DataFrame instance
        NOTE: Samples are assumed JOINTLY sampled for all vector elements in all case variants.
    :param diff_axis: name or tuple of names of index axes for x values to compare.
    :param case_axis: (optional) name or tuple of names for index axes
        with case categories for which x values in diff_axis are compared separately.
    :param p_lim: (optional) scalar minimum joint credibility for difference to be included
    :param threshold: (optional) scalar minimum absolute difference between elements to be considered.
    :return: list of tuples (((i, j), *c), p),
        meaning that
        prob{ X_i - X_j > threshold in case==*c } AND similar for all preceding tuples } = p,
        where (i, j) are column/index label(s) in x,
        c includes zero, one, or more labels in given case index or indices.
        The approximate probability is estimated from the relative frequency of samples,
        using a Jeffreys prior pseudo-count = 0.5.

    As each successive row includes one new pair in the jointly credible set,
    the joint probability for the sequence of pairs DECREASES with each new pair.
    Therefore, the result rows are automatically ordered
    with strictly non-increasing values of p.

    Arne Leijon, 2023-04-16
    """
    def check_reverse():
        """reverse df pairs where opposite comparison is more frequent
        """
        def reverse_label(col):
            return ((col[0][1], col[0][0]), *col[1:])

        rev = [c for c in df.columns.values
               if (df[c] < -threshold).sum(axis=0) > (df[c] > threshold).sum(axis=0) ]
        df[rev] = - df[rev]   # -> np.VisibleDeprecationWarning, Pandas 1.5.1 bugg? should work ?
        # works OK in pandas 2.0
        df.rename(columns={c: reverse_label(c) for c in rev}, inplace=True, errors='raise')

    # ------------------------------------------------- check args
    if type(case_axis) is not tuple:
        case_axis = (case_axis,)
    if type(diff_axis) is not tuple:
        diff_axis = (diff_axis,)
    if type(x) is pd.DataFrame:
        must_stack = [c for c in x.columns.names if c not in diff_axis]
        if len(must_stack) > 0:
            x = x.stack(must_stack, future_stack=True)
    must_unstack =  [c for c in x.index.names if c in diff_axis]
    x = x.unstack(must_unstack)
    sample_axis = [i for (i, i_name) in enumerate(x.index.names)
                   if i_name not in case_axis]
    # any index levels NOT named in vector_axis are considered as part of sample index
    if len(sample_axis) == 0:
        raise RuntimeError('No sample axis in input data')
    if len(sample_axis) > 1:
        logger.warning(f'Sample index includes {len(sample_axis)} levels: '
                       + str([x.index.names[i] for i in sample_axis]))
    # ---------------------------------------------------------
    diff_cols = list(combinations(x.columns, 2))
    df = pd.DataFrame({(i, j): x[i] - x[j]
                         for (i,j) in diff_cols},
                        columns=diff_cols)
    if len(case_axis) > 0:
        df = df.unstack(list(case_axis), fill_value=0.)
        df.columns = pd.Index([ci for ci in df.columns], tupleize_cols=False)  # flat Index, NOT MultiIndex
    else:
        df.columns = pd.Index([(ci, ()) for ci in df.columns], tupleize_cols=False)  # flat Index, NOT MultiIndex
    # ONE column for each desired comparison: (*diff, *case)
    # each row is handled as an independent i.i.d. sample from the underlying distribution
    n_samples = df.shape[0]
    if n_samples < 200:
        logger.warning(f'Only {n_samples} samples: Too few -> unreliable results.')
    check_reverse()
    res = [] # space for result

    # ---------------------------------- Main loop:
    p_diff = ((df > threshold).sum(axis=0) + 0.5) / (n_samples + 1)  # 0.5 pseudo-count = Jeffreys prior
    # = pd.Series with potential credibility values, p_diff.index = df.columns
    while np.any(p_diff > p_lim):
        ijc_max = p_diff.idxmax()
        # = diff column head with maximum prob of difference
        res.append((ijc_max, p_diff.max()))
        keep_rows = df[ijc_max] > threshold
        df.drop(columns=ijc_max, inplace=True)
        # keeping only columns with comparison pairs not yet included in res
        df = df.loc[keep_rows]  # works OK in pandas 2.0, NOT in v 1.5.1
        # keep only samples (rows) where accepted condition was satisfied
        check_reverse()  # again
        p_diff = ((df > threshold).sum(axis=0) + 0.5) / (n_samples + 1)
    return res


# ---------------------------------------------------------------
def cred_group_diff(x_groups, group_axis, case_axis=None,
                    p_lim=0.6, threshold=0., rng=RNG):
    """Find pairs of jointly credible differences between
    groups with independent scalar or vector-valued random variables,
    represented by UNRELATED sets of samples for each group.

    :param x_groups: dict with elements (group_cat: group_data)
        where group_cat is a label or tuple of labels identifying the group,
        and group_data is a pd.Series or pd.DataFrame instance,
        containing samples from random vectors
        with related samples for different case categories.
        group_data must have same structure for all groups.
        Sample array elements are treated as INDEPENDENT across groups,
        but assumed jointly sampled across case categories within each group.
        Thus, the order of samples is UNRELATED across groups,
        but samples are assumed jointly RELATED across case categories within each group.
    :param group_axis: name or tuple of names for categories in x_groups.keys()
        len(group_axis) must be same as length of all x_groups.keys()
    :param case_axis: (optional) secondary name or names for index of cases within which differences are considered
    :param p_lim: (optional) scalar minimum joint credibility for difference to be included
    :param threshold: (optional) scalar minimum difference between elements to be considered.
    :param rng: (optional) np.random.Generator instance
    :return: list of tuples (((i, j), *c), p),
        meaning that
        prob{ X_i - X_j > threshold in case=*c } AND similar for all preceding tuples } = p,
        where (i, j) are index label(s) in x,
        c includes zero, one, or more labels in given case index or indices.

    Method: Data for each x_group are re-sampled for equal number of samples,
    then handled as usual by cred_diff function.
    """
    if type(group_axis) is not tuple:
        group_axis = (group_axis,)
    if case_axis is None:
        case_axis = ()
    elif type(case_axis) is not tuple:
        case_axis = (case_axis,)
    if len(case_axis) > 0:
        for (g, x) in x_groups.items():
            must_unstack = [c for c in x.index.names if c in case_axis]
            x_groups[g] = x.unstack(must_unstack)
    max_n_samples = max(x.shape[0] for x in x_groups.values())
    # all rows in each x are assumed independent samples
    # re-sample to equal size
    for (g, x) in x_groups.items():
        n_x = x.shape[0]
        if n_x < max_n_samples:
            x_add = x.sample(max_n_samples - n_x, axis=0, replace=True, random_state=rng)
            x_groups[g] = pd.concat([x, x_add],
                                    axis=0, ignore_index=True)
    x_groups = pd.concat(x_groups, axis=0,
                         names=list(group_axis))
    # = pd.DataFrame with groups to be compared
    return cred_diff(x_groups, diff_axis=group_axis, case_axis=case_axis, p_lim=p_lim, threshold=threshold)


# -------------------------------------------------------------------
def cred_corr(x, corr_axis, vector_axis=(), p_lim=0.6):
    """Find set of jointly credible correlations between random vectors or scalars,
    represented by samples from joint distributions.
    :param x: a pd.DataFrame or pd.Series instance,
        with rows containing i.i.d. samples from jointly distributed random variables.
    :param corr_axis: label(s) of axis representing separate random variables / vectors,
        for which credible correlations are to be found.
        May be axis in either columns or index of x.
    :param vector_axis: (optional) label(s) of axis with related vector elements in each sample.
        Row index axis NOT named in corr_axis or vector_axis are used as samples.
    :param p_lim: (optional) scalar minimum joint credibility for difference to be included
    :return: list of tuple((i, j), p, median_corr), where
        (i, j) is the pair of labels along corr_axis for the credibly correlated random variables
        p = the JOINT credibility of this and all previous tuples in the list,
        median_c = the median conditional correlation coefficient, given that
            all previous correlations in the list are credibly non-zero.

    The correlation (cosine) values are calculated WITHOUT subtraction of the mean,
    i.e., vectors are treated as non-normalized directions in multidimensional space.
    For random scalars, each correlation sample is the product, normalized by sample std.deviation.
    For random vectors, each correlation sample is the cosine angle between elements in each pair of vector samples,
        normalized by root mean square across all samples,
        with vector elements stored along vector_axis of x.

    Arne Leijon, 2023-04-16
    """
    # ------------------------------------------------- check args
    if type(corr_axis) is not tuple:
        corr_axis = (corr_axis,)
    if type(vector_axis) is not tuple:
        vector_axis = (vector_axis,)
    if type(x) is pd.DataFrame:
        must_stack = [c for c in x.columns.names if c not in corr_axis]
        if len(must_stack) > 0:
            x = x.stack(must_stack, future_stack=True)
    must_unstack =  [c for c in x.index.names if c in corr_axis]
    x = x.unstack(must_unstack)
    # now columns include the separate variables for which correlations are calculated
    # rows are samples, possibly sub-grouped by vector_axis dimension(s)
    sample_axis = [i for (i, i_name) in enumerate(x.index.names)
                   if i_name not in vector_axis]
    # any index levels NOT named in vector_axis are considered as part of sample index
    if len(sample_axis) == 0:
        raise RuntimeError('No sample axis in data')
    if len(sample_axis) > 1:
        logger.warning(f'Sample index includes {len(sample_axis)} levels: '
                       + str([x.index.names[i] for i in sample_axis]))
    n_samples = x.shape[0]
    if n_samples < 200:
        logger.warning(f'Only {n_samples} samples: Too few -> unreliable results.')
    # ---------------------------------------------------------
    pair_cols = list(combinations(x.columns, 2))
    corr = pd.DataFrame({(i, j): normalized_xy(x[i], x[j], sample_axis)
                         for (i,j) in pair_cols},
                        columns=pair_cols)
    # Each row of corr has ONE correlation sample for each (i,j) pair
    return credibly_nonzero(corr, p_lim)


# -------------------------------------------------------------------
def normalized_xy(x, y, sample_axis):
    """Calculate normalized correlation between two sampled random variables
    :param x: pd.Series instance, with index (samples, *vector_axis)
    :param y: pd.Series instance, with same index as x
    :param sample_axis: integer of label defining sample axis of x and y
    :return: pd.Series with correlation values, grouped by vector_axis
    """
    xy = x * y
    x2 = x**2
    y2 = y**2
    if x.index.nlevels == 1:
        return xy / np.sqrt(x2.mean() * y2.mean())
    else:
        xy = xy.groupby(level=sample_axis).sum()
        x2 = x2.groupby(level=sample_axis).sum()
        y2 = y2.groupby(level=sample_axis).sum()
        # = sq sum along vector_axis
        return xy / np.sqrt(x2.mean() * y2.mean())


def credibly_nonzero(x, p_lim=0.6):
    """Find set of elements of a random-vector X that are credibly non-zero,
    useful, e.g., when X is a random array of correlation-like values.
    :param x: a pd.DataFrame with sampled values from a random vector, stored as
        column x[id] = a pd.Series with scalar samples for ONE scalar random variable,
        one sample in each row.
    :param p_lim: (optional) scalar minimum joint credibility for difference to be included

    :return: list of tuples(id, p, median_x), where
        id is a column-identifying element from input x,
        p is the JOINT credibility of non-zero values,
        meaning that
        max( prob{ X_id > 0), prob(X_id < 0) ) AND similar for all previous tuples} = p
        median_x is the conditional median(X_id), given that X is non-zero in all previous tuples.

        The probability is estimated from the relative frequency of samples
        which are systematically deviating from zero on either side,
        using the side that has the greatest relative frequency,
        including only the remaining samples for which all previous results were satisfied.
        Thus, if 80% of samples are positive, p = 0.8.
        Similarly, if 80% of samples are negative, p = 0.8.
        If the median of samples is zero, p = 0.5, indicating no systematic deviation from zero.
        Thus, the resulting median_x values indicate both the sign and magnitude of the deviation from zero.

    As each successive result tuple includes one new element in the credible set,
    the joint probability decreases with each new element in the sequence.
    Therefore, the result list is automatically ordered
    with non-increasing values of p.
    The absolute value of median_x will also decrease toward zero.

    Arne Leijon, 2023-04-16
    """
    def check_reverse():
        """Flip bool_x column(s), where False is more common than True
        :return: None, operates in place
        """
        n_x = bool_x.shape[0]
        flip = [col for (col, p_x) in bool_x.items() if p_x.sum() < n_x / 2]
        bool_x[flip] = np.logical_not(bool_x[flip])

    # -------------------------------------------------------------------
    n_samples = x.shape[0]
    bool_x = x > 0.
    check_reverse()

    res = []
    # space for result
    p_pos = (bool_x.sum(axis=0) + 0.5) / (n_samples + 1)
    while np.any(p_pos > p_lim):
        col_max = p_pos.idxmax()
        # = id of column with maximum prob of positive values
        res.append((col_max, p_pos[col_max], x[col_max].median()))
        keep_rows = bool_x[col_max]
        bool_x.drop(columns=col_max, inplace=True)
        # keeping only columns not yet included in res
        bool_x = bool_x.loc[keep_rows]
        x = x.loc[keep_rows]
        # keep only samples (rows) where accepted condition was satisfied
        # reduced x needed to calculate median only for remaining samples
        check_reverse()
        p_pos = (bool_x.sum(axis=0) + 0.5) / (n_samples + 1)
    return res


# ----------------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.stats import norm

    print('*** Testing cred_diff, cred_group_diff, cred_corr')
    n_samples = 1000
    mu = [[0., 0.5, 1.],
          [0., -1., 0.5],
          [0., -1., -2.]]
    n_mu = 3
    len_x = 3
    x_labels = [f'x{i}' for i in range(len_x)]
    case_labels = [c for c in 'ABCDEF'[:n_mu]]
    x = np.array([norm.rvs(loc=m, size=(n_samples, len_x))
                  for m in mu])
    x2 = x.reshape((-1, len_x))
    ind = pd.MultiIndex.from_product([case_labels, range(n_samples)],
                                     names=['Case', '_sample'])
    x = pd.DataFrame(x2, index=ind, columns=x_labels)
    x.columns.set_names('x_element', inplace=True)
    print('x = \n', x.head())
    # y = pd.DataFrame(x2, columns=[(xi, xi) for xi in x_labels], index=ind)
    # # y.columns = Index with tuples as labels
    # z = pd.DataFrame({(xi, xi): x2[:, i]
    #                   for (i, xi) in enumerate(x_labels)},
    #                  index=ind)
    # z.columns = MultiIndex with two levels

    print('\nTest cred_diff:')
    d = cred_diff(x, diff_axis='x_element', case_axis='Case')
    print('cred_diff = ', d)
    mu_df = pd.DataFrame(mu,
                         index=pd.Index(case_labels, name='Case'),
                         columns=x_labels)
    true_prob_diff = [norm.cdf(mu_df.loc[c, i] - mu_df.loc[c, j], scale=np.sqrt(2))
                      for (((i,j),c), _) in d]
    # print('true marg. prob. ', true_prob_diff)
    print('true joint prob. ', np.cumprod(true_prob_diff))
    print("""NOTE: the 3rd cred_diff result shows slightly over-estimated credibility
    probably because the largest value is selected in each step,
    and the test data includes three different cases with equal true differences
    """)

    print('\nTest cred_group_diff:')
    n_group_samples = [100, 500, 1000]
    x_groups = {g: pd.DataFrame(norm.rvs(loc=m, size=(ns, len_x)),
                                columns=pd.Index(x_labels, name='X'))
                for (g, m, ns) in zip(case_labels, mu, n_group_samples)}

    d = cred_group_diff(x_groups, group_axis='Group', case_axis='X')
    print('cred_group_diff = ', d)
    mu_df = pd.DataFrame(mu,
                         index=pd.Index(case_labels, name='Group'),
                         columns=x_labels)
    true_prob_diff = [norm.cdf(mu_df.loc[i, c] - mu_df.loc[j, c], scale=np.sqrt(2))
                      for (((i, j), c), _) in d]
    print('true joint prob. = ', np.cumprod(true_prob_diff))

    # -----------------------------------------
    print('\nTest cred_corr:')
    xt = x.stack('x_element')
    xt = xt.unstack('Case')
    d = cred_corr(xt, corr_axis='Case', vector_axis='x_element')
    print('cred_corr ', d)

    cosine = np.array([np.sum(x_i * x_j)
                       / np.sqrt((np.sum(x_i ** 2) + len_x) *
                                 (np.sum(x_j ** 2) + len_x))
                       for (x_i, x_j) in combinations(np.array(mu), 2)])
    print('cosine = ', cosine)
    # ij_pairs = [p for p in combinations(range(n_mu), 2)]
    # print('mu cosine = ', [ (ij, c) for (ij, c) in zip(ij_pairs, cosine)])
