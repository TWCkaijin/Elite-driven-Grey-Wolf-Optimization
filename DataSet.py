import opfunu as of


class DataSet:
    funcs_years= {
        "CEC":{
            "2021": ["F3", "F4", "F6", "F7", "F8", "F9", "F10"],
            "2022": ["F2", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
        },
        "gene":{
            
        }
    }

    def get_function(year,function_name,dim):
        return function_generate(year,function_name,dim).get_function_info()

class function_generate:
    def __init__(self,year,function_name,dim):
        self.dim = dim
        self.source = of.get_functions_by_classname(function_name+year)[0](ndim = self.dim)
        if self.source is None:
            raise ValueError("Function not found")    
    
    def get_function_info(self):
        return function_struct(self.func,self.dim,self.source.lb.tolist(),self.source.ub.tolist(),"continue")

    def func(self,x):
        F = self.source.evaluate(x)
        return F

class function_struct:
    def __init__(self,func,dim,lb,ub,function_type):
        self.func = func
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.f_type =  function_type