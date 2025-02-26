import numpy as np
import math
import matplotlib.pyplot as plt

try:
    from HHO.CECData import CEC
except:
    from CECData import CEC

def levy_flight(dim):
    beta = 1.5
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) /
             (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    u = 0.01 * np.random.randn(dim) * sigma
    v = np.random.randn(dim)
    step = u / (np.abs(v) ** (1 / beta))
    return step

class HHO:
    def __init__(self, obj_function, dim, lb, ub, num_hawks=30, max_iter=100):
        self.obj_function = obj_function
        self.dim = dim
        self.lb = np.array(lb)
        self.ub = np.array(ub)
        self.num_hawks = num_hawks
        self.max_iter = max_iter
        
        # 初始化獵鷹位置
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
            
            E0 = 2 * np.random.rand() - 1  # 初始逃脫能量
            for i in range(self.num_hawks):
                E = 2 * E0 * (1 - (t / self.max_iter))  # 能量衰減
                r = np.random.rand()
                J = 2 * (1 - np.random.rand())
                LF = levy_flight(self.dim)
                
                if abs(E) >= 1:
                    if r >= 0.5:
                        X_rand = self.hawks[np.random.randint(self.num_hawks)]
                        self.hawks[i] = X_rand - r * np.abs(X_rand - 2 * r * self.hawks[i])
                    else:
                        self.hawks[i] = self.best_position - np.mean(self.hawks, axis=0) - r * (self.lb + r * (self.ub - self.lb))
                else:
                    delta_X = self.best_position - self.hawks[i]
                    if r >= 0.5 and abs(E) >= 0.5:
                        self.hawks[i] = delta_X - E * np.abs(J * self.best_position - self.hawks[i])
                    elif r >= 0.5 and abs(E) < 0.5:
                        self.hawks[i] = self.best_position - E * np.abs(delta_X)
                    elif r < 0.5 and abs(E) >= 0.5:
                        Y = self.best_position - E * np.abs(J * self.best_position - self.hawks[i])
                        Z = Y + np.random.rand(self.dim) * LF
                        self.hawks[i] = Z if self.obj_function(Z) < self.obj_function(Y) else Y
                    elif r < 0.5 and abs(E) < 0.5:
                        Y = self.best_position - E * np.abs(J * self.best_position - np.mean(self.hawks, axis=0))
                        Z = Y + np.random.rand(self.dim) * LF
                        self.hawks[i] = Z if self.obj_function(Z) < self.obj_function(Y) else Y
                
                # 確保邊界限制
                self.hawks[i] = np.clip(self.hawks[i], self.lb, self.ub)
            
            convergence_curve.append(self.best_score)
        
        return self.best_position, self.best_score, convergence_curve

class HHOCONTROL:
    def __init__(self, MAX_ITER, NUM_WOLVES, YEAR, FUNCTION):
        self.MAX_ITER = MAX_ITER
        self.NUM_HAWKS = NUM_WOLVES
        self.YEAR = YEAR

        self.UB = FUNCTION.ub
        self.LB = FUNCTION.lb
        self.DIM = FUNCTION.dim
        self.f = FUNCTION.func
        self.f_type = FUNCTION.f_type
    
    def Start(self):
        hho = HHO(obj_function=self.f, dim=self.DIM, lb=self.LB, ub=self.UB, 
                  num_hawks=self.NUM_HAWKS, max_iter=self.MAX_ITER)
        best_position, best_value, curve = hho.optimize()
        
        return (best_position, best_value, np.log10(curve))

if __name__ == '__main__':
    MAX_ITER = 500
    NUM_HAWKS = 30
    DIM = 10
    YEAR = "2021"
    FUNCTION_NAME = "F3"
    
    function = CEC(YEAR, FUNCTION_NAME, DIM).get_function_info()
    UB = function.ub
    LB = function.lb
    f = function.func
    
    hho = HHO(obj_function=f, dim=DIM, lb=LB, ub=UB, num_hawks=NUM_HAWKS, max_iter=MAX_ITER)
    best_position, best_value, curve = hho.optimize()
    
    print(f"[CEC {YEAR}-{FUNCTION_NAME}] Best solution found:", best_position)
    print(f"[CEC {YEAR}-{FUNCTION_NAME}] Best fitness:", best_value)
    
    plt.plot(np.log10(curve))
    plt.xlabel("Iterations")
    plt.ylabel("Fitness Value (Log10)")
    plt.title(f"HHO Convergence {YEAR}-{FUNCTION_NAME}-{DIM}D")
    plt.show()
