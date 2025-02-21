from EDGWO.EDGWO import EDGWOCONTROL




if __name__ == '__main__':
    EDGWOResult = EDGWOCONTROL(MAX_ITER=500, NUM_WOLVES=30, YEAR="2022", FUNCTION_NAME="F1", DIM=10).Start()
    print(EDGWOResult.curve)