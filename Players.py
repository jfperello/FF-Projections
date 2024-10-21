class Player:

    def __init__(self, name, pos, catches, targets, rushing_attempts,rushing_yds):
        self.name = name
        self.pos = pos
        self.catches = catches
        self.targets = targets
        self.rushing_attempts = rushing_attempts
        self.rushing_yds = rushing_yds
       

    def catch_rate(self):
        return self.catches/self.targets
    def yds_per_carry(self):
        return self.rushing_yds/self.rushing_attempts
    def efficiency(self):
        self.yds_per_carry =  self.yds_per_carry()
        self.catch_rate = self.catch_rate()
    def print_player_stats(self):
        player_string = []
        for k,v in self.__dict__.items():
            print(f'{str(k).capitalize()}: {v}')

def main():
    #creating an instance of a class
    jj = Player(name = 'Justin Jefferson', pos='WR',catches = 128, targets=184, rushing_attempts=10, rushing_yds=82)
    #call our catch_rate method
    jj.efficiency()
    jj.print_player_stats()


if __name__ == "__main__":
    main()