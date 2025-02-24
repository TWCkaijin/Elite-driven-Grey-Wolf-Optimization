import numpy as np
import matplotlib.pyplot as plt

from DataSet import DataSet

class HHO:
    def __init__(self, obj_function, dim, lb, ub, num_hawks=30, max_iter=100):
        self.obj_function = obj_function
        self.dim = dim
        self.lb = np.array(lb)
        self.ub = np.array(ub)
        self.num_hawks = num_hawks
        self.max_iter = max_iter
        
        # 初始化獵鷹群位置
        self.hawks = np.random.uniform(self.lb, self.ub, (self.num_hawks, self.dim))
        self.best_position = None
        self.best_score = np.inf
    
    def optimize(self):
        convergence_curve = []
        for t in range(self.max_iter):
            
            # 計算適應度並找出最好的解（獵物）
            for i in range(self.num_hawks):
                fitness = self.obj_function(self.hawks[i])
                if fitness < self.best_score:
                    self.best_score = fitness
                    self.best_position = self.hawks[i].copy()
                    
            # 更新位置
            E1 = 2 * (1 - (t / self.max_iter))  # 能量下降因子
            
            for i in range(self.num_hawks):
                E = 2 * E1 * np.random.rand() - E1  # 獵物逃跑能量
                q = np.random.rand()  # 隨機機率
                r = np.random.rand(self.dim)  # 隨機向量
                
                if abs(E) >= 1:  # exploration
                    X_rand = self.hawks[np.random.randint(self.num_hawks)]  # 隨機選擇獵鷹
                    self.hawks[i] = X_rand - r * abs(X_rand - 2 * np.random.rand() * self.hawks[i])
                else:  # exploitation
                    if q >= 0.5:
                        self.hawks[i] = self.best_position - E * abs(self.best_position - self.hawks[i])
                    else:
                        delta_X = abs(self.best_position - self.hawks[i])
                        self.hawks[i] = delta_X * np.exp(-E * t) * np.cos(2 * np.pi * r) + self.best_position
                
                # 確保邊界限制
                self.hawks[i] = np.clip(self.hawks[i], self.lb, self.ub)
            
            convergence_curve.append(self.best_score)
            
        return self.best_position, self.best_score, convergence_curve, self.hawks


class HHOCONTROL:
    def __init__(self, MAX_ITER, NUM_HAWKS, YEAR, FUNCTION):
        self.MAX_ITER = MAX_ITER
        self.NUM_HAWKS = NUM_HAWKS
        self.YEAR = YEAR

        self.UB = FUNCTION.ub
        self.LB = FUNCTION.lb
        self.DIM = FUNCTION.dim
        self.f = FUNCTION.func
        self.f_type = FUNCTION.f_type
    
    def Start(self):
        hho = HHO(obj_function=self.f, dim=self.DIM, lb=self.LB, ub=self.UB, 
                  num_hawks=self.NUM_HAWKS, max_iter=self.MAX_ITER)
        best_position, best_value, curve, hawks = hho.optimize()
        
        return (hawks, np.log10(curve))


if __name__ == '__main__':

    funcs_by_year = DataSet.funcs_years
    
    MAX_ITER = 500
    NUM_HAWKS = 30
    DIM = 10
    
    for year in funcs_by_year['CEC']:
        for func_name in funcs_by_year['CEC'][year]:
            function = DataSet.get_function(year,func_name,DIM)
            UB = function.ub
            LB = function.lb
            f = function.func # 取得函式
            # 計算函式值 f([多個維度組成的陣列])   -> 例如 f([x,y])
            
            # 執行 HHO
            hho = HHO(obj_function=f, dim=DIM, lb=LB, ub=UB, num_hawks=NUM_HAWKS, max_iter=MAX_ITER)
            best_position, best_value, curve = hho.optimize()
            
            print(f"[CEC {year}-{func_name}] Best solution found:", best_position)
            print(f"[CEC {year}-{func_name}] Best fitness:", best_value)
            
            # 繪製收斂曲線
            plt.plot(np.log10(curve))
            plt.xlabel("Iterations")
            plt.ylabel("Fitness Value (Log10)")
            plt.title(f"HHO Convergence {year}-{func_name}-{DIM}D")
            plt.show()
