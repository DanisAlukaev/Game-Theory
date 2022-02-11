import sys
from enum import Enum
import random
from turtle import pos, position
from tqdm import tqdm


class Mode(Enum):
    SMART = 0
    RANDOM = 1
    ADVISOR = 2


class Turn(Enum):
    DUPLICATOR = 1
    SPOILER = -1


class Logger:
    """
    The class used to log the progress of the game.
    Allows to redirect stdout to specified file: the result of method print will
    be both displayed in the terminal and appended to log file.
    """

    def __init__(self, filename='games.log'):
        self.filename = filename
        self.log = open(filename, 'a')
        self.cli = sys.stdout
    
    def write(self, string):
        self.cli.write(string)
        self.log.write(string)
    
    def flush(self):
        pass


class Analyzer:
    """
    The class used to determine the positions with a winning strategy (acceptable positions). 
    Implements backward induction for Finite Position Game(FPG).
    Iteratively check whether there exists possible move (p, q), s.t.
    q is not a final position, and any opponent move leads to winning strategy.
    """

    def __init__(self, day, month, year):
        self.day, self.month, self.year = day, month, year
        self.winning_position = day + month + year

        self.possible_moves = range(1, day + month + 1)
        self.acceptable_positions = [self.winning_position - move for move in self.possible_moves]
        self.suggested_moves = {position: [] for position in range(1, self.winning_position)}

        self.message_analyzing = "Analyzing the game..."
        self.message_no_winning_strategy = "\nYou don't have any winning strategy. Return random move."
        self.__run()
    
    def __run(self):
        fix_points = self.acceptable_positions[:]
        offsets = {i: [i + j for j in self.possible_moves] for i in self.possible_moves}
        for position, move in zip(self.acceptable_positions, self.possible_moves):
            self.suggested_moves[position].append(move)

        print(self.message_analyzing)
        for position in tqdm(range(1, self.winning_position)[::-1]):
            if position in self.acceptable_positions:
                continue
            for move in self.possible_moves:
                move_offsets = offsets[move]
                if position + move in self.acceptable_positions:
                    continue
                positions_fixed = True
                for offset in move_offsets:
                    if not position + offset in fix_points:
                        positions_fixed = False
                if positions_fixed:
                    fix_points.append(position)
                    self.suggested_moves[position].append(move)

        self.acceptable_positions = fix_points
        return fix_points
    
    def suggest_move(self, position):
        if self.suggested_moves[position]:
            return random.choice(self.suggested_moves[position]), True
        return random.choice(self.possible_moves), self.message_no_winning_strategy


def prompt_string(message, warning, answers):
    print(message)
    answer = input().lower()
    while answer not in answers:
        print(warning, message)
        answer = input().lower()
    return answer


def prompt_numeric(message, warning, interval):
    print(message)
    answer = input()
    while not answer.isnumeric() or int(answer) not in interval:
        print(warning, message)
        answer = input()
    return int(answer)


class Configuration:
    """
    The class used to configure game routines such as prompting the user, setting up logging, etc.
    Can be used as a base class for new FPG games.
    """

    def __init__(self, day, month, year, filename="games.log"):
        self.day, self.month, self.year = day, month, year
        self.filename = filename

        self.number_games_played = 0
        self.winning_position = day + month + year
        self.possible_moves = range(1, day + month + 1)
        self.starting_position = None
        self.mode = None

        self.message_play_again = "\nDo you want to play again? [Y/N]"
        self.message_wrong_answer_polar_question = "\nThe answer is either 'Y' or 'N'.\nTry again:"

        self.message_ask_option_starting_position = "Select starting position at random? [Y/N]"
        self.message_ask_starting_position = f"\nSpecify starting position in the range [{1}..{self.winning_position-1}]"
        self.message_wrong_starting_position = f"\nThe starting position should be numeric and belong to [{1}..{self.winning_position-1}]. Try again:"

        self.message_current_position = "\nCurrent position is "
        self.message_ask_move = f". Choose a move in the range of [{1}..{max(self.possible_moves)}]."
        self.message_wrong_move = f"\nThe move should be numeric and belong to [{1}..{max(self.possible_moves)}]. Try again:"
        self.message_impossible_position = f'Impossible position, it should belong to [1..{self.winning_position}].\n'

        self.message_ask_mode = "\nChoose the playing mode [1,2,3]:\n"
        self.message_smart_move = "[1] Smart (program uses a winning strategy)\n"
        self.message_random_move = "[2] Random (program makes random moves)\n"
        self.message_advisor_mode = "[3] Advisor (program advises a winning strategy)"
        self.message_wrong_mode = "\nThe answer is either '1', '2' or '3'. Try again:"

        self.__setup_logging()

    def __setup_logging(self):
        sys.stdout = Logger(self.filename)

    def __start(self):
        needs_game = {"y": True, "n": False}
        if self.number_games_played == 0:
            answer = "y"
        else:
            answer = prompt_string(self.message_play_again, self.message_wrong_answer_polar_question, ["y", "n"])
        self.number_games_played += needs_game[answer]
        return needs_game[answer]

    def __configure_starting_position(self):
        answer = prompt_string(self.message_ask_option_starting_position, self.message_wrong_answer_polar_question, ["y", "n"])
        if answer == "y":
            return random.randint(1, self.winning_position - 1)
        answer = prompt_numeric(self.message_ask_starting_position, self.message_wrong_starting_position, range(1, self.winning_position))
        self.starting_position = answer
        return self.starting_position

    def __configure_playing_mode(self):
        message = self.message_ask_mode + self.message_smart_move + self.message_random_move + self.message_advisor_mode
        mode = {'1': Mode.SMART, '2': Mode.RANDOM, '3': Mode.ADVISOR}
        answer = prompt_string(message, self.message_wrong_mode, ['1', '2', '3'])
        self.mode = mode[answer]
        return self.mode

    def configure(self):
        self.starting_position = self.__configure_starting_position()
        self.playing_mode = self.__configure_playing_mode()
        return self.starting_position, self.playing_mode

    def start(self):
        return self.__start()

    def __str__(self):
        return f"""\n----------CONFIGURATIONS----------\n
Possible positions:\t[1..{self.winning_position - 1}]
Possbile moves:\t\t[1..{self.day + self.month}]
Starting position:\t{self.starting_position}
Final position:\t\t{self.winning_position}
Playing mode:\t\t{self.mode.name}\n
----------------------------------\n"""

