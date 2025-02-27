import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


from DataSet import DataSet
from ConfigClass import Color
from ConfigClass import Configs

class MAINCONTROL:
    def __init__(self, MAX_ITER, NUM_WOLVES, param_I, param_II, param_III, DIM):
        self.MAX_ITER = MAX_ITER
        self.NUM_WOLVES = NUM_WOLVES
        self.param_I = param_I
        self.param_II = param_II
        self.param_III = param_III
        self.DIM = DIM

    def Start(self, EPOCH):
        opt_obj = Configs.optimizers["EDGWO"](self.MAX_ITER, self.NUM_WOLVES,
                                            DataSet.get_function(I=self.param_I, II=self.param_II, III=self.param_III, dim=self.DIM))
        # 啟用交互模式
        plt.ion()
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X = np.linspace(-100, 100, 100)
        Y = np.linspace(-100, 100, 100)
        X, Y = np.meshgrid(X, Y)

        data_obj = DataSet.get_function(self.param_I, self.param_II, self.param_III, self.DIM)
        Z = np.vectorize(lambda x, y: data_obj.func([x, y]))(X, Y)

        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        scatter = ax.scatter([], [], [], color='black', marker='o')

        def update(frame):
            scatter._offsets3d = (EDGWO_Wolves[:, 0], EDGWO_Wolves[:, 1], np.vectorize(lambda x, y: data_obj.func([x, y]))(EDGWO_Wolves[:, 0], EDGWO_Wolves[:, 1]))
            return scatter,

        ani = FuncAnimation(fig, update, frames=range(1), interval=100, blit=False)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Fitness")
        plt.title(f"{self.param_III} / Epoch={EPOCH}")
        

        for i in range(EPOCH):
            plt.title(f"{self.param_I}-{self.param_II}-{self.param_III} / Epoch={i+1}")
            EDGWO_Wolves, EDGWO_Result = opt_obj.Start()
            # 更新圖形
            scatter._offsets3d = (EDGWO_Wolves[:, 0], EDGWO_Wolves[:, 1], np.vectorize(lambda x, y: data_obj.func([x, y]))(EDGWO_Wolves[:, 0], EDGWO_Wolves[:, 1]))
            plt.draw()
            plt.show()
            plt.pause(0.1)

        # 關閉交互模式
        plt.ioff()
        plt.show()
        print("Demo completed")

if __name__ == '__main__':


    funcs_by_year = DataSet().all_funcs
    

    while True:
        
        f_type = input(f"Enter the Dataset param ({' / '.join(funcs_by_year)}): ") # DataSet
        year = None
        name = None
        dim = None

        if f_type not in funcs_by_year:
            print("Invalid function type")
            continue
        if f_type == "CEC":
            year = input(f"Enter the Year param ({' / '.join(funcs_by_year[f_type])}): ") # Year
            if year not in funcs_by_year[f_type]:
                print("Invalid param")
                continue

            name = input(f"Enter the Name param ({' / '.join(funcs_by_year[f_type][year])}): ") # Function Name
            if name not in funcs_by_year[f_type][year]:
                print("Invalid param\n\n")
                continue
            
            if "2" not in funcs_by_year[f_type][year][name]:
                print("Demo method can only perform 2 dimension data\n\n")
                continue

            dim = input(f"Enter the Dim param ({' / '.join(funcs_by_year[f_type][year][name])}): ") # Dimension
            if dim not in funcs_by_year[f_type][year][name]:
                print("Invalid param\n\n")
                continue
        elif(f_type == "GENE"):
            print("GENE is not supported in this demo")
            continue

        print(f"{Color.MAGENTA}DataSet: {f_type}-{year}-{name} - Dimension: {dim}{Color.RESET}\n")
        MAINCONTROL(MAX_ITER=1, NUM_WOLVES=30, param_I=f_type, param_II=year, param_III=name, DIM=int(dim)).Start(int(input("Input iterations: ")))