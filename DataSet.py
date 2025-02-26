import opfunu as of
import scipy.io as sio
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.model_selection import train_test_split
import sklearn

class DataSet:
    funcs_years= {
        "CEC":{
            "2021": ["F3", "F4", "F6", "F7", "F8", "F9", "F10"],
            "2022": ["F2", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
        },
        "gene":{
            
        }
    }
    NN_K = 12

    def __init__(self):

        self.all_funcs= {"CEC":self.get_CEC_data_dict(),
                        "GENE":self.get_GENE_data_dict()}

    def get_function(I,II,III,dim):
        if I == "CEC":
            return CECFUNC(II,III,dim).get_function_info()
        elif I == "GENE":
            return GENEFUNC(III,dim).get_function_info()
        


    def get_CEC_data_dict(self):
        CEC_DICT = {}
        directI = of.cec_based.__dict__
        for year in directI.keys():
            year_dict = {}
            if(year[0]=='c' and year!='cec'):
                directII = directI[year].__dict__
                for func in directII.keys():
                    func_list=[]
                    if(func[0]=='F'):
                        directIII = directII[func]
                        diml = directIII().dim_supported
                        if type(diml) is not list:
                            continue
                        for dim in diml:
                            func_list.append(str(dim))
                        
                        if len(func_list)>0:
                            year_dict.update({func[0:-4:1]:func_list})
                if len(year_dict)>0:
                    CEC_DICT.update({year[-4:]:year_dict})
        return CEC_DICT
    
    def get_GENE_data_dict(self):
        return {
            "1.  ALLAML":7129,
            "2.  BreatEW_data":31,
            "3.  colon":2000,
            "4.  HeartEW_data":14,
            "5.  Leukemia_1":5327,
            "6.  Leukemia_2":7129,
            "7.  Leukemia_3":11225,
            "8.  Leukemia":3312,
            "9.  lung_discrete":325,
            "10. lung":3312,
            "11. lymphoma":4026,
        }
        

class CECFUNC:
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
    
class GENEFUNC:
    def __init__(self,name,dim):
        self.name = name[4:]
        self.dim = dim
        self.data = sio.loadmat(f'_geneData/{self.name}.mat')['X']
        self.labels = sio.loadmat(f'_geneData/{self.name}.mat')['Y']
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.data, self.labels, test_size=0.2, random_state=42)
        self.Y_test = self.Y_test.ravel()
        self.Y_train = self.Y_train.ravel()

    def get_function_info(self):
        return function_struct(self.func,self.dim,np.max(self.data,axis=0),np.min(self.data,axis=0),"d")
    
    

    def func(self,x):
        """ 
        間單來說就是優化每個特徵的參數，
        然後把這個參數帶入到資料後用KNN演算法驗證，
        計算準確率來當作適應函數 
        """
        weights = x[:-1]
        k = int(round(x[-1]))

        k = max(1, min(20, k))

        X_train_weighted = self.X_train * weights
        X_test_weighted = self.X_test * weights

        knn = KNN(n_neighbors=k)
        knn.fit(X_train_weighted, self.Y_train)
        
        accuracy = knn.score(X_test_weighted, self.Y_test)
        return 1/accuracy  


class function_struct:
    def __init__(self,func,dim,lb,ub,function_type):
        self.func = func
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.f_type =  function_type


DataSet().get_GENE_data_dict