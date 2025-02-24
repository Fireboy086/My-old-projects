class Dog:
    mammal = True

    def __init__(self, name, age, nature, breed):
        self.name = name
        self.age = age
        self.nature = nature
        self.breed = breed

    def info(self):
        return f"{self.name} is {self.age}. {self.nature} {self.breed} breed dog."

    def bark(self):
        return "Woof!"

class Pets:
    def __init__(self):
        self.pets_list = []

    def add_pet(self, pet):
        self.pets_list.append(pet)

    def show_pets(self):
        print(f"I have {len(self.pets_list)} dogs.")
        for pet in self.pets_list:
            print(pet.info())
        print("And they're all mammals, of course.")

toby = Dog("Toby", 4, "Kind", "Golden Retriever")
charlie = Dog("Charlie", 6, "Tireless", "Jack Russell Terrier")
rocky = Dog("Rocky", 7, "Obedient", "Ordinary")

my_pets = Pets()
my_pets.add_pet(toby)
my_pets.add_pet(charlie)
my_pets.add_pet(rocky)

my_pets.show_pets()
