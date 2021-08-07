import abc
# Implement repository pattern with "abtract" classes
class Repository(abc.ABC):

    @abc.abstractmethod
    def add(self):
        pass
    
    @abc.abstractmethod
    def remove(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    # Further abstract methods and abstract attributes can be added here