import sys


class Duplicator:
    def __init__():
        # A.I. 
        # goes second
        pass


class Logger:
    def __init__(self, filename='games.log'):
        self.filename = filename
        self.log = open(filename, 'a')
        self.cli = sys.stdout
    
    def write(self, string):
        self.cli.write(string)
        self.log.write(string)
    
    def flush(self):
        pass


class NewGameObserver:
    def __init__(self):
        self.number_games_played = 0
        self.new_game_message = "Do you want to play again? [Y/N]"
        self.wrong_format = "\nThe answer is either 'Y' or 'N'.\nTry again:"
    
    def __run(self):
        if self.number_games_played == 0:
            return True
        print(self.new_game_message)
        answer = input().lower()
        while answer not in ["y", "n"]:
            print(self.wrong_format, self.new_game_message)
            answer = input().lower()
        needs_game = {"y": True, "n": False}
        return needs_game[answer]

    def run(self):
        flag = self.__run()
        self.number_games_played += flag
        return flag


class Game:
    def __init__(self, filename="games.log"):
        self.filename = filename
        self.logs = None
        self.new_game_observer = NewGameObserver()
    
    def __run(self):
        while self.new_game_observer.run():
            print(f"New game {self.new_game_observer.number_games_played}...\n")
        print("Exited from program")

    def __setup_logging(self):
        sys.stdout = Logger(self.filename)

    def run(self):
        self.__setup_logging()
        self.__run()
    

if __name__ == "__main__":
    game = Game()
    game.run()
