import Repository

# Example of a student repository under the abstract class repository
class StudentRepository(Repository.Repository):
    def __init__(self):
        self.__items = []

    def add(self, item):
        pass

    def remove(self):
        pass

    def update(self):
        raise NotImplementedError(
            "This method is not implemented for the student repository, please refer to the ...repository for this functionality!"
        )


test = StudentRepository()
