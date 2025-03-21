# -*- coding: utf-8 -*-

"""
Created on Thu Sep 27 14:30:24 2018

@author: Ali
"""
from time import time

import logging

import sys
import numpy as np
import numba
import pdb
from numpy import linalg as LA
import pandas as pd
import inspect


#### Model calculation  ###

@numba.jit(nopython=True, debug=False)
def build_word_transition_vector(word_proba, wfreq, word_leak):
    """
    Calculates the transition probability of the word markov chain

    :param word_proba: word probabilities
    :param wfreq: word frequencies
    :param word_leak: leak parameter
    :return: the transition vector.
    """
    lng = word_proba.shape[0]
    res = np.zeros(lng)
    for i in range(lng):
        res[i] = (word_proba[i] + wfreq[i] * word_leak) / (1 + word_leak)
    return res / res.sum()


@numba.jit(nopython=True)
def TD_dist(word_dist, repr):
    """
    Calculates the top-down retroaction on letters.

    :param word_dist: word distribution
    :param repr: arrays of lexical representations
    :return: The distribution corresponding the the top-down retroaction on letters.
    """
    sh = repr.shape
    res = np.zeros((sh[1], sh[2]))
    for i in range(sh[0]):  # mots du lexique
        for j in range(sh[1]):
            for k in range(sh[2]):
                res[j, k] += word_dist[i] * repr[i, j, k]
    return res


@numba.jit(nopython=True)
def wsim(repr, percept):
    """
    Calculates the similarity between the percept and the lexical representations: np.einsum('jk,ijk->ij', percept_dist, self.orth_dist)

    :param repr: lexical representations
    :param percept: percept distribution
    :return: the similarity array
    """
    # to calculate wsim_value, calculate the product for each word
    # of pok*mot * perr*mot where the error occurs, which is equivalent to:
    # prod(pok*m) * perr_j/pok_j *m = prod(pok*m) * (1-pok_j)/pok_j
    sh = repr.shape
    res = np.ones((sh[0], sh[1] + 1))  # lexicon words, ok+4erreurs
    for i in range(sh[0]):  # lexicon words
        for j in range(sh[1]):  # error position
            tmp_ok = 0
            tmp_l = 0
            for k in range(sh[2]):
                l = repr[i, j, k]
                p = percept[j, k]
                tmp_l += l
                tmp_ok += p * l
            res[i, 0] *= tmp_ok  # at the end, we have the product of the ok at all positions
            # this line only works by replacing tmp_l with 1 if the l's are in norm 1
            res[i, j + 1] *= (tmp_l - tmp_ok) / tmp_ok if tmp_ok > 0 else 0  # error in position j
        for j in range(sh[1]):  # error positions
            res[i, j + 1] *= res[i, 0]
    return res


@numba.jit(debug=False)
def word_sim_att(repr, percept, attention):
    """
    Calculates the similarity vector np.einsum('lij,ij->li', repr, percept), but modulated by attention:

    :param repr: lexical representations
    :param percept: percept distribution
    :param attention: the attention distribution
    :return: the similarity array
    """
    sh = repr.shape
    res = np.ones((sh[0]))
    for i in range(sh[0]):  # lexicon words
        for j in range(sh[1]):  # position within the word
            if np.sum(repr[i, j]) > 0:
                tmp = 0
                att = attention[j]
                u = (1 - att) / sh[2]
                for k in range(sh[2]):  # alphabet letter
                    tmp += (att * repr[i, j, k] * percept[j, k]) + u
                res[i] *= tmp
            else:
                res[i] = 0
    return res


