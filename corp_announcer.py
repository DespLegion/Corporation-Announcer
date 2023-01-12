import time
import sys
from src.announcer_core.commands import execute_from_command_line


# start_time = time.time()

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
    # print("_________________________________________")
    # print("--- %s seconds ---" % (time.time() - start_time))
