# [[file:../class.org::result_class][result_class]]
# Tangled on Fri Mar 15 06:05:36 2024
import numpy as np
import pandas as pd
import warnings
import torch

import cvxpy as cp
from osmm import OSMM
osmm_prob = OSMM()

from .root_with_precision import root_with_precision

class OracleDemands(object):

    """Objects of this class describe demands for a given utility function.

    The supplied utility function is assumed to be increasing,
    concave, and continuously differentiable.  It must map a vector (a
    =pytorch.tensor=) into a float, but otherwise can have any desired structure. 

    There are three fundamental representations of demand described:
       - Marshallian (demands depend on prices & budget)
       - Hicksian (demands depend on prices and a level of utility)
       - Frischian (demands depend on prices and a marginal utility of expenditures (MUE).    
    """

    def __init__(self, utility, tol=1e-12, verbose=False,**kwargs):
        """Supply a function which maps a vector represented as a
        =torch.tensor= into a float, say U(c).
        """

        self.utility = utility
        self.verbose = verbose
        self.tol = tol

    def _frischian_demands(self,p,lbda):
        """Compute Frischian demands."""

        assert lbda>0,"lambda must be positive."

        osmm_prob.f_torch.function = lambda c: -self.utility(c)

        p = np.array(p)
        c = cp.Variable(len(p), nonneg=True)

        osmm_prob.g_cvxpy.variable = c
        osmm_prob.g_cvxpy.objective = lbda*p@c
        osmm_prob.g_cvxpy.constraints = []

        guess = 1/(lbda*p)

        result = osmm_prob.solve(guess,verbose=self.verbose,eps_gap_abs=self.tol)

        return c.value

    def _marshallian_demands(self,p,x):
        """Compute Marshallian demands."""

        assert x>0,"budget must be positive."

        osmm_prob.f_torch.function = lambda c: -self.utility(c)

        p = np.array(p)
        c = cp.Variable(len(p), nonneg=True)

        osmm_prob.g_cvxpy.variable = c
        osmm_prob.g_cvxpy.objective = 0
        osmm_prob.g_cvxpy.constraints = [p@c==x]

        guess = x/(len(p)*p)

        result = osmm_prob.solve(guess,verbose=self.verbose,eps_gap_abs=self.tol)

        #print("Result:",result)

        assert c.value is not None

        return c.value

    def _hicksian_demands(self,p,U):
        """Compute Hicksian demands."""

        def _sum(x,y):
            S = 0
            for i in range(len(x)):
                S += x[i]*y[i]

            return S

        osmm_prob.f_torch.function = lambda c: _sum(c,p)

        c = cp.Variable(len(p), nonneg=True)

        osmm_prob.g_cvxpy.variable = c
        osmm_prob.g_cvxpy.objective = 0
        osmm_prob.g_cvxpy.constraints = [-self.utility(c)<=-U]

        guess = np.ones(len(p))

        result = osmm_prob.solve(guess,verbose=self.verbose,eps_gap_abs=self.tol)

        print("Result:",result)

        assert c.value is not None

        return c.value

    def _frischian_V(self,p,lbda):
        """Frischian indirect utility."""
        c = self._frischian_demands(p,lbda)
        return self.utility(c)

    def _marshallian_V(self,p,x):
        """Marshallian indirect utility."""
        c = self._marshallian_demands(p,x)
        return self.utility(c)

    def _frischian_x(self,p,lbda):
        """Frischian expenditures."""
        return p@self._frischian_demands(p,lbda)
# result_class ends here

# [[file:../class.org::*Methods describing the utility function][Methods describing the utility function:1]]
# Tangled on Fri Mar 15 06:05:36 2024
    def marginal_utilities(self,c):

        # Compute gradient
        x = torch.tensor(c,requires_grad=True,dtype=torch.float)

        return torch.autograd.functional.jacobian(self.utility,x)

    def hessian_utility(self,c):

        # Compute gradient
        x = torch.tensor(c,requires_grad=True,dtype=torch.float)

        return torch.autograd.functional.hessian(self.utility,x)
# Methods describing the utility function:1 ends here

# [[file:../class.org::*Methods describing demands and their primitives][Methods describing demands and their primitives:1]]
# Tangled on Fri Mar 15 06:05:36 2024
    def lambdavalue(self,p,x=None,U=None,ub=10,tol=1e-12):
        """
        Given expenditures x, prices p return the MUE, lambda(p,x);
        *or* if given level of utility U return lambda(p,U)
        """
        def excess_expenditures(p,x):
            def f(lbda):
                """"Difference in expenditures p@f(lbda,p)-x"""
                #lbda = np.abs(lbda)
                c = self._frischian_demands(p,lbda)
                return p@c-x

            return f

        def excess_utility(p,U):
            def f(lbda):
                """"Difference in expenditures p@f(lbda,p)-x"""
                #lbda = np.abs(lbda)
                V = self._frischian_V(p,lbda)
                return V-U
            return f

        assert not ((x is None)*(U is None)), "Must supply either x or U."

        if x is not None:
            return root_with_precision(excess_expenditures(p,x),[0,ub,np.Inf],tol,open_interval=True)
        elif U is not None:
            return root_with_precision(excess_utility(p,U),[0,ub,np.Inf],tol,open_interval=True)

     
    def demands(self,p,x=None,U=None,lbda=None):
        """
        Demands at prices p, given one of
          - x (Marshallian)
          - U (Hicksian)
          - lbda (Frischian)
        """
        assert ((x is None) + (U is None) + (lbda is None))==2, "Specify one of x,U,lbda."

        if lbda is not None:
            return self._frischian_demands(p,lbda)
        elif x is not None:
            return self._marshallian_demands(p,x)
        elif U is not None:
            try:
                return self._hicksian_demands(p,U)
            except AssertionError:
                lbda = self.lambdavalue(p,U=U)
                return self._frischian_demands(p,lbda)

    def indirect_utility(self,p,x=None,U=None,lbda=None):
        """
        Indirect utility at prices p, given one of
          - x (Marshallian)
          - U (Hicksian)
          - lbda (Frischian)
        """
        assert ((x is None) + (U is None) + (lbda is None))==2, "Specify one of x,U,lbda."

        if lbda is not None:
            return self._frischian_V(p,lbda)
        elif x is not None:
            return self._marshallian_V(p,x)
        elif U is not None:
            return U

    V = indirect_utility

    def expenditures(self,p,x=None,U=None,lbda=None):
        """
        Expenditures at prices p, given one of
          - x (Marshallian)
          - U (Hicksian)
          - lbda (Frischian)
        """
        assert ((x is None) + (U is None) + (lbda is None))==2, "Specify one of x,U,lbda."

        if lbda is not None:
            return self._frischian_x(p,lbda)
        elif x is not None:
            return x
        elif U is not None:
            return p@self.demands(p,U=U)
# Methods describing demands and their primitives:1 ends here
