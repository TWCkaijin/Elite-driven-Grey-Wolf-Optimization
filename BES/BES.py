import numpy as np
import matplotlib.pyplot as plt
try:
    from BES.CECData import CEC
except:
    from CECData import CEC

class BES:
    def __init__(self, obj_function, dim, lb, ub, num_par=30, max_iter=100):
        self.obj_function = obj_function
        self.dim = dim
        self.lb = np.array(lb)
        self.ub = np.array(ub)
        self.num_par = num_par
        self.max_iter = max_iter

        # 初始化
        self.particles = np.random.uniform(self.lb, self.ub, (self.num_par, self.dim))
        self.energy = np.ones(self.num_par)  # 初始設定為1
        self.best_position = np.zeros((self.num_par, self.dim))  # 最佳位置
        self.best_energy = np.full(self.num_par, np.inf)  # 最佳能量

        # 最佳解(全局)
        self.gbest_position = np.random.uniform(self.lb, self.ub, self.dim)
        self.gbest_energy = np.inf

    def optimize(self):
        convergence_curve = []

        for t in range(self.max_iter):
            for i in range(self.num_par):
                fitness = self.obj_function(self.particles[i])

                self.energy[i] = 1 / (fitness + 1e-10) # 確保分母不為0

                # 最佳位置
                if self.energy[i] < self.best_energy[i]:
                    self.best_energy[i] = self.energy[i]
                    self.best_position[i] = self.particles[i].copy()

                # 全局最佳
                if self.energy[i] < self.gbest_energy:
                    self.gbest_energy = self.energy[i]
                    self.gbest_position = self.particles[i].copy()
                
            for i in range(self.num_par):
                r1 = np.random.rand(self.dim)
                r2 = np.random.rand(self.dim)

                self.particles[i] = self.particles[i] + r1 * (self.best_position[i] - self.particles[i]) + r2 * (self.gbest_position - self.particles[i])
                # 邊界處理
                self.particles[i] = np.clip(self.particles[i], self.lb, self.ub)

            convergence_curve.append(self.gbest_energy)
        return self.gbest_position, self.gbest_energy, convergence_curve
    

class BESCONTROL:
    def __init__(self,MAX_ITER, NUM_PARTICLES, YEAR, FUNCTION_NAME, DIM):
        self.MAX_ITER = MAX_ITER
        self.NUM_PARTICLES = NUM_PARTICLES
        self.YEAR = YEAR
        self.FUNCTION_NAME = FUNCTION_NAME
        self.DIM = DIM
        
        function = CEC(self.YEAR, self.FUNCTION_NAME, self.DIM).get_function_info()  # 取得CEC Year年度，維度為 DIM 之 F1 函式的資訊
        
        self.UB = function.ub
        self.LB = function.lb
        #print(f"UB: {self.UB} || LB: {self.LB}")
        self.dim= function.dim
        self.f = function.func

    def info(self):
        return f"BES Convergence {self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D"

    def Start(self):
        bes = BES(obj_function=self.f, dim=self.DIM, lb=self.LB, ub=self.UB, 
                    num_par=self.NUM_PARTICLES, max_iter=self.MAX_ITER)
        best_position, best_value, curve = bes.optimize()
        
        """ print("Best solution found:", best_position)
        print("Best fitness:", best_value) """

        return np.log10(curve)




if __name__ == '__main__':

    funcs_by_year = {
        "2021": ["F3", "F6", "F8", "F10"],
        "2022": ["F4", "F7", "F8", "F9"]
    }

    # 設定參數
    MAX_ITER = 500
    NUM_PARTICLES = 30
    DIM = 10

    # CEC 函式呼叫方法  
    for year in funcs_by_year:
        for func_name in funcs_by_year[year]:
            function = CEC(year,func_name,DIM).get_function_info()  # 取得CEC Year年度，維度為 DIM 之 F1 函式的資訊
            UB = function.ub
            LB = function.lb
            f = function.func # 取得函式
            # 計算函式值 f([多個維度組成的陣列])   -> 例如 f([x,y])

    
            # 執行 BES
            bes = BES(obj_function=f, dim=DIM, lb=LB, ub=UB, num_par=NUM_PARTICLES, max_iter=MAX_ITER)
            best_position, best_value, curve = bes.optimize()

            print(f"[CEC {year}-{func_name}] Best solution found:", best_position)
            print(f"[CEC {year}-{func_name}] Best fitness:", best_value)

            # 繪製收斂曲線
            plt.plot(np.log10(curve))
            plt.xlabel("Iterations")
            plt.ylabel("Fitness Value (Log10)")
            plt.title(f"BES Convergence {year}-{func_name}-{DIM}D")
            plt.show()