@numba.jit(nopython=True, debug=False)
def create_repr(words_indices, size, eps):
    """
    Creates lexical representations of the model.

    :param words_indices: indices corresponding to the position in the alphabet for each letter of each word.
    :param size: int, size of the alphabet.
    :param eps: float, epsilon value for the quality of the representation
    :return: lexical representations.
    """
    wdi = np.shape(words_indices)
    arr = np.zeros((wdi[0], wdi[1], size), dtype=np.float32)
    for iwd in range(arr.shape[0]):
        wd = words_indices[iwd]
        for iN in range(arr.shape[1]):
            letter_index = wd[iN]
            eps_final = 0.66 / (size - 1) if letter_index == size - 1 else eps
            for iL in range(arr.shape[2]):
                # -1 = uniform, -2 = null
                arr[iwd, iN, iL] = 1 / size if letter_index == -1 else 0 if letter_index == -2 else \
                    1 - eps_final * (size - 1) if iL == letter_index else eps_final
    return arr


@numba.jit(nopython=True, debug=False)
def create_repr_mixt(words_indices, size, eps, repr_type):
    """
    Creates lexical representations of the model with mixed types of representation, corresponding to different epsilon values.
    :param words_indices: indices corresponding to the position in the alphabet for each letter of each word.
    :param size: int, size of the alphabet.
    :param eps: float, epsilon value for the quality of the representation
    :return: lexical representations.
    """
    wdi = np.shape(words_indices)
    arr = np.zeros((wdi[0], wdi[1], size))
    for iwd in range(arr.shape[0]):  # mots
        wd = words_indices[iwd]
        idx = repr_type[iwd]
        eps_mixt = eps if idx == 0 else 0.02 if idx == 1 else 1 / size
        for iN in range(arr.shape[1]):  # letter position
            letter_index = wd[iN]
            for iL in range(arr.shape[2]):  # alphabet letter
                arr[iwd, iN, iL] = 1 / size if letter_index == -1 else \
                    1 - eps_mixt * (size - 1) if iL == letter_index else eps_mixt
    return arr


def gaussian(mu, sigma, length):
    """
    Returns a normalized Gaussian vector of a specified length, centered at a given mean and with a given standard deviation.

    :param mu: the mean of the Gaussian distribution.
    :param sigma: the standard deviation of the Gaussian distribution.
    :param length: the length of the output vector
    :return: a normalized Gaussian vector.
    """
    vect = np.exp(-np.power(np.arange(0, length) - mu, 2.) / (2 * np.power(sigma, 2.)))
    return vect / np.sum(vect)


def gaussian_to_creneau(dist):
    """
    Turns a gaussian distribution into a creneau distribution, keeping all values above a threshold
    :param dist: the gaussian distribution to turn into a creneau
    :return: np array of the distribution
    """
    n = sum([1 for i in dist if i > 0.1])
    dist = np.array([1 / n if i > 0.1 else 0 for i in dist])
    return dist


def calculate_sigma(grapheme_deb, len_stim, len_grapheme, max_ext, threshold):
    """
    Calculates gaussian parameters to align visual attention with a single grapheme.

    :param grapheme_deb: int. Starting position of a grapheme in a sequence
    :param len_stim: int. Length of the stimulus.
    :param len_grapheme: int. Length of the grapheme.
    :param max_ext: float. Maximum attention value to reach outside the grapheme
    :param threshold: float. threshold to consider max_ext has been reached.
    :return: values for mu and sigma
    """
    mu = grapheme_deb + (len_grapheme - 1) / 2
    if grapheme_deb + len_grapheme - 1 >= len_stim or grapheme_deb < 0:
        print("Error : bad configuration of parameters")
        return
    sigma_min = 0.25
    sigma_max = 2.25
    fin = False
    calcule_min = True
    calcule_max = True
    while not fin:
        if calcule_min:
            mu_min_gaussian = gaussian(mu, sigma_min, len_stim)
            mu_min_val = max([val if abs(i - mu) > len_grapheme / 2 else 0 for i, val in enumerate(mu_min_gaussian)])
        if calcule_max:
            mu_max_gaussian = gaussian(mu, sigma_max, len_stim)
            mu_max_val = max([val if abs(i - mu) > len_grapheme / 2 else 0 for i, val in enumerate(mu_max_gaussian)])
        if abs(mu_min_val - max_ext) < threshold or abs(mu_max_val - max_ext) < threshold or mu_max_val < max_ext or mu_min_val > max_ext:
            fin = True
        if abs(mu_min_val - max_ext) < abs(mu_max_val - max_ext):
            calcule_min = False
            calcule_max = True
            sigma_max = (sigma_min + sigma_max) / 2
        else:
            calcule_max = False
            calcule_min = True
            sigma_min = (sigma_min + sigma_max) / 2
        print(mu_min_val, mu_max_val, sigma_min, sigma_max)
    return mu, sigma_max if calcule_min else sigma_min