class Spoiler:
    """
    Class implementing opponent's behaviour. 
    Primarily, has 2 modes: 'smart' when the program uses winning strategy against the user, and
    'random' when it makes random moves. The 'advisor' mode applies the 'smart' strategy.
    """

    def __init__(self, analyzer):
        self.mode = None
        self.analyzer = analyzer

    def set_mode(self, mode):
        self.mode = mode
    
    def make_move(self, position):
        routines = {
            Mode.SMART: self.__smart_mode, 
            Mode.RANDOM: self.__random_mode,
            Mode.ADVISOR: self.__smart_mode, 
        }
        move = routines[self.mode](position)
        while position + move > self.analyzer.winning_position:
            move = routines[self.mode](position)
        return move
    
    def __smart_mode(self, position):
        move, success = self.analyzer.suggest_move(position)
        return move
        
    def __random_mode(self, position):
        random.seed(position)
        return random.choice(self.analyzer.possible_moves)


class Game(Configuration):
    def __init__(self, day=12, month=11, year=2001):
        # TODO: logging for each game

        Configuration.__init__(self, day, month, year)
        self.position = None
        self.spoiler = None
        self.analyzer = None

    def __prompt_move(self, position):
        message = ''.join([self.message_current_position, str(position), self.message_ask_move])
        if self.spoiler.mode == Mode.ADVISOR:
            suggestion, success = self.analyzer.suggest_move(position)
            if isinstance(success, str):
                message += success
            message += f" Advisor suggestion is +{suggestion}."
        answer = prompt_numeric(message, self.message_wrong_move, range(1, max(self.possible_moves) + 1))
        while position + answer > self.analyzer.winning_position:
            message = self.message_impossible_position + message
            answer = prompt_numeric(message, self.message_wrong_move, range(1, max(self.possible_moves) + 1))
        return answer
    
    def __start_session(self):
        turn = Turn.DUPLICATOR
        make_move = {Turn.DUPLICATOR: self.__prompt_move, Turn.SPOILER: self.spoiler.make_move}
        player = {Turn.DUPLICATOR: "Duplicator", Turn.SPOILER: "Spoiler"}
        while True:
            move = make_move[turn](self.position)
            self.position += move
            print(f"\n{player[turn]} makes move +{move}: {self.position - move} -> {self.position}")
            if self.position == self.winning_position:
                print(f"{player[turn]} wins!")
                break
            turn = Turn(-turn.value)

    def __run(self):
        try:
            self.analyzer = Analyzer(self.day, self.month, self.year)
            self.spoiler = Spoiler(self.analyzer)
            while self.start():
                print(f"\nGame session #{self.number_games_played} started.")
                self.position, mode = self.configure()
                print(self.__str__())
                self.spoiler.set_mode(mode)
                self.__start_session()
        except KeyboardInterrupt:
            pass

        print("\nThe program was terminated.")

    def run(self):
        self.__run()
    

if __name__ == "__main__":
    game = Game()
    game.run()
