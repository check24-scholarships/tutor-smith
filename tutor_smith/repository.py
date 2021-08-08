import abc

# Implement repository pattern with "abtract" classes
class Repository(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.__items = []

    # Add all class attributes
    @property
    def items(self):
        raise NotImplementedError

    def add(self, item):
        pass

    @abc.abstractmethod
    def remove(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    # Further abstract methods and abstract attributes can be added here
