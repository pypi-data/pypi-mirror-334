from .distribution import GMSNBurr
import numpy as np
import pytensor.tensor as at
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
from pytensor.tensor import gammaln, switch, isinf
from scipy.special import betaincinv, gammaln as np_gammaln
from typing import Optional, Tuple

# Check parameters
def check_params(alpha1, alpha2, sigma):
    """
    Checks if the input parameters for the GMSNBurr distribution are valid.

    Parameters:
        sigma (float): Scale parameter (must be > 0)
        alpha1 (float): Shape parameter (must be > 0)
        alpha2 (float): Shape parameter (must be > 0)
    """
    if np.any(alpha1 <= 0):
        raise ValueError("alpha1 must be greater than 0")
    if np.any(alpha2 <= 0):
        raise ValueError("alpha2 must be greater than 0")
    if np.any(sigma <= 0):
        raise ValueError("sigma must be greater than 0")

# Convert into tensor variable
def to_tensor(*args):
    """
    Converts input values into Tensor Variables.
    
    Parameters:
        *args: One or more values to be converted into Tensor Variables.

    Returns:
        list: A list of Tensor Variables containing the input values.
    """
    return [at.as_tensor_variable(arg) for arg in args]

# PDF
def pdf(y, mu, sigma, alpha1, alpha2, log=False):
    """
    Computes the PDF of the GMSNBurr distribution.

    Parameters:
        y (float): Value
        mu (float): Location parameter
        sigma (float): Scale parameter (sigma > 0)
        alpha1 (float): Shape parameter (alpha1 > 0)
        alpha2 (float): Shape parameter (alpha2 > 0)
        log (bool): If True, returns the natural logarithm of the PDF (default = False)

    Returns:
        float: The computed PDF value.
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
    if log:
        lp_val = lp.eval()
    else:
        lp_val = at.exp(lp).eval()
    return lp_val

# CDF
def cdf(y, mu, sigma, alpha1, alpha2, lower_tail=True, log=False):
    """
    Computes the CDF of the GMSNBurr distribution.

    Parameters:
        y (float): Value
        mu (float): Location parameter
        sigma (float): Scale parameter (sigma > 0)
        alpha1 (float): Shape parameter (alpha1 > 0)
        alpha2 (float): Shape parameter (alpha2 > 0)
        lower_tail (bool): If True, computes P(X <= x); if False, computes P(X > x) (default = True)
        log (bool): If True, returns the natural logarithm of the CDF (default = False)

    Returns:
        float: The computed CDF value.
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
        return log_cdf_value.eval()
    else:
        real_cdf_value = cdf_value if lower_tail else 1 - cdf_value
        return real_cdf_value.eval()

# Random
def random(mu: np.ndarray | float, sigma: np.ndarray | float, alpha1: np.ndarray | float, alpha2: np.ndarray | float, rng = np.random.default_rng(), size: Optional[Tuple[int]]=None):
    """
    Generate random samples from the GMSNBurr distribution.

    Parameters:
        mu (float or np.ndarray): Location parameter.
        sigma (float or np.ndarray): Scale parameter (must be > 0).
        alpha1 (float or np.ndarray): Shape parameter (must be > 0).
        alpha2 (float or np.ndarray): Shape parameter (must be > 0).
        rng (np.random.Generator, optional): Random number generator instance (default: np.random.default_rng()).
        size (Tuple[int, ...], optional): Shape of the output array.

    Returns:
        np.ndarray: Random variates from the GMSNBurr distribution.
    """
    check_params(alpha1, alpha2, sigma)
    betaln_val = np_gammaln(alpha1) + np_gammaln(alpha2) - np_gammaln(alpha1 + alpha2)
    lomega = (
        -0.5 * np.log(2 * np.pi)
        + betaln_val
        - alpha2 * (np.log(alpha2) - np.log(alpha1))
        + (alpha1 + alpha2) * np.log1p(alpha2 / alpha1))
    omega = np.exp(lomega)
    z1 = rng.chisquare(2 * alpha1, size=size) / (2 * alpha1)
    z2 = rng.chisquare(2 * alpha2, size=size) / (2 * alpha2)
    logzf = np.log(z2) - np.log(z1)
    random_variate = mu - (sigma / omega) * logzf
    return np.asarray(random_variate)

