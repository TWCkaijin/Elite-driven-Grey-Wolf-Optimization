import numpy as np
import matplotlib.pyplot as plt

from ConfigClass import Configs
from ConfigClass import Color

from DataSet import DataSet

class MAINCONTROL:
    def __init__(self, MAX_ITER, NUM_WOLVES, f_type, year, name, DIM):
        self.MAX_ITER = MAX_ITER
        self.NUM_WOLVES = NUM_WOLVES
        self.f_type = f_type
        self.year = year
        self.name = name
        self.DIM = DIM

    def Worker(self, obj, EPOCH):
        Result= None
        for i in range(EPOCH):
            print('\r',end='')
            tmp = (1/(obj.Start()[-1])) if self.f_type == "GENE" else obj.Start()[-1]
            Result = (Result * i + tmp)/ (i+1) if Result is not None else tmp

            print(f"Epoch {i+1} completed",end='')
        print()
        return Result

    def Start(self, EPOCH):

        for optimizer in Configs.optimizers:
            print(f"{Color.MAGENTA}Starting {optimizer} works for {EPOCH} Epochs{Color.RESET}")
            obj = Configs.optimizers[optimizer](self.MAX_ITER, self.NUM_WOLVES,
                                                DataSet.get_function(I=self.f_type, II=self.year, III=self.name, dim=self.DIM))
            Result = self.Worker(obj, EPOCH)
            print(f"{Color.GREEN}{optimizer} completed{Color.RESET}\n\n")
            plt.plot(Result, label=optimizer)
        
        print(f"{Color.GREEN}All Optimizers Completed, plotting the chart{Color.RESET}")
        plt.xlabel("Iterations")
        plt.ylabel("Fitness Value (Log10)")
        plt.title(f"CEC{self.year}-{self.name}-{self.DIM}D-{self.NUM_WOLVES}N-{EPOCH} EPOCH")
        plt.legend()
        plt.show()


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
            

            dim = input(f"Enter the Dim param ({' / '.join(funcs_by_year[f_type][year][name])}): ") # Dimension
            if dim not in funcs_by_year[f_type][year][name]:
                print("Invalid param\n\n")
                continue
        elif(f_type == "GENE"):
            name = input(f"Enter the Name param:\n{'\n'.join(funcs_by_year[f_type])}\nEnter the index: ")
            name = list(funcs_by_year['GENE'].keys())[int(name)-1]
            dim = funcs_by_year[f_type][name]
            print(f"Selected: {name} - Dimension: {dim}")
        else:
            print("Invalid function type")
            continue

        print(f"{Color.MAGENTA}DataSet: {f_type}-{year}-{name} - Dimension: {dim}{Color.RESET}\n")
        MAINCONTROL(MAX_ITER=int(input("Input Ieration per epoch: ")), NUM_WOLVES=30, f_type=f_type,year=year, name=name, DIM=int(dim)).Start(int(input("Input Epochs: ")))