import numpy as np
import matplotlib.pyplot as plt
from EDGWO.EDGWO import EDGWOCONTROL
from GWO.GWO import GWOCONTROL



class CentralControl:
    def __init__(self, MAX_ITER, NUM_WOLVES, YEAR, FUNCTION_NAME, DIM):
        self.MAX_ITER = MAX_ITER
        self.NUM_WOLVES = NUM_WOLVES
        self.YEAR = YEAR
        self.FUNCTION_NAME = FUNCTION_NAME
        self.DIM = DIM

    def Start(self):
        EDGWOResult = EDGWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                    FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM).Start()
        GWOResult = GWOCONTROL(MAX_ITER=self.MAX_ITER, NUM_WOLVES=self.NUM_WOLVES, YEAR=self.YEAR,
                                FUNCTION_NAME=self.FUNCTION_NAME, DIM=self.DIM).Start()

        plt.plot(EDGWOResult.curve, label="ED-GWO")
        plt.plot(GWOResult.curve, label="GWO")
        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.YEAR}-{self.FUNCTION_NAME}-{self.DIM}D with {self.NUM_WOLVES} wolves")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    CentralControl(MAX_ITER=500, NUM_WOLVES=30, YEAR="2022", FUNCTION_NAME="F1", DIM=10).Start()