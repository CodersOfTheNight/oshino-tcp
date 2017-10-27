import socket
import re

from oshino import Agent


class AsyncSocketWrapper(object):
    ADDR_PATT = re.compile(r"(tcp://)?(?P<host>\w+):(?P<port>\d+)")

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(0)

    @classmethod
    def parse_addr(cls, addr):
        result = cls.ADDR_PATT.search(addr)
        return result.group("host"), int(result.group("port"))

    def bind(self, addr):
        return self._socket.bind(self.parse_addr(addr))

    def connect(self, addr):
        return self._socket.connect(self.parse_addr(addr))


class TCPAgent(Agent):

    @property
    def bind(self):
        return self._data.get("bind", None)

    @property
    def connect(self):
        return self._data["connect"]

    @property
    def parser(self):
        path = self._data.get("parser", None)
        if path:
            module, fn_name = path.rsplit(".", 1)
            fn = getattr(__import__(module), fn_name)
            return fn
        else:
            return None

    def _parse(self, msg):
        parser_fn = self.parser
        if parser_fn:
            return parser_fn(msg)
        else:
            return None

    async def process(self, event_fn):
        logger = self.get_logger()
        if self.socket_active:
            try:
                logger.trace("Trying to read msg")
                msg = None
                logger.trace("Received msg: '{0}'".format(msg))
                msg_obj = self._parse(msg)
                if msg_obj:
                    event_fn(service=self.prefix, **msg_obj)
            except Exception as ex:
                logger.exception(ex)
        else:
            logger.debug("Zmq socket is still waiting for connection")

    def on_start(self):
        logger = self.get_logger()
        logger.info("Initializing TCP Socket")
        self.socket = AsyncSocketWrapper()
        if self.bind:
            self.socket.bind(self.bind)
            logger.info("TCP Socket bound on: {0}".format(self.bind))
            self.socket_active = True
        else:
            self.socket.connect(self.connect)
            logger.info("TCP Socket connected to: {0}".format(self.connect))
            self.socket_active = True

    def on_stop(self):
        self.socket.close()
