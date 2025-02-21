import numpy as np
import matplotlib.pyplot as plt

from EDGWO.EDGWO import EDGWOCONTROL
from GWO.GWO import GWOCONTROL



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
            tmp = obj.Start()
            Result = (Result * i + tmp)/ (i+1) if Result is not None else tmp
            print(f"Epoch {i+1} completed")
        return Result

    def Start(self, EPOCH):
        EDGWOResult = None
        GWOResult = None
        EDGWO_obj = EDGWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                        FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        GWO_obj = GWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                    FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM)
        
        
        EDGWOResult = self.Worker(EDGWO_obj, EPOCH)
        GWOResult = self.Worker(GWO_obj, EPOCH)

        print(f"All {EPOCH} Epochs completed")
        plt.plot(EDGWOResult, label="ED-GWO")
        plt.plot(GWOResult, label="GWO")
        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D-{self.NUM_WOLVES}N-30 EPOCH")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    funcs_by_year = {
        "2021": ["F3", "F6", "F8", "F10"],
        "2022": ["F4", "F7", "F8", "F9"]
    }

    for year in funcs_by_year:
        for func_name in funcs_by_year[year]:
            print(f"CEC {year}-{func_name}")
            MAINCONTROL(MAX_ITER=500, NUM_WOLVES=30, YEAR=year, FUNCTION_NAME=func_name, DIM=10).Start(10)