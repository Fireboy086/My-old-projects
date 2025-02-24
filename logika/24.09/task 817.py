class Car():
    def __init__(self,mark,model,year) -> None:
        self.speed = 0
        self.mark = mark
        self.model = model
        self.year = year
    def accelerate(self):
        self.speed += 5
    def brake(self):
        if self.speed >= 5:
            self.speed += -5
    def get_speed(self):
        return self.speed
    def introduce_to_the_public(self):
        print(f"i (the {self.mark} {self.model} {self.year}) can go wroom wroom")

wroom_wroom = Car("Hyundai","Tucson",2020)

wroom_wroom.introduce_to_the_public()

for i in range(5):
    wroom_wroom.accelerate()
    print(f"Current speed: {wroom_wroom.get_speed()}")

for i in range(5):
    wroom_wroom.brake()
    print(f"Current speed: {wroom_wroom.get_speed()}")