##### General utilities ####


def norm1D(arr):
    """
    Normalizes a one-dimensional array.

    :param arr: a one-dimensional array
    :return: the normalized version of the input array `arr`.
    """
    arr = np.array(arr)
    if arr.sum() > 0:
        return arr / arr.sum()
    return arr


def norm_percept(p):
    """
    Normalizes an array in the same shape as the percept distribution.

    :param p: the percept distribution
    :return: the normalized vector.
    """
    return p / p.sum(axis=1, keepdims=True)


@numba.jit(nopython=True, debug=False)
def norm2D(matrix, n=2):
    """
    Norms a 2D vector.

    :param matrix: vector to be normalized
    :param n: the norm Lx to be considered.
    :return: the normalized vector.
    """
    if matrix is not None:
        res = np.zeros(matrix.shape)
        for j in range(matrix.shape[0]):
            if n == 2:
                norm = LA.norm(matrix[j, :])
            else:
                norm = np.sum(matrix[j, :])
            if norm > 0:
                for k in range(matrix.shape[1]):
                    res[j, k] = matrix[j, k] / norm
        return res
    return None


@numba.jit(nopython=True, debug=False)
def norm3D(matrix, n=2):
    """
    Norms a 3D vector.

    :param matrix: vector to be normalized
    :param n: the norm Lx to be considered.
    :return: the normalized vector.
    """
    res = np.zeros(matrix.shape)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if n == 2:
                norm = LA.norm(matrix[i, j, :])
            else:
                norm = np.sum(matrix[i, j, :])
            if norm > 0:
                for k in range(matrix.shape[2]):
                    res[i, j, k] = matrix[i, j, k] / norm
    return res


@numba.jit(nopython=True, debug=False)
def calculate_norm3D(matrix):
    """
    Calculated the L2 norm of 3D vectors

    :param matrix: the vector
    :return: the norm.
    """
    res = np.ones(matrix.shape[0])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            res[i] *= LA.norm(matrix[i, j, :])
    return res


def l_round(liste, n=3):
    """
    Takes a list of numbers and returns a new list with each number rounded to a specified number of decimal places (default is 3).

    :param liste: a list of numbers that you want to round
    :param n: the number of decimal places to round each element in the input list to.
    :return: a new list where each element is rounded to the specified number of decimal places.
    """
    return [round(i, n) for i in liste]


def edit_distance(s1, s2, subst_cost=0.4):
    """
    Calculates the Levenshtein distance between two strings, with an optional substitution cost. The edit_distance function calculates the Levenshtein distance between s1 and s2.
    The Levenshtein distance is the minimum number of operations (insertions, deletions, and substitutions) required to transform s1

    :param s1: s1 is the first string that you want to compare
    :param s2: s2 is the second string that we want to compare with s1.
    :param subst_cost: the cost of substituting one character with another.
    :return: the Levenshtein distance between two strings `s1` and `s2`.
    """
    len1 = len(s1)
    len2 = len(s2)
    lev = [[i if j == 0 else j if i == 0 else 0 for j in range(len2 + 1)] for i in range(len1 + 1)]
    for i in range(len1):
        for j in range(len2):
            lev[i + 1][j + 1] = min(lev[i][j + 1] + 1, lev[i + 1][j] + 1, lev[i][j] + subst_cost * abs(s1[i] - s2[j]))
    return lev[len1][len2]