# Moment
def moment(mu, sigma, alpha1, alpha2, y = None, size = None):
    """
    Compute the moment (expected value) of the GMSNBurr distribution.

    Parameters:
        y (float): Value (not used in the computation).
        size (Tuple[int, ...], optional): Desired shape of the output tensor.
        mu (float): Location parameter.
        sigma (float): Scale parameter (must be > 0).
        alpha1 (float): Shape parameter (must be > 0).
        alpha2 (float): Shape parameter (must be > 0).

    Returns:
        float: The computed expected value.
    """
    check_params(alpha1, alpha2, sigma)
    y, mu, sigma, alpha1, alpha2 = to_tensor(y, mu, sigma, alpha1, alpha2)
    if y is not None:
        size = y.shape
    elif size is None:
        size = (1,) 
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
    """
    Computes the quantile (inverse CDF) of the GMSNBurr distribution.

    Parameters:
        p (float): Probability value(s), must be in (0,1).
        mu (float): Location parameter.
        sigma (float): Scale parameter (must be > 0).
        alpha1 (float): Shape parameter (must be > 0).
        alpha2 (float): Shape parameter (must be > 0).

    Returns:
        float: The quantile corresponding to probability p.
    """
    check_params(alpha1, alpha2, sigma)
    if np.any(p <= 0) or np.any(p >= 1):
        raise ValueError("p must be strictly between 0 and 1")
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

# Show plot GMSNBurr as an example based on the parameters
def example(mu, sigma, alpha1, alpha2):
    range_min, range_max, num_points = -10, 10, 100
    x = np.linspace(mu + range_min, mu + range_max, num_points)
    pdf_example = [pdf(xi, mu, sigma, alpha1, alpha2) for xi in x]
    delta_alpha_pdf = alpha1 - alpha2
    if delta_alpha_pdf > 0:
        legend_loc = "upper right"
    else:
        legend_loc = "upper left"
    with plt.style.context('seaborn-v0_8-bright'):
        plt.figure(figsize=(12,6))
        plt.plot(x, pdf_example, label=f'GMSNBurr({mu}, {sigma}, {alpha1}, {alpha2})', color='steelblue', linewidth=2.0)
        plt.plot([], [], ' ', label=f'\u0394\u03B1 = {delta_alpha_pdf}')
        plt.xlabel("x")
        plt.ylabel("Density")
        plt.legend(loc=legend_loc, fontsize=10)
    plt.show()

# Estimate parameters using PyMC MCMC
def estimate(data, priors=None, draws=2000, tune=1000, chains = 4, cores=4):
    """
    Estimation of GMSNBurr distribution parameters using MCMC in PyMC with user-defined priors.

    Parameters:
    - data: array-like
        Observed data used for parameter estimation.
    - priors: dict (default=None)
        A dictionary specifying the prior for each parameter.
        Example:
        {
            "mu": pm.Normal("mu", mu=0, sigma=10),
            "sigma": pm.HalfCauchy("sigma", beta=5),
            "alpha1": pm.LogNormal("alpha1", mu=2, sigma=2),
            "alpha2": pm.LogNormal("alpha2", mu=2, sigma=2)
        }
    - draws: int (default=2000)
        The number of samples to draw from the posterior distribution.
    - tune: int (default=1000)
        The number of tuning (warm-up) iterations before sampling.
    - chains: int (default=4)
        The number of independent Markov chains to run.
    - cores: int (default=4)
        The number of CPU cores to use for parallelizing the MCMC process.

    Returns:
    - trace: arviz.InferenceData
        The results of the parameter sampling in the form of a trace (if return_trace=True).
    - summary: pandas.DataFrame
        A summary of the statistical results of the parameter estimates.
    """
    with pm.Model() as model:
        mu = priors.get("mu", pm.Normal("mu", mu=0, sigma=5))
        sigma = priors.get("sigma", pm.HalfCauchy("sigma", beta=2))
        alpha1 = priors.get("alpha1", pm.LogNormal("alpha1", mu=0, sigma=0.25))
        alpha2 = priors.get("alpha2", pm.LogNormal("alpha2", mu=0, sigma=0.25))
        likelihood = GMSNBurr("GMSNBurrEstimation", mu=mu, sigma=sigma, alpha1=alpha1, alpha2=alpha2, observed=data)
        traceGMSNBurr = pm.sample(draws=draws, tune=tune, cores=cores, chains=chains, return_inferencedata=True, idata_kwargs={"log_likelihood": True})
        log_evidence = pm.loo(traceGMSNBurr).elpd_loo
    summary = az.summary(traceGMSNBurr, round_to=3, hdi_prob=0.95)
    return traceGMSNBurr, summary