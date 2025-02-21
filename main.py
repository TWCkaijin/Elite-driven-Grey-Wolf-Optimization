import numpy as np
import matplotlib.pyplot as plt

from EDGWO.EDGWO import EDGWOCONTROL
from GWO.GWO import GWOCONTROL
from CHGWOSCA.CHGWOSCA import CHGWOSCACONTROL
from REEGWO.REEGWO import REEGWOCONTROL



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
        
        print(f"Starting ED-GWO works for {EPOCH} Epochs")
        EDGWOResult = self.Worker(EDGWO_obj, EPOCH)

        print(f"Starting GWO works for {EPOCH} Epochs")
        GWOResult = self.Worker(GWO_obj, EPOCH)

        print(f"Starting CHGWOSCA works for {EPOCH} Epochs")
        CHGResult = self.Worker(CHG_obj, EPOCH)

        print(f"Starting REEGWO works for {EPOCH} Epochs")
        REEResult = self.Worker(REE_obj, EPOCH)

        print(f"All {EPOCH} Epochs completed")
        print("Plotting the results")

        plt.plot(EDGWOResult, label="ED-GWO", color='black')
        plt.plot(GWOResult, label="GWO", color='red')
        plt.plot(CHGResult, label="CHGWOSCA", color='blue')
        plt.plot(REEResult, label="REEGWO", color='green')

        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D-{self.NUM_WOLVES}N-{EPOCH} EPOCH")
        plt.legend()
        plt.show()


if __name__ == '__main__':


    funcs_by_year = {
        "2021": ["F3", "F6", "F8", "F10"],
        "2022": ["F4", "F7", "F8", "F9"]
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

        
        print(f"DataSet: CEC {year}-{func_name}\n")
        MAINCONTROL(MAX_ITER=500, NUM_WOLVES=30, YEAR=year, FUNCTION_NAME=func_name, DIM=10).Start(10)
