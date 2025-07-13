from src.program import *
from src.sockets import *
import argparse
import signal




def main():
    parser = argparse.ArgumentParser(description="A simple program for sharing clipboards.")
    parser.add_argument("--port", type=int, default=6969, help="Port to run the server on (default: 6969)")
    parser.add_argument("-p", type=int, default=6969, help="Port to run the server on (default: 6969)")
    args = parser.parse_args()

    program = TerminalProgram(args.port)

    signal.signal(signal.SIGINT,program.shutdown)




    try:
        program.run()
    except:
        pass


if __name__ == "__main__":
    main()