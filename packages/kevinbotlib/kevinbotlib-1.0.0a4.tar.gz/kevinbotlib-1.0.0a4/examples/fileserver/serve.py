import time

from kevinbotlib.fileserver import FileServer

server = FileServer(
    ftp_port=2121,  # ftp
    http_port=8000,  # http
    directory="./",  # serve directory
)

try:
    server.start()

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.stop()
