class User:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    
    def __str__(self):
        return f"L'utente è {self.name} {self.surname}"
    
    def getSurname(self):
        return self.surname

