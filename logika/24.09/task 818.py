class MoneyBox():
    def __init__(self,max_capacity,name) -> None:
        self.max_capacity = max_capacity
        self.current = 0
        self.name = name
    def MONEU_MORE_MONEY(self, MONEU):
        if self.current + MONEU <= self.max_capacity:
            self.current += MONEU
            print(f"added {MONEU} to the {self.name} jar")
        else:
            print(f"you cant add {MONEU} more, it's gonna overflow")
    def feature_for_convinience_but_nobody_told_me_to_do_it_so_i_did_it_anyways_introducing_check_balance(self):
        
        if self.current < self.max_capacity:
            print(f"currently there are {self.current} green ones in this jar. you can only add {self.max_capacity-self.current} more")
        elif self.current == self.max_capacity:
            print("it's full you dumb#ss, get a new one")
        else:
            print("how tf did you overflow")

moneycollector = MoneyBox(200,"moneycollector")
moneycollector.feature_for_convinience_but_nobody_told_me_to_do_it_so_i_did_it_anyways_introducing_check_balance()
moneycollector.MONEU_MORE_MONEY(40)
moneycollector.feature_for_convinience_but_nobody_told_me_to_do_it_so_i_did_it_anyways_introducing_check_balance()
moneycollector.MONEU_MORE_MONEY(160)
moneycollector.feature_for_convinience_but_nobody_told_me_to_do_it_so_i_did_it_anyways_introducing_check_balance()
moneycollector.MONEU_MORE_MONEY(1)