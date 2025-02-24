import numpy as np
import matplotlib.pyplot as plt

from ConfigClass import Configs
from ConfigClass import Color

from DataSet import DataSet

class MAINCONTROL:
    def __init__(self, MAX_ITER, NUM_WOLVES, YEAR, FUNCTION_NAME, DIM):
        self.MAX_ITER = MAX_ITER
        self.NUM_WOLVES = NUM_WOLVES
        self.YEAR = YEAR
        self.FUNCTION_NAME = FUNCTION_NAME
        self.DIM = DIM

    def Worker(self, obj, EPOCH):
        Result= None
        for i in range(EPOCH):
            print('\r',end='')
            tmp = obj.Start()[-1]
            Result = (Result * i + tmp)/ (i+1) if Result is not None else tmp
            print(f"Epoch {i+1} completed",end='')
        print()
        return Result

    def Start(self, EPOCH):

        for optimizer in Configs.optimizers:
            print(f"{Color.MAGENTA}Starting {optimizer} works for {EPOCH} Epochs{Color.RESET}")
            obj = Configs.optimizers[optimizer](self.MAX_ITER, self.NUM_WOLVES, self.YEAR,
                                                DataSet.get_function(self.YEAR, self.FUNCTION_NAME, self.DIM))
            Result = self.Worker(obj, EPOCH)
            print(f"{Color.GREEN}{optimizer} completed{Color.RESET}\n\n")
            plt.plot(Result, label=optimizer)
        
        print(f"{Color.GREEN}All Optimizers Completed, plotting the chart{Color.RESET}")
        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D-{self.NUM_WOLVES}N-{EPOCH} EPOCH")
        plt.legend()
        plt.show()


if __name__ == '__main__':


    funcs_by_year = DataSet.funcs_years

    while True:
        f_type = input("Enter the function type (CEC/gene): ")
        if f_type not in funcs_by_year:
            print("Invalid function type")
            continue

        year = input(f"Enter the year of CEC ({', '.join(funcs_by_year[f_type])}): ")
        if year not in funcs_by_year[f_type]:
            print("Invalid year")
            continue

        func_name = input(f"Enter the function name ({', '.join(funcs_by_year[f_type][year])}): ")
        if func_name not in funcs_by_year[f_type][year]:
            print("Invalid function name\n\n")
            continue

        dim = int(input("Enter the dimension (10 or 20): "))
        if dim not in [10, 20]:
            print("Invalid dimension")
            continue
        
        print(f"{Color.MAGENTA}DataSet: CEC {year}-{func_name} - Dimension: {dim}{Color.RESET}\n")
        MAINCONTROL(MAX_ITER=300, NUM_WOLVES=30, YEAR=year, FUNCTION_NAME=func_name, DIM=dim).Start(1)