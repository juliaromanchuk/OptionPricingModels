from math import log, sqrt, exp, pi
from scipy import stats
import pandas as pd

## Option Greeks for non-dividend paying stock
## The Greeks measure the sensitivity of the value of a derivative or a portfolio to changes in parameter value(s)
#  while holding the other parameters fixed.


class Greeks(object):
    def __init__(self, S0, K, T, r, sigma):
        self.S0 = S0            # initial stock price
        self.K = K              # strike price
        self.r = r              # annualized risk-free interest rate, continuously compounded
        self.T = T              # time to expiration
        self.sigma = sigma      # the volatility of returns of the option-pricing model

    def get_d1(self):
        d1 = ((log(self.S0 / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T)))
        return d1

    def get_d2(self):
        d1 = self.get_d1()
        d2 = d1 - self.sigma*sqrt(self.T)
        return d2

    def get_nd1(self):
        d1 = self.get_d1()
        n_d1 = (1/sqrt(2*pi)) * exp(-(d1 ** 2)/2)
        return n_d1
# N(d1)is the cumulative distribution function of the standard normal distribution
    def calculate_call_delta(self):
        d1 = self.get_d1()
        call_delta = stats.norm.cdf(d1)
        return call_delta

    def calculate_put_delta(self):
        d1 = self.get_d1()
        put_delta = stats.norm.cdf(d1) - 1
        return put_delta
## Gamma is the same for puts and calls

    def calculate_gamma(self):
        n_d1 = self.get_nd1()
        gamma = n_d1/(self.S0 * self.sigma * sqrt(self.T))
        return gamma

## Vega is the same for puts and calls

    def calculate_vega(self):
        n_d1 = self.get_nd1()
        vega = self.S0 * n_d1 * sqrt(self.T)
        return vega


    def calculate_call_rho(self):
        d2 = self.get_d2()
        nd2 = stats.norm.cdf(d2)
        call_rho = self.K * self.T * exp(-self.r * self.T) * nd2
        return call_rho

    def calculate_put_rho(self):
        d2 = self.get_d2()
        nd2 = stats.norm.cdf(-d2)
        put_rho = -self.K * self.T * exp(-self.r * self.T) * nd2
        return put_rho

    def calculate_call_theta(self):
        d2 = self.get_d2()
        nd2 = stats.norm.cdf(d2)
        n_d1 = self.get_nd1()
        call_theta = (-self.S0 * n_d1 * self.sigma/2 * sqrt(self.T)) - self.r * self.K * exp(- self.r * self.T) * nd2
        return call_theta

    def calculate_put_theta(self):
        d2 = self.get_d2()
        nd2 = stats.norm.cdf(-d2)
        n_d1 = self.get_nd1()
        put_theta = (-self.S0 * n_d1 * self.sigma/2 * sqrt(self.T)) + self.r * self.K * exp(- self.r * self.T) * nd2
        return put_theta


x = Greeks(0.80, 0.81, 0.5833, 0.03, 0.15)

call_delta = x.calculate_call_delta()
call_theta = x.calculate_call_theta()
call_vega = x.calculate_vega()
call_gamma = x.calculate_gamma()
call_rho = x.calculate_call_rho()

put_delta = x.calculate_put_delta()
put_theta = x.calculate_put_theta()
put_rho = x.calculate_put_rho()
put_vega = x.calculate_vega()
put_gamma = x.calculate_gamma()

## define a function to show option greeks for both put and call with the same initial parameters as a data frame

def show_option_greeks():
    indexes = pd.Series(["Delta", "Theta", "Gammma", "Vega", "Rho"])
    data = [[call_delta, put_delta], [call_theta, put_theta], [call_gamma, put_gamma],
            [call_vega, put_vega], [call_rho, put_rho]]
    greeks = pd.DataFrame(data, index=indexes, columns=["Call", "Put"])
    print greeks


show_option_greeks()
