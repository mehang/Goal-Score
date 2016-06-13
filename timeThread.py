import threading
import time
import scrape

# THIS THREAD WILL RUN FOREVER

# Tlock = threading.Lock()

def main(teams, delay, lock):
  start = time.time()
  
  scrape.main(teams, lock)

  # go on forever :: request after each delay
  while True:
    # wait for some time
    if (time.time() - start) > delay:
      print "CALL SCRAPE.MAIN() AGAIN."
      scrape.main(teams, lock)
      start = time.time()
      print time.ctime(start), " time after delay call to scrape."

# if __name__ == "__main__":
#   teams = ["mexico","uruguay"]
#   main(teams, 10, Tlock)                    