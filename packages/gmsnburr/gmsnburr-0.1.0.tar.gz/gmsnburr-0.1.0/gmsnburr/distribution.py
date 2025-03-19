import pymc as pm
import numpy as np
import pytensor.tensor as at
from pytensor.tensor import gammaln, switch, isinf
from scipy.special import betaincinv, gammaln as np_gammaln
from typing import Optional, Tuple

# KOMPONEN 1: Logaritma Natural PDF
def logp(y: at.TensorVariable,
        mu: at.TensorVariable,
        sigma: at.TensorVariable,
        alpha1: at.TensorVariable,
        alpha2: at.TensorVariable,
        log=True): # untuk output dalam logaritma natural PDF, jika false output PDF

    # periksa input parameter alpha1, alpha2, dan sigma
    if not at.all(alpha1 > 0):
        raise ValueError("alpha1 harus lebih besar dari 0")
    if not at.all(alpha2 > 0):
        raise ValueError("alpha2 harus lebih besar dari 0")
    if not at.all(sigma > 0):
        raise ValueError("sigma harus lebih besar dari 0")

    # hitung nilai logaritma natural beta(alpha1, alpha2)
    betaln_val = gammaln(alpha1) + gammaln(alpha2) - gammaln(alpha1 + alpha2)

    # hitung logaritma natural omega
    lomega = (
        -0.5 * at.log(2 * at.pi)
        + betaln_val
        - alpha2 * (at.log(alpha2) - at.log(alpha1))
        + (alpha1 + alpha2) * at.log1p(alpha2 / alpha1))

    # nilai omega
    omega = at.exp(lomega)

    # (y - mu) / sigma
    zo = -omega * ((y - mu) / sigma)
    zoa = zo + at.log(alpha2) - at.log(alpha1)

    # hitung logp
    logp = (
        lomega
        - at.log(sigma)
        + alpha2 * (at.log(alpha2) - at.log(alpha1))
        + alpha2 * zo
        - (alpha1 + alpha2) * at.log1p(at.exp(zoa))
        - betaln_val
    )

    # memeriksa zo apakah infinity
    lp = switch(isinf(zo), -at.inf, logp)

    if log:
        return lp # untuk logaritma natural PDF
    else:
        return at.exp(lp)  # untuk nilai PDF sebenarnya

# KOMPONEN 2: Logaritma Natural CDF
def logcdf(y: at.TensorVariable,
          mu: at.TensorVariable,
          sigma: at.TensorVariable,
          alpha1: at.TensorVariable,
          alpha2: at.TensorVariable,
          lower_tail=True, # untuk output lower tail, jika false upper tail
          log=True, # untuk output dalam logaritma natural CDF, jika false output CDF
          **kwargs):

    # periksa input parameter alpha1, alpha2, dan sigma
    if not at.all(alpha1 > 0):
        raise ValueError("alpha1 harus lebih besar dari 0")
    if not at.all(alpha2 > 0):
        raise ValueError("alpha2 harus lebih besar dari 0")
    if not at.all(sigma > 0):
        raise ValueError("sigma harus lebih besar dari 0")

    # hitung nilai logaritma natural beta(alpha1, alpha2)
    betaln_val = gammaln(alpha1) + gammaln(alpha2) - gammaln(alpha1 + alpha2)

    # hitung logaritma natural omega
    lomega = (
        -0.5 * at.log(2 * at.pi)
        + betaln_val
        - alpha2 * (at.log(alpha2) - at.log(alpha1))
        + (alpha1 + alpha2) * at.log1p(alpha2 / alpha1))

    # nilai omega
    omega = at.exp(lomega)

    # komponen CDF
    epart = at.exp(- (alpha2 / alpha1) * omega * ((y - mu) / sigma))
    ep = 1 / (1 + epart)

    # hitung nilai CDF dengan incomplete beta ratio
    cdf_value = at.betainc(alpha1, alpha2, ep)

    # menghitung logaritma natural CDF
    if log:
        # output lower tail, jika false upper tail
        log_cdf_value = at.log(cdf_value) if lower_tail else at.log(1 - cdf_value)
        return log_cdf_value
    else: # untuk nilai CDF sebenarnya
        return cdf_value if lower_tail else 1 - cdf_value