def get_size(obj, seen=None):
    """Recursively finds size of objects : for memory investigation

    :param: the object you want to know the size
    :return: its size"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def fullspec(passedFunc, *args, **kwargs):
    """
    Takes a function and its arguments, and returns a dictionary containing all the arguments with their corresponding values, including default values if not provided.

    :param passedFunc: a function object that you want to inspect and extract the arguments and their values from
    :return: a dictionary containing the parameters and their corresponding values that will be passed to the `passedFunc` function.
    """
    spec = inspect.getfullargspec(passedFunc)
    args_names = spec.args[1:] if spec.args[0] == 'self' else spec.args
    params = dict(zip(args_names, args))
    defaults = dict(zip(args_names[-len(spec.defaults):], spec.defaults))
    for k, v in kwargs.items():
        params[k] = v
    for k in args_names:
        if k not in params:
            if k in defaults:
                params[k] = defaults[k]
            else:
                raise TypeError('missing argument', k)
    return params


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    addLoggingLevel('TRACE', logging.DEBUG - 5)
    logging.getLogger(__name__).setLevel("TRACE")
    logging.getLogger(__name__).trace('that worked')
    logging.trace('so did this')
    logging.TRACE
    5
            if self.segment_reading and len(tmp)>0:
                n=sum([1 for i in tmp if i>0.1])
                tmp=np.array([1/n if i>0.1 else 0 for i in tmp])
                tmp[tmp > 1] = 1

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


for lib in ['numba', 'numpy', 'bokeh', 'selenium', 'urllib3']:
    logger = logging.getLogger(lib)
    logger.setLevel(logging.WARNING)
# on crée différents niveaux de logging
addLoggingLevel("BRAID", 11)
addLoggingLevel("SIMU", 13)
addLoggingLevel("GUI", 14)
addLoggingLevel("EXPE", 21)


def abstractmethod(method):
    """
    An @abstractmethod member fn decorator.
    (put this in some library somewhere for reuse).

    """
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method '
                                  + repr(method))
    default_abstract_method.__name__ = method.__name__
    return default_abstract_method


def matplotlib_style():
    """
    Parameters for matplotlib display

    :return: the parameters
    """
    from matplotlib import pylab
    import matplotlib.pyplot as plt
    params = {'legend.fontsize': 'x-large',
              'legend.title_fontsize': 'xx-large',
              'axes.labelsize': 18,
              'axes.titlesize': 'x-large',
              'xtick.labelsize': 'x-large',
              'ytick.labelsize': 'x-large',
              'figure.facecolor': "white",
              }
    pylab.rcParams.update(params)
    plt.rcParams.update({'axes.titlesize': 'x-large'})
    plt.rcParams.update({'axes.labelsize': 'x-large'})


def pandas_options():
    """
    Parameters for pandas display

    :return: the parameters
    """
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 3)


def prod(w1, w2, normalize=True):
    """
    Calculates the element-wise product of two arrays and optionally normalizes the result.

    :param w1: the first set of values
    :param w2: the second set of weights
    :param normalize: boolean flag that determines whether the output should be normalized or not.
    :return: the product of two arrays `w1` and `w2`.
    """
    arr = np.array([np.array(i) * np.array(j) for i, j in zip(w1, w2)])
    return norm2D(arr, n=1) if normalize else arr


def str_transfo(str1):
    """
    Removes any leading `#` and trailing `~` characters from a string and splits the string at the first occurrence of `_`.

    :param str1: the string to be transformed
    :return: the new string.
    """
    return str1.split('_')[0].replace('#', '').replace('~', '')


def str_eq(str1, str2):
    """
    Compares two strings after removing any leading `#` and trailing `~` characters and splitting the strings at the first occurrence of `_`.

    :param str1: the first string
    :param str2: the second string
    :return: a boolean
    """
    return str_transfo(str1) == str_transfo(str2)


def uniform(length):
    """Uniform distribution given its length"""
    return np.ones(length) / length
