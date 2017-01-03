import numpy as np
import matplotlib.pyplot as plot


class ESS:
    def __init__(self, payoff_matrix, strategies):
        """
        Payoff Matrix is in form
        [ [(pi1(S1, S1), pi2(S1, S1)), (pi1(S1, S2), pi2(S1, S2))],
          [(pi1(S2, S1), pi2(S2, S1)), (pi1(S2, S2), pi2(S2, S2))] ]
        Strategies is in form
        (strategy1, strategy2)
        """
        self.matrix = payoff_matrix
        self.strategies = strategies
    
    def utility(self, stratindex):
        return lambda x: x*self.matrix[stratindex][0][0] + (1-x)*self.matrix[stratindex][1][0]
        
    def averageutility(self):
        return lambda x: x*self.utility(0)(x) + (1-x)*self.utility(1)(x)

    def roc(self, strategy):
        stratindex = self.strategies.index(strategy)
        if stratindex == 0:
            return lambda x: x*(self.utility(stratindex)(x) - self.averageutility()(x))
        if stratindex == 1:
            return lambda x: (1-x)*(self.utility(stratindex)(x) - self.averageutility()(x))

    def plotroc(self, strategy):
        print("R.O.C. for " + strategy)
        x = [i/100.0 for i in range(100)]
        y = [self.roc(strategy)(i) for i in x]
        plot.plot(x, y, 'r', linewidth=2.0)
        plot.axhline(linewidth=4, color='k')
        plot.show()
