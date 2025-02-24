import numpy as np
import matplotlib.pyplot as plt

from EDGWO.EDGWO import EDGWOCONTROL
from GWO.GWO import GWOCONTROL
from CHGWOSCA.CHGWOSCA import CHGWOSCACONTROL
from REEGWO.REEGWO import REEGWOCONTROL
from MSGWO.MSGWO import MSGWOCONTROL
from PSO.PSO import PSO
from BES.BES import BES
from HHO.HHO import HHO
from ChOA.ChOA import ChOA

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
        print("\n")
        return Result

    def Start(self, EPOCH):

        for optimizer in Configs.optimizers:
            print(f"{Color.MAGENTA}Starting {optimizer} works for {EPOCH} Epochs{Color.RESET}")
            obj = Configs.optimizers[optimizer](MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                                FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
            Result = self.Worker(obj, EPOCH)
            print(f"{Color.GREEN}{optimizer} completed{Color.RESET}")
            plt.plot(Result, label=optimizer)

        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D-{self.NUM_WOLVES}N-{EPOCH} EPOCH")
        plt.legend()
        plt.show()


if __name__ == '__main__':


    funcs_by_year = DataSet.funcs_years

    while True:
        year = input("Enter the year of CEC (2021/2022): ")
        if year not in funcs_by_year:
            print("Invalid year")
            continue

        func_name = input(f"Enter the function name ({', '.join(funcs_by_year[year])}): ")
        if func_name not in funcs_by_year[year]:
            print("Invalid function name\n\n")
            continue

        dim = int(input("Enter the dimension (10 or 20): "))
        if dim not in [10, 20]:
            print("Invalid dimension")
            continue
        
        print(f"{Color.MAGENTA}DataSet: CEC {year}-{func_name} - Dimension: {dim}{Color.RESET}\n")
        MAINCONTROL(MAX_ITER=500, NUM_WOLVES=30, YEAR=year, FUNCTION_NAME=func_name, DIM=dim).Start(10)