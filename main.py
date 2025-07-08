from src.program import *
from src.sockets import *
import signal

program = TerminalProgram()

signal.signal(signal.SIGINT,program.shutdown)




try:
    program.run()
except:
    pass


