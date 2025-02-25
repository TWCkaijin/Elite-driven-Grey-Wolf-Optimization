import numpy as np
import matplotlib.pyplot as plt

from DataSet import DataSet

class PSO:
    def __init__(self, obj_function, dim, lb, ub, num_par=30, max_iter=30, w=0.7, c1=2, c2=2):
        self.obj_function = obj_function
        self.dim = dim
        self.lb = np.array(lb)
        self.ub = np.array(ub)
        self.num_par = num_par
        self.max_iter = max_iter
        self.w = w
        self.c1 = c1
        self.c2 = c2

        # 初始化速度/位置
        self.particles = np.random.uniform(self.lb, self.ub, (self.num_par, self.dim))
        self.velocities = np.random.uniform(-abs(self.ub - self.lb), abs(self.ub - self.lb), (self.num_par, self.dim))

        # 個體最佳解
        self.pbest = self.particles.copy()
        self.pbest_scores = np.array([np.inf] * self.num_par)

        # 全局最佳解
        self.gbest = np.random.uniform(self.lb, self.ub, self.dim)
        self.gbest_score = np.inf
    
    def optimize(self):
        convergence_curve = []

        for t in range(self.max_iter):
            for i in range(self.num_par):
                fitness = self.obj_function(self.particles[i])
                
                if fitness < self.pbest_scores[i]:
                    self.pbest_scores[i] = fitness
                    self.pbest[i] = self.particles[i].copy()

                if fitness < self.gbest_score:
                    self.gbest_score = fitness
                    self.gbest = self.particles[i].copy()
        
            for i in range(self.num_par):
                r1, r2 = np.random.rand(self.dim), np.random.rand(self.dim)
                cognitive_component = self.c1 * r1 * (self.pbest[i] - self.particles[i])
                social_component = self.c2 * r2 * (self.gbest - self.particles[i])
                self.velocities[i] = self.w * self.velocities[i] + cognitive_component + social_component

                # 更新位置
                self.particles[i] += self.velocities[i]

                # 邊界處理
                self.particles[i] = np.clip(self.particles[i], self.lb, self.ub)

            convergence_curve.append(self.gbest_score)
    
        return self.gbest, self.gbest_score, convergence_curve, self.particles
    

class PSOCONTROL:
    def __init__(self,MAX_ITER, NUM_WOLVES, YEAR, FUNCTION):
        self.MAX_ITER = MAX_ITER
        self.NUM_PARTICLES = NUM_WOLVES
        self.YEAR = YEAR

        self.UB = FUNCTION.ub
        self.LB = FUNCTION.lb
        self.DIM= FUNCTION.dim
        self.f = FUNCTION.func
        self.f_type = FUNCTION.f_type

    def Start(self):
        pso = PSO(obj_function=self.f, dim=self.DIM, lb=self.LB, ub=self.UB, 
                    num_par=self.NUM_PARTICLES, max_iter=self.MAX_ITER)
        best_position, best_value, curve, particles = pso.optimize()
        
        """ print("Best solution found:", best_position)
        print("Best fitness:", best_value) """

        return (particles, np.log10(curve))




if __name__ == '__main__':

    funcs_by_year = DataSet.funcs_years

    # 設定參數
    MAX_ITER = 500
    NUM_PARTICLES = 30
    DIM = 10

    # CEC 函式呼叫方法  
    for year in funcs_by_year['CEC']:
        for func_name in funcs_by_year['CEC'][year]:
            function = DataSet.get_function(year,func_name,DIM)  # 取得CEC Year年度，維度為 DIM 之 F1 函式的資訊
            UB = function.ub
            LB = function.lb
            f = function.func # 取得函式
            # 計算函式值 f([多個維度組成的陣列])   -> 例如 f([x,y])

    
            # 執行 PSO
            pso = PSO(obj_function=f, dim=DIM, lb=LB, ub=UB, num_par=NUM_PARTICLES, max_iter=MAX_ITER)
            best_position, best_value, curve = pso.optimize()

            print(f"[CEC {year}-{func_name}] Best solution found:", best_position)
            print(f"[CEC {year}-{func_name}] Best fitness:", best_value)

            # 繪製收斂曲線
            plt.plot(np.log10(curve))
            plt.xlabel("Iterations")
            plt.ylabel("Fitness Value (Log10)")
            plt.title(f"PSO Convergence {year}-{func_name}-{DIM}D")
            plt.show()
