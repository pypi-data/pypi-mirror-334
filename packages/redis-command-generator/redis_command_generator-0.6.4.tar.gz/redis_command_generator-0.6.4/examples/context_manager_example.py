from time import sleep
import redis_command_generator as cg

# Hint: run `make dev` to interpret from local sources
if __name__ == '__main__':
    # Traffic will run for 1 minute and then gracefully stop
    with cg.GenRunner() as runner:
        sleep(60)