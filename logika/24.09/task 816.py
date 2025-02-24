from random import choice


class Coin():
    def __init__(self):
        self.sideup = None
    def flip(self,number_of_flips):
        for n in range(number_of_flips):
            self.sideup = choice(["Heads","Tails"])
            print(f"flip {n+1} resulted in {self.sideup}")

coin = Coin()
coin.flip(50)