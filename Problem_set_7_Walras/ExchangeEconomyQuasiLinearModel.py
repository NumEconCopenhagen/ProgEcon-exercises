from types import SimpleNamespace
import numpy as np
from scipy import optimize
from ExchangeEconomyModel import ExchangeEconomyModelClass

class ExchangeEconomyModelQuasiLinearClass(ExchangeEconomyModelClass):

    # uA(x1A,x2A) = ln(x1A) + alpha*x2A
    # uB(x1B,x2B) = ln(x1B) + beta*x2B

    ######################
    # utility and demand # 
    ######################

    def utility_A(self,x1A,x2A):
        """
        Utility function for agent A.
        """        

        raise NotImplementedError("This method is not implemented yet.")
    
    def x2A_indifference(self,uA,x1A):

        raise NotImplementedError("This method is not implemented yet.")
    
    def utility_B(self,x1B,x2B):
        """
        Utility function for agent B.
        """

        raise NotImplementedError("This method is not implemented yet.")
    
    def x2B_indifference(self,uB,x1B):

        raise NotImplementedError("This method is not implemented yet.")

    def demand_A(self,p1):
        """
        Demand for good 1 and 2 for agent A.
        """

        raise NotImplementedError("This method is not implemented yet.")
    
    def demand_B(self,p1):
        """
        Demand for good 1 and 2 for agent B.
        """

        raise NotImplementedError("This method is not implemented yet.")
        
    def solve_dictator_B(self):
        """ 
        Solve the dictator problem for agent A.
        """

        raise NotImplementedError("This method is not implemented yet.")
            