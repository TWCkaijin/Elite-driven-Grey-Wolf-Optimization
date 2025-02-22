import opfunu as of

class CEC:
    def __init__(self,year,function_name,dim):
        self.dim = dim
        self.func = of.get_functions_by_classname(function_name+year)[0](ndim = self.dim)
        
        if dim not in [2,10,20]:
            raise ValueError("Dimension must be in [2,10,20]")
        if function_name not in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
            raise ValueError("Function name must be in [F1~F12]") 
        
        
    
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
        
    