# KOMPONEN 3: Random
def random(
      mu: np.ndarray | float,
      sigma: np.ndarray | float,
      alpha1: np.ndarray | float,
      alpha2: np.ndarray | float,
      rng = np.random.default_rng(),
      size: Optional[Tuple[int]]=None):

    # periksa input parameter alpha1, alpha2, dan sigma
    if sigma <= 0:
        raise ValueError("sigma must be more than 0")
    if alpha1 <= 0:
        raise ValueError("alpha1 must be more than 0")
    if alpha2 <= 0:
        raise ValueError("alpha2 must be more than 0")

    # hitung nilai logaritma natural beta(alpha1, alpha2)
    betaln_val = np_gammaln(alpha1) + np_gammaln(alpha2) - np_gammaln(alpha1 + alpha2)

    # hitung logaritma natural omega
    lomega = (
        -0.5 * np.log(2 * np.pi)
        + betaln_val
        - alpha2 * (np.log(alpha2) - np.log(alpha1))
        + (alpha1 + alpha2) * np.log1p(alpha2 / alpha1))

    # nilai omega
    omega = np.exp(lomega)

    z1 = np.random.chisquare(2 * alpha1, size=size) / (2 * alpha1)
    z2 = np.random.chisquare(2 * alpha2, size=size) / (2 * alpha2)
    logzf = np.log(z2) - np.log(z1)
    random_variate = mu - (sigma / omega) * logzf

    return np.asarray(random_variate)

# KOMPONEN 4: Moment
def moment(y, size,
          mu: at.TensorVariable,
          sigma: at.TensorVariable,
          alpha1: at.TensorVariable,
          alpha2: at.TensorVariable):

    # cek shape input
    if size is None:
        size = y.shape

    # hitung nilai logaritma natural beta(alpha1, alpha2)
    betaln_val = gammaln(alpha1) + gammaln(alpha2) - gammaln(alpha1 + alpha2)

    # hitung logaritma natural omega
    lomega = (
        -0.5 * at.log(2 * at.pi)
        + betaln_val
        - alpha2 * (at.log(alpha2) - at.log(alpha1))
        + (alpha1 + alpha2) * at.log1p(alpha2 / alpha1))

    # nilai omega
    omega = at.exp(lomega)

    # komponen moment
    moment = mu + sigma/omega*(at.log(alpha2/alpha1) + at.digamma(alpha1)- at.digamma(alpha2))

    # cek dimensi
    return at.full(size, moment)

# KOMPONEN 5: Quantile
def quantile(p, mu, sigma, alpha1, alpha2):
    # hitung nilai logaritma natural beta(alpha1, alpha2)
    betaln_val = np_gammaln(alpha1) + np_gammaln(alpha2) - np_gammaln(alpha1 + alpha2)

    # hitung logaritma natural omega
    lomega = (
        -0.5 * np.log(2 * at.pi)
        + betaln_val
        - alpha2 * (np.log(alpha2) - np.log(alpha1))
        + (alpha1 + alpha2) * np.log1p(alpha2 / alpha1))

    # nilai omega
    omega = np.exp(lomega)

    ib = betaincinv(alpha1, alpha2, p)
    s = (1 / ib) - 1
    quantile_value = mu - (sigma / omega) * (alpha2 / alpha1) * np.log(s)
    return quantile_value

class GMSNBurr(pm.Continuous):
    """Distribusi GMSNBurr (Generalized Modified to be Stable as Normal from Burr)
       Custom Distribution PyMC"""

    def __init__(self, mu, sigma, alpha1, alpha2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mu = at.as_tensor_variable(mu)
        self.sigma = at.as_tensor_variable(sigma)
        self.alpha1 = at.as_tensor_variable(alpha1)
        self.alpha2 = at.as_tensor_variable(alpha2)

    @staticmethod
    def main(name: str, mu, sigma, alpha1, alpha2, observed=None, **kwargs):
        """Membuat distribusi dengan nama tertentu untuk model PyMC"""
        return pm.CustomDist(
            name, mu, sigma, alpha1, alpha2, 
            logp=logp, logcdf=logcdf, random=random, observed=observed,
            **kwargs,
        )

    @staticmethod
    def dist(mu, sigma, alpha1, alpha2, **kwargs):
        """Mendefinisikan distribusi tanpa nama dalam PyMC"""
        return pm.CustomDist.dist(
            mu, sigma, alpha1, alpha2, 
            logp=logp, logcdf=logcdf, random=random,
            **kwargs,
        )

    @staticmethod
    def moment(rv, size, mu, sigma, alpha1, alpha2):
        """Menghitung nilai moment pertama distribusi"""
        return moment(rv, size, mu, sigma, alpha1, alpha2)

    @staticmethod
    def quantile(q, mu, sigma, alpha1, alpha2):
        """Menghitung kuantil dari distribusi"""
        return quantile(q, mu, sigma, alpha1, alpha2)
