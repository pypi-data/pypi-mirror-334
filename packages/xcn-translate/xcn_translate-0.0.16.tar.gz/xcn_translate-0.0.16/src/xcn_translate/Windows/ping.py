from pythonping import ping
from pythonping.executor import ResponseList
from xcn_translate.Windows.xclog import xlogger

class Ping(object):
    target = '127.0.0.1'
    timeout = 4
    count = 1
    size = 10
    interval = 1

    __ping_response = None
    __except = None
    __result = None

    def __init__(self, target=None, timeout=None, count=None, size=None, interval=None, **kwargs):
        self.target = self.target if target is None else target
        self.timeout = self.timeout if timeout is None else timeout
        self.count = self.count if count is None else count
        self.size = self.size if size is None else size
        self.interval = self.interval if interval is None else interval
        if type(kwargs) == dict and len(kwargs) > 1:
            self.__init_kwargs(kwargs)

        self.__logger = xlogger('xcnPing', level=xlogger.INFO)
        self.__logger.setStreamhandler(level=xlogger.INFO)

    def __init_kwargs(self, kwargs):
        for key in kwargs.keys():
            if key == 'target':
                self.target = kwargs[key]
            elif key == 'timeout':
                self.timeout = kwargs[key]
            elif key == 'count':
                self.count = kwargs[key]
            elif key == 'size':
                self.size = kwargs[key]
            elif key == 'interval':
                self.interval = kwargs[key]

    @property
    def logger(self):
        return self.__logger;

    def start(self):
        try:
            self.__ping_response = \
                ping(self.target,
                    timeout = self.timeout,
                    count = self.count,
                    size = self.size,
                    interval = self.interval)
        except OSError as e:
            self.__except = str(e)

    @property
    def success(self):
        '''
        Check success state of the request.
        :rtype: bool
        '''
        if self.__except is not None:
            return False
        return self.__ping_response.success()

    @property
    def packet_loss(self):
        if self.__except is not None:
            return self.count
        ret = None if type(self.__ping_response) is not ResponseList else self.__ping_response.packet_loss
        return ret

    @property
    def rtt_min_ms(self):
        ret = None if type(self.__ping_response) is not ResponseList else self.__ping_response.rtt_min_ms
        return ret

    @property
    def rtt_max_ms(self):
        ret = None if type(self.__ping_response) is not ResponseList else self.__ping_response.rtt_max_ms
        return ret

    @property
    def rtt_avg_ms(self):
        ret = None if type(self.__ping_response) is not ResponseList else self.__ping_response.rtt_avg_ms
        return ret

    @property
    def result(self):
        if self.__except is not None:
            return self.__except
        if type(self.__ping_response) is ResponseList:
            return '{}'.format(self.__ping_response)
        return None