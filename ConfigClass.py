
from EDGWO.EDGWO import EDGWOCONTROL
from GWO.GWO import GWOCONTROL
from CHGWOSCA.CHGWOSCA import CHGWOSCACONTROL
from REEGWO.REEGWO import REEGWOCONTROL
from MSGWO.MSGWO import MSGWOCONTROL
from PSO.PSO import PSOCONTROL
from BES.BES import BESCONTROL
from HHO.HHO import HHOCONTROL
from ChOA.ChOA import ChOACONTROL
from SCSO.SCSO import SCSOCONTROL

class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

class Configs:
    optimizers = {
        "EDGWO": EDGWOCONTROL,
        "GWO": GWOCONTROL,
        "CHGWOSCA": CHGWOSCACONTROL,
        "REEGWO": REEGWOCONTROL,
        "MSGWO": MSGWOCONTROL,
        "BES": BESCONTROL,
        "ChOA": ChOACONTROL,
        "PSO" :PSOCONTROL,
        #"HHO" :HHOCONTROL,
        "SCSO":SCSOCONTROL,
    } 
    

