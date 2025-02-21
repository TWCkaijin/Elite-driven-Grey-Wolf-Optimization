import numpy as np

# 定義 Grey Wolf Optimization (GWO)
class GWO:
    def __init__(self, obj_function, dim, lb, ub, num_wolves=10, max_iter=100):
        self.obj_function = obj_function  # 目標函數
        self.dim = dim                    # 變數維度
        self.lb = np.array(lb)            # 下界
        self.ub = np.array(ub)            # 上界
        self.num_wolves = num_wolves      # 狼群數量
        self.max_iter = max_iter          # 最大迭代次數

        # 初始化狼群位置
        self.wolves = np.random.uniform(self.lb, self.ub, (self.num_wolves, self.dim))
        self.alpha, self.beta, self.delta = np.zeros(self.dim), np.zeros(self.dim), np.zeros(self.dim)
        self.alpha_score, self.beta_score, self.delta_score = np.inf, np.inf, np.inf

    def optimize(self):
        convergence_curve = []
        for t in range(self.max_iter):
            # 計算適應度並更新 α, β, δ
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

                self.wolves[i] = (X1 + X2 + X3) / 3

                # 限制範圍
                self.wolves[i] = np.clip(self.wolves[i], self.lb, self.ub)

            convergence_curve.append(self.alpha_score)
        
        return self.alpha, self.alpha_score, convergence_curve
    
import matplotlib.pyplot as plt

# Rastrigin 測試函數 (全域最小值 f(0,0) = 0)
def rastrigin(X):
    A = 10
    return A * len(X) + sum([(x**2 - A * np.cos(2 * np.pi * x)) for x in X])

# 設定參數
dim = 2
lb, ub = [-5.12] * dim, [5.12] * dim
max_iter = 100

# 執行 GWO
gwo = GWO(obj_function=rastrigin, dim=dim, lb=lb, ub=ub, num_wolves=20, max_iter=max_iter)
best_position, best_value, curve = gwo.optimize()

print("Best solution found:", best_position)
print("Best fitness:", best_value)

# 繪製收斂曲線
plt.plot(curve)
plt.xlabel("Iterations")
plt.ylabel("Fitness Value")
plt.title("GWO Convergence Curve")
plt.show()

X = np.linspace(-5.12, 5.12, 100)
Y = np.linspace(-5.12, 5.12, 100)
X, Y = np.meshgrid(X, Y)
Z = rastrigin([X, Y])

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.7)

# 畫出狼群搜索過程
wolves_path = np.array(gwo.wolves)
for i in range(len(wolves_path)):
    ax.scatter(wolves_path[i][:, 0], wolves_path[i][:, 1], rastrigin(wolves_path[i].T), color='black', marker='o')

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Fitness")
plt.title("GWO Searching Path")
plt.show()
