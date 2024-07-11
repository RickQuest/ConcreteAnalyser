import abc

class BaseStage(metaclass=abc.ABCMeta):

    def __init__(self):
        self._port = 'COM1'
        self._stagezone = [0,0,0]
        self._baudrate = 250000
        self._parity=8
        self._bits=8

    @property
    def stagezone(self):
        return self._stagezone
    @stagezone.setter
    def stagezone(self, a):
        if(a[0] < 0 or a[1]<0 or a[2]<0):
            raise ValueError("Sorry stage dimensions cannot be negative")
        self._stagezone = a

    @property
    def parity(self):
        return self._parity
    @parity.setter
    def parity(self, a):
        self._parity = a

    @property
    def port(self):
        return self._port
    @port.setter
    def port(self, a):
        self._port = a

    @property
    def bits(self):
        return self._bits
    @bits.setter
    def bits(self, a):
        self._bits = a

    @property
    def baudrate(self):
        return self._baudrate
    @baudrate.setter
    def baudrate(self, a):
        self._baudrate = a

    @classmethod
    @abc.abstractmethod
    def send_command(self):
        """ Implement me! """
        pass

    @classmethod
    @abc.abstractmethod
    def home(self):
        """ Implement me! """
        pass

    @classmethod
    @abc.abstractmethod
    def moveX(self):
        """ Implement me! """
        pass

    @classmethod
    @abc.abstractmethod
    def moveY(self):
        """ Implement me! """
        pass

    @classmethod
    @abc.abstractmethod
    def moveZ(self):
        """ Implement me! """
        pass

    @classmethod
    @abc.abstractmethod
    def start(self):
        """ Implement me! """
        pass

    @classmethod
    @abc.abstractmethod
    def stop(self):
        """ Implement me! """
        pass