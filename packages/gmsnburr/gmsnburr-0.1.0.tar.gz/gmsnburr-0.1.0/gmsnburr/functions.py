import numpy as np
import pytensor.tensor as at
from pytensor.tensor import gammaln, switch, isinf
from scipy.special import betaincinv, gammaln as np_gammaln
from pymc.distributions.shape_utils import rv_size_is_none
from typing import Optional, Tuple
from pymc.distributions.dist_math import check_parameters

def check_params(alpha1, alpha2, sigma):
    """
    Memeriksa apakah input parameter valid
        alpha1 >= 0
        alpha2 >= 0
        sigma >= 0
    """
    if np.any(alpha1 <= 0):
        raise ValueError("alpha1 harus lebih besar dari 0")
    if np.any(alpha2 <= 0):
        raise ValueError("alpha2 harus lebih besar dari 0")
    if np.any(sigma <= 0):
        raise ValueError("sigma harus ldebih besar dari 0")

def to_tensor(*args):
    """Mengonversi input menjadi tensor variable."""
    return [at.as_tensor_variable(arg) for arg in args]

# PDF
def pdf(y, mu, sigma, alpha1, alpha2, log=False):
    """
    Fungsi untuk menghitung PDF GMSNBurr(y|mu, sigma, alpha1, alpha2)
    Input parameter:
        y = value
        mu = parameter lokasi
        sigma = parameter skala (>= 0)
        alpha1 = parameter bentuk (>= 0)
        alpha2 = parameter bentuk (>= 0)
        log = boolean untuk menghitung logaritma natural PDF (default=False)
    Return:
        Logaritma Natural PDF jika log = True
        PDF jika log = False
    """
    check_params(alpha1, alpha2, sigma)
    y, mu, sigma, alpha1, alpha2 = to_tensor(y, mu, sigma, alpha1, alpha2)
    betaln_val = gammaln(alpha1) + gammaln(alpha2) - gammaln(alpha1 + alpha2)
    lomega = (
        -0.5 * at.log(2 * at.pi)
        + betaln_val
        - alpha2 * (at.log(alpha2) - at.log(alpha1))
        + (alpha1 + alpha2) * at.log1p(alpha2 / alpha1))
    omega = at.exp(lomega)
    zo = -omega * ((y - mu) / sigma)
    zoa = zo + at.log(alpha2) - at.log(alpha1)
    logp_val = (
        lomega
        - at.log(sigma)
        + alpha2 * (at.log(alpha2) - at.log(alpha1))
        + alpha2 * zo
        - (alpha1 + alpha2) * at.log1p(at.exp(zoa))
        - betaln_val)
    lp = switch(isinf(zo), -at.inf, logp_val)
    return lp if log else at.exp(lp)

# CDF
def cdf(y, mu, sigma, alpha1, alpha2, lower_tail=True, log=False):
    """
    Fungsi untuk menghitung CDF GMSNBurr(y|mu, sigma, alpha1, alpha2)
    Input parameter:
        y = value
        mu = parameter lokasi
        sigma = parameter skala (>= 0)
        alpha1 = parameter bentuk (>= 0)
        alpha2 = parameter bentuk (>= 0)
        lower_tail = P(X <= x) jika True, P(X > x) jika False (default = True)
        log = boolean untuk menghitung logaritma natural PDF (default = False)
    Return:
        Logaritma Natural CDF lower tail jika log = True dan lower_tail = True
        Logaritma Natural CDF upper tail jika log = True dan lower_tail = False
        CDF lower tail jika log = False dan lower_tail = True
        CDF upper tail jika log = True dan lower_tail = False
    """
    check_params(alpha1, alpha2, sigma)
    y, mu, sigma, alpha1, alpha2 = to_tensor(y, mu, sigma, alpha1, alpha2)
    betaln_val = gammaln(alpha1) + gammaln(alpha2) - gammaln(alpha1 + alpha2)
    lomega = (
        -0.5 * at.log(2 * at.pi)
        + betaln_val
        - alpha2 * (at.log(alpha2) - at.log(alpha1))
        + (alpha1 + alpha2) * at.log1p(alpha2 / alpha1))
    omega = at.exp(lomega)
    epart = at.exp(- (alpha2 / alpha1) * omega * ((y - mu) / sigma))
    ep = 1 / (1 + epart)
    cdf_value = at.betainc(alpha1, alpha2, ep)
    if log:
        log_cdf_value = at.log(cdf_value) if lower_tail else at.log(1 - cdf_value)
        return log_cdf_value
    else:
        return cdf_value if lower_tail else 1 - cdf_value

# Random
def random(mu: np.ndarray | float, sigma: np.ndarray | float, alpha1: np.ndarray | float, alpha2: np.ndarray | float, rng = np.random.default_rng(), size: Optional[Tuple[int]]=None):
    check_params(alpha1, alpha2, sigma)
    betaln_val = np_gammaln(alpha1) + np_gammaln(alpha2) - np_gammaln(alpha1 + alpha2)
    lomega = (
        -0.5 * np.log(2 * np.pi)
        + betaln_val
        - alpha2 * (np.log(alpha2) - np.log(alpha1))
        + (alpha1 + alpha2) * np.log1p(alpha2 / alpha1))
    omega = np.exp(lomega)
    z1 = np.random.chisquare(2 * alpha1, size=size) / (2 * alpha1)
    z2 = np.random.chisquare(2 * alpha2, size=size) / (2 * alpha2)
    logzf = np.log(z2) - np.log(z1)
    random_variate = mu - (sigma / omega) * logzf
    return np.asarray(random_variate)

# Moment
def moment(y, size, mu, sigma, alpha1, alpha2):
    check_params(alpha1, alpha2, sigma)
    y, mu, sigma, alpha1, alpha2 = to_tensor(y, mu, sigma, alpha1, alpha2)
    if size is None:
        size = y.shape
    betaln_val = gammaln(alpha1) + gammaln(alpha2) - gammaln(alpha1 + alpha2)
    lomega = (
        -0.5 * at.log(2 * at.pi)
        + betaln_val
        - alpha2 * (at.log(alpha2) - at.log(alpha1))
        + (alpha1 + alpha2) * at.log1p(alpha2 / alpha1))
    omega = at.exp(lomega)
    moment = mu + sigma/omega*(at.log(alpha2/alpha1) + at.digamma(alpha1)- at.digamma(alpha2))
    return at.full(size, moment)

# Quantile
def quantile(p, mu, sigma, alpha1, alpha2):
    check_params(alpha1, alpha2, sigma)
    betaln_val = np_gammaln(alpha1) + np_gammaln(alpha2) - np_gammaln(alpha1 + alpha2)
    lomega = (
        -0.5 * np.log(2 * at.pi)
        + betaln_val
        - alpha2 * (np.log(alpha2) - np.log(alpha1))
        + (alpha1 + alpha2) * np.log1p(alpha2 / alpha1))
    omega = np.exp(lomega)
    ib = betaincinv(alpha1, alpha2, p)
    s = (1 / ib) - 1
    quantile_value = mu - (sigma / omega) * (alpha2 / alpha1) * np.log(s)
    return quantile_value