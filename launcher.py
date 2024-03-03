from fetcher import Fetcher
from dasher import Dasher

def caller():
    fetobj = Fetcher()
    dashobj = Dasher()

    fetobj.fetcher()
    dashobj.dasher()

caller()