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

class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

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
            tmp = obj.Start()
            Result = (Result * i + tmp)/ (i+1) if Result is not None else tmp
            print(f"Epoch {i+1} completed",end='')
        print("\n")
        return Result

    def Start(self, EPOCH):
        EDGWO_obj = EDGWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                        FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        GWO_obj = GWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                    FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        CHG_obj = CHGWOSCACONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                        FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        REE_obj = REEGWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                        FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        MSG_obj = MSGWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                        FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        
        print(f"{Color.YELLOW}Starting ED-GWO works for {EPOCH} Epochs{Color.RESET}")
        EDGWOResult = self.Worker(EDGWO_obj, EPOCH)

        print(f"{Color.YELLOW}Starting GWO works for {EPOCH} Epochs{Color.RESET}")
        GWOResult = self.Worker(GWO_obj, EPOCH)

        print(f"{Color.YELLOW}Starting CHGWOSCA works for {EPOCH} Epochs{Color.RESET}")
        CHGResult = self.Worker(CHG_obj, EPOCH)

        print(f"{Color.YELLOW}Starting REEGWO works for {EPOCH} Epochs{Color.RESET}")
        REEResult = self.Worker(REE_obj, EPOCH)

        print(f"{Color.YELLOW}Starting MSGWO works for {EPOCH} Epochs{Color.RESET}")
        MSGResult = self.Worker(MSG_obj, EPOCH)

        print(f"{Color.GREEN}All {EPOCH} Epochs completed{Color.RESET}")
        print(f"{Color.GREEN}Plotting the results{Color.RESET}")

        plt.plot(EDGWOResult, label="ED-GWO", color='black')
        plt.plot(GWOResult, label="GWO", color='red')
        plt.plot(CHGResult, label="CHGWOSCA", color='blue')
        plt.plot(REEResult, label="REEGWO", color='green')
        plt.plot(MSGResult, label="MSGWO", color='purple')


        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D-{self.NUM_WOLVES}N-{EPOCH} EPOCH")
        plt.legend()
        plt.show()


if __name__ == '__main__':


    funcs_by_year = {
        "2021": ["F3", "F4", "F6", "F7", "F8", "F9", "F10"],
        "2022": ["F2", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
    }

    while True:
        year = input("Enter the year of CEC (2021/2022): ")
        if year not in funcs_by_year:
            print("Invalid year")
            exit()

        func_name = input(f"Enter the function name ({', '.join(funcs_by_year[year])}): ")
        if func_name not in funcs_by_year[year]:
            print("Invalid function name\n\n")
            exit()

        dim = int(input("Enter the dimension (10 or 20): "))
        if dim not in [10, 20]:
            print("Invalid dimension")
            exit()
        
        print(f"{Color.MAGENTA}DataSet: CEC {year}-{func_name} - Dimension: {dim}{Color.RESET}\n")
        MAINCONTROL(MAX_ITER=500, NUM_WOLVES=30, YEAR=year, FUNCTION_NAME=func_name, DIM=dim).Start(10)