import numpy as np
import matplotlib.pyplot as plt
try:
    from EDGWO.CECData import CEC
except:
    from CECData import CEC
# 定義 cHGWOSCA 
class CHGWOSCA:
    def __init__(self, obj_function, dim, lb, ub, num_wolves=30, max_iter=100):
        self.obj_function = obj_function  
        self.dim = dim
        self.lb = np.array(lb)
        self.ub = np.array(ub)
        self.num_wolves = num_wolves
        self.max_iter = max_iter

        # 初始化狼群位置
        self.wolves = np.random.uniform(self.lb, self.ub, (self.num_wolves, self.dim))
        self.alpha, self.beta, self.delta = np.random.uniform(self.lb, self.ub, self.dim),np.random.uniform(self.lb, self.ub, self.dim),np.random.uniform(self.lb, self.ub, self.dim)
        self.alpha_score, self.beta_score, self.delta_score = np.inf, np.inf, np.inf

    def optimize(self):
        convergence_curve = []
        for t in range(self.max_iter):
            # 更新 Alpha Beta Delta
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

            a = 2 - t * (2 / self.max_iter)
            w = t / self.max_iter

            # 更新所有狼的位置
            for i in range(self.num_wolves):
                # --- GWO 更新公式 ---
                r1, r2 = np.random.rand(), np.random.rand() 
                A1, C1 = 2 * a * r1 - a, 2 * r2
                D_alpha = abs(C1 * self.alpha - self.wolves[i])
                X1 = self.alpha - A1 * D_alpha

                r1, r2 = np.random.rand(), np.random.rand()
                A2, C2 = 2 * a * r1 - a, 2 * r2
                D_beta = abs(C2 * self.beta - self.wolves[i])
                X2 = self.beta - A2 * D_beta

                r1, r2 = np.random.rand(), np.random.rand()
                A3, C3 = 2 * a * r1 - a, 2 * r2
                D_delta = abs(C3 * self.delta - self.wolves[i])
                X3 = self.delta - A3 * D_delta

                X_gwo = (X1 + X2 + X3) / 3

                # --- SCA 更新公式 ---
                r1_sca, r2_sca = np.random.rand(), np.random.rand()
                r3_sca, r4_sca = np.random.rand(), np.random.rand()
                if r4_sca < 0.5:
                    X_sca = self.wolves[i] + r1_sca * np.sin(r2_sca) * abs(r3_sca * self.alpha - self.wolves[i])
                else:
                    X_sca = self.wolves[i] + r1_sca * np.cos(r2_sca) * abs(r3_sca * self.alpha - self.wolves[i])

                # 混合
                X_new = 0.9 * X_gwo + 0.1 * X_sca
                X_new = np.clip(X_new, self.lb, self.ub)
                self.wolves[i] = X_new

            convergence_curve.append(self.alpha_score)

        return self.alpha, self.alpha_score, convergence_curve
