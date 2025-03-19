from .distribution import GMSNBurr
import pymc as pm
import pytensor.tensor as at
import arviz as az
import numpy as np

def compute_logp(value, mu, sigma, alpha1, alpha2, eval=True):
    """Mengembalikan logp sebagai tensor atau nilai numerik langsung."""
    
    # Konversi input menjadi tensor jika perlu
    value, mu, sigma, alpha1, alpha2 = map(at.as_tensor_variable, [value, mu, sigma, alpha1, alpha2])
    
    # Hitung logp
    logp_expr = GMSNBurr.logp(value, mu, sigma, alpha1, alpha2)
    
    return logp_expr.eval() if eval else logp_expr

def get_logp_fn():
    """Mengembalikan fungsi logp yang bisa digunakan langsung dengan angka."""
    
    # Definisi parameter sebagai tensor
    mu = at.scalar('mu')
    sigma = at.scalar('sigma')
    alpha1 = at.scalar('alpha1')
    alpha2 = at.scalar('alpha2')
    value = at.scalar('value')

    # Buat distribusi kustom
    rv = GMSNBurr.dist(mu=mu, sigma=sigma, alpha1=alpha1, alpha2=alpha2)

    # Hitung logp
    rv_logp = pm.logp(rv, value)

    # Kompilasi menjadi fungsi yang bisa langsung dipakai
    return pm.compile([value, mu, sigma, alpha1, alpha2], rv_logp)

def estimate_gmsn_burr_params(data, priors=None, draws=2000, tune=1000, return_trace=True):
    """
    Estimasi parameter distribusi GMSNBurr menggunakan MCMC di PyMC dengan prior yang bisa ditentukan pengguna.

    Parameters:
    - data: array-like
        Data observasi yang digunakan untuk estimasi parameter.
    - priors: dict (default=None)
        Kamus yang menentukan prior untuk setiap parameter.
        Contoh:
        {
            "mu": pm.Normal("mu", mu=0, sigma=10),
            "sigma": pm.HalfNormal("sigma", sigma=5),
            "alpha1": pm.Gamma("alpha1", alpha=2, beta=2),
            "alpha2": pm.Gamma("alpha2", alpha=2, beta=2)
        }
    - draws: int (default=2000)
        Jumlah sampel yang akan diambil dari distribusi posterior.
    - tune: int (default=1000)
        Jumlah iterasi tuning (warm-up) sebelum pengambilan sampel.
    - return_trace: bool (default=True)
        Jika True, mengembalikan hasil trace dari sampling.

    Returns:
    - trace: arviz.InferenceData
        Hasil sampling parameter dalam bentuk trace (jika return_trace=True).
    - summary: pandas.DataFrame
        Ringkasan statistik hasil estimasi parameter.
    """

    with pm.Model() as model:
        # Gunakan prior dari pengguna jika diberikan, jika tidak pakai prior default
        mu = priors.get("mu", pm.Normal("mu", mu=0, sigma=10))
        sigma = priors.get("sigma", pm.HalfNormal("sigma", sigma=5))
        alpha1 = priors.get("alpha1", pm.Gamma("alpha1", alpha=2, beta=2))
        alpha2 = priors.get("alpha2", pm.Gamma("alpha2", alpha=2, beta=2))

        # Likelihood menggunakan distribusi kustom GMSNBurr
        likelihood = GMSNBurr("obs", mu=mu, sigma=sigma, alpha1=alpha1, alpha2=alpha2, observed=data)

        # Sampling dengan MCMC
        trace = pm.sample(draws=draws, tune=tune, return_inferencedata=True)

    # Ringkasan hasil estimasi
    summary = az.summary(trace)

    if return_trace:
        return trace, summary
    return summary
