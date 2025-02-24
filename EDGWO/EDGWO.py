import numpy as np
import matplotlib.pyplot as plt
from DataSet import DataSet

class EDGWO:
    def __init__(self, obj_function, dim, lb, ub, num_wolves=10, max_iter=100):
        self.obj_function = obj_function  # 目標函數
        self.dim = dim                    # 變數維度
        self.lb = np.array(lb)            # 下界
        self.ub = np.array(ub)            # 上界
        self.num_wolves = num_wolves      # 狼群數量
        self.max_iter = max_iter          # 最大迭代次數

        # 初始化狼群位置
        self.wolves = np.random.uniform(self.lb, self.ub, (self.num_wolves, self.dim))
        self.alpha, self.beta, self.delta = np.random.uniform(self.lb, self.ub, self.dim),np.random.uniform(self.lb, self.ub, self.dim),np.random.uniform(self.lb, self.ub, self.dim)
        self.alpha_score, self.beta_score, self.delta_score = np.inf, np.inf, np.inf

    def VectorComponentCalculation(self, a, index, Xm, targetlead):
        r1, r2 = np.random.rand(), np.random.rand()
        A, C = 2 * a * r1 - a, 2 * r2

        if(A<1):
            D = abs(C * targetlead - self.wolves[index])
            return targetlead - A * D
        else:
            r3, r4 = np.random.rand(), np.random.rand()
            return targetlead - Xm - r3 * (self.lb + (self.ub-self.lb) * r4)
            #return self.alpha - Xm - r3 * (self.lb + (self.ub-self.lb) * r4)
        

    def optimize(self):
        convergence_curve = []
        for t in range(self.max_iter):
            # 計算適應度並更新
            mean_pos = np.mean(self.wolves, axis=0)
            for i in range(self.num_wolves):
                fitness = self.obj_function(self.wolves[i])
                if fitness < self.alpha_score:
                    self.delta_score, self.delta = self.beta_score, self.beta.copy()
                    self.beta_score, self.beta = self.alpha_score, self.alpha.copy()
                    self.alpha_score, self.alpha = fitness, self.wolves[i].copy()
                elif fitness < self.beta_score:
                    self.delta_score, self.delta = self.beta_score, self.beta.copy()
                    self.beta_score, self.beta = fitness, self.wolves[i].copy()
                elif fitness < self.delta_score:
                    self.delta_score, self.delta = fitness, self.wolves[i].copy()
            # 更新狼群位置
            a = 2 - t * (2 / self.max_iter)  # 動態調整 a
            for i in range(self.num_wolves):

                """ # calcu;ating X1
                r1, r2 = np.random.rand(), np.random.rand()
                A1, C1 = 2 * a * r1 - a, 2 * r2
                D_alpha = abs(C1 * self.alpha - self.wolves[i])
                X1 = self.alpha - A1 * D_alpha """
                X1 = self.VectorComponentCalculation(a, index=i, Xm=mean_pos, targetlead=self.alpha)


                """ # calculating X2
                r1, r2 = np.random.rand(), np.random.rand()
                A2, C2 = 2 * a * r1 - a, 2 * r2
                D_beta = abs(C2 * self.beta - self.wolves[i])
                X2 = self.beta - A2 * D_beta """
                X2 = self.VectorComponentCalculation(a, index=i, Xm=mean_pos, targetlead=self.beta)

                """ # calculating X3
                r1, r2 = np.random.rand(), np.random.rand()
                A3, C3 = 2 * a * r1 - a, 2 * r2
                D_delta = abs(C3 * self.delta - self.wolves[i])
                X3 = self.delta - A3 * D_delta """
                X3 = self.VectorComponentCalculation(a, index=i, Xm=mean_pos, targetlead=self.delta)


                if np.random.rand() < (0.5 * (1 - t/self.max_iter)):
                    self.wolves[i] = (X1 + X2 + X3) / 3
                else:
                    r5 = np.random.rand()
                    l = -1+2*r5
                    self.wolves[i] = self.alpha + np.linalg.norm(self.alpha-self.wolves[i])*np.exp(l)*np.cos(2*np.pi*l)

                # 限制範圍
                self.wolves[i] = np.clip(self.wolves[i], self.lb, self.ub)

            convergence_curve.append(self.alpha_score)
        return self.alpha, self.alpha_score, convergence_curve, self.wolves
    

class EDGWOCONTROL:
    def __init__(self,MAX_ITER, NUM_WOLVES, YEAR, FUNCTION_NAME, DIM):
        self.MAX_ITER = MAX_ITER
        self.NUM_WOLVES = NUM_WOLVES
        self.YEAR = YEAR
        self.FUNCTION_NAME = FUNCTION_NAME
        self.DIM = DIM
        
        function = DataSet.get_function(self.YEAR, self.FUNCTION_NAME, self.DIM)  # 取得CEC Year年度，維度為 DIM 之 F1 函式的資訊
        
        self.UB = function.ub
        self.LB = function.lb
        #print(f"UB: {self.UB} || LB: {self.LB}")
        self.dim= function.dim
        self.f = function.func

    def info(self):
        return f"ED-GWO Convergence {self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D"

    def Start(self):
        gwo = EDGWO(obj_function=self.f, dim=self.DIM, lb=self.LB, ub=self.UB, 
                    num_wolves=self.NUM_WOLVES, max_iter=self.MAX_ITER)
        best_position, best_value, curve, wolves = gwo.optimize()
        
        """ print("Best solution found:", best_position)
        print("Best fitness:", best_value) """

        return (wolves, np.log10(curve))




if __name__ == '__main__':

    funcs_by_year = DataSet.funcs_years

    # 設定參數
    MAX_ITER = 500
    NUM_WOLVES = 30
    DIM = 10

    # CEC 函式呼叫方法  
    for year in funcs_by_year:
        for func_name in funcs_by_year[year]:
            function = DataSet.get_function(year,func_name,DIM) # 取得CEC Year年度，維度為 DIM 之 F1 函式的資訊
            UB = function.ub
            LB = function.lb
            f = function.func # 取得函式
            # 計算函式值 f([多個維度組成的陣列])   -> 例如 f([x,y])

    
            # 執行 GWO
            gwo = EDGWO(obj_function=f, dim=DIM, lb=LB, ub=UB, num_wolves=NUM_WOLVES, max_iter=MAX_ITER)
            best_position, best_value, curve = gwo.optimize()

            print(f"[CEC {year}-{func_name}] Best solution found:", best_position)
            print(f"[CEC {year}-{func_name}] Best fitness:", best_value)

            # 繪製收斂曲線
            plt.plot(np.log10(curve))
            plt.xlabel("Iterations")
            plt.ylabel("Fitness Value (Log10)")
            plt.title(f"ED-GWO Convergence {year}-{func_name}-{DIM}D")
            plt.show()
