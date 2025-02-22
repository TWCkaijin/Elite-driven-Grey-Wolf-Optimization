import opfunu as of


class CEC:
    def __init__(self,year,function_name,dim):
        self.dim = dim
        self.func = of.get_functions_by_classname(function_name+year)[0](ndim = self.dim)
        if self.func is None:
            raise ValueError("Function not found")    
    
    def get_function_info(self):
        return functions(self.cec_func,self.dim,self.func.lb.tolist(),self.func.ub.tolist())

    def cec_func(self,x):
        F = self.func.evaluate(x)
        return F
    

class functions:
    def __init__(self,func,dim,lb,ub):
        self.func = func
        self.dim = dim
        self.lb = lb
        self.ub = ub
