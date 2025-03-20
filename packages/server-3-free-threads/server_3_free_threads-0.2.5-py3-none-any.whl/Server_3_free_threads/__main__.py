import sys
from Server_3_free_threads.initial_func import main


try:
    main()
except KeyboardInterrupt:
    sys.exit()
