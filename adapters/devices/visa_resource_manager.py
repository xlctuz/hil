import pyvisa

rm = pyvisa.ResourceManager()

if __name__ == "__main__":
    import time
    while True:
        logger.info(rm.list_resources())
        time.sleep(1)

