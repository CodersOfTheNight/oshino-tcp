from oshino import Agent


class TCPAgent(Agent):

    @property
    def bind(self):
        return self._data.get("bind", None)

    @property
    def connect(self):
        return self._data["connect"]

    async def process(self, event_fn):
        logger = self.get_logger()
        if self.socket_active:
            try:
                logger.trace("Trying to read msg")
                msg = None
                logger.trace("Received msg: '{0}'".format(msg))
                event_fn(service=self.prefix, **json_obj)
            except Exception as ex:
                logger.exception(ex)
        else:
            logger.debug("Zmq socket is still waiting for connection")

    def on_start(self):
        logger = self.get_logger()
        logger.info("Initializing TCP Socket")
        self.socket = None
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
