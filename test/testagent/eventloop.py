import select

class EventLoop(object):
    """Minimalistic event loop"""
    def __init__(self):
        self.running = False
        self.readfds = []
        self.fd_dict = {}

    def set_default_handler(self, handler):
        self.default_handler = handler

    def add_default_fd(self, fd):
        self.readfds.append(fd)

    def add_handler(self, fd, handler):
        self.readfds.append(fd)
        self.fd_dict[fd] = handler

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while (self.running):
            readable, writable, exceptional = select.select(self.readfds, [], [])
            for fd in readable:
                if fd in self.fd_dict:
                    self.fd_dict[fd](self.stop)
                else:
                    self.default_handler(self.stop)

    def is_running(self):
        return self.running
