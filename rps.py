import sys
import random
import secrets
import hmac
import hashlib


class KeyGenerator:
    @staticmethod
    def generate_key():
        return secrets.token_hex(32)


class HMACCalculator:
    @staticmethod
    def calculate_hmac(key, move):
        h = hmac.new(key.encode(), move.encode(), hashlib.sha256)
        return h.hexdigest()


class Rules:
    @staticmethod
    def generate_rules(moves):
        rules = {}
        half_len = len(moves) // 2

        for i, move1 in enumerate(moves):
            for j in range(i + 1, i + half_len + 1):
                move2 = moves[j % len(moves)]
                rules[(move1, move2)] = "Win"
                rules[(move2, move1)] = "Lose"

        for move in moves:
            rules[(move, move)] = "Draw"

        return rules


class Table:
    @staticmethod
    def display_rules(moves):
        # Exclude "--help" from the list of moves
        moves = [move for move in moves if move != "--help"]

        print(
            "In this table, each cell shows the result of the move in the corresponding row against the move in the corresponding column."
        )

        header = ["v PC\\User >"] + moves
        table = [header]
        rules = Rules.generate_rules(moves)

        for move1 in moves:
            row = [move1]
            for move2 in moves:
                result = rules[(move1, move2)]
                row.append(result)
            table.append(row)

        column_widths = [
            max(len(str(row[i])) for row in table) for i in range(len(moves) + 1)
        ]
        separator = "+-" + "-+-".join(["-" * (width) for width in column_widths]) + "-+"
        print("\n" + separator)
        for row in table:
            row_str = (
                "| "
                + " | ".join(
                    str(row[i]).center(column_widths[i]) for i in range(len(row))
                )
                + " |"
            )
            print(row_str)
            print(separator)


class WinnerDeterminer:
    @staticmethod
    def determine_winner(user_move, computer_move, rules):
        if user_move == computer_move:
            return "Draw"
        elif (user_move, computer_move) in rules:
            return "User wins"
        else:
            return "Computer wins"


class Menu:
    @staticmethod
    def display_menu(moves):
        print("Menu:")
        for i, move in enumerate(moves, start=1):
            print(f"{i} - {move}")
        print("0 - Exit")

    @staticmethod
    def get_user_choice(moves):
        while True:
            user_choice = input("Select your move: ")
            if user_choice == "0":
                return None
            try:
                user_index = int(user_choice) - 1
                if 0 <= user_index < len(moves):
                    return moves[user_index]
                else:
                    print("Invalid choice. Please select a valid move.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class RPSGame:
    def __init__(self, moves):
        self.moves = moves
        self.rules = Rules.generate_rules(moves)
        self.key = KeyGenerator.generate_key()

    def play_game(self):
        computer_move = random.choice(self.moves)
        print(
            f"Computer's HMAC: {HMACCalculator.calculate_hmac(self.key, computer_move)}"
        )

        Menu.display_menu(self.moves)
        user_move = Menu.get_user_choice(self.moves)

        if user_move is None:
            return

        result = WinnerDeterminer.determine_winner(user_move, computer_move, self.rules)
        print(f"User chose: {user_move}")
        print(f"Computer chose: {computer_move}")
        print(f"Result: {result}")
        print(f"Key: {self.key}")


def main():
    moves = sys.argv[1:]

    if "--help" in sys.argv:
        if len(moves) < 3 or len(set(moves)) != len(moves):
            print("Invalid number of arguments. Provide at least 3 unique moves.")
            sys.exit(1)
        Rules.display_rules(moves)
        sys.exit(0)

    if len(moves) < 3 or len(set(moves)) != len(moves):
        print("Invalid number of arguments. Provide at least 3 unique moves.")
        sys.exit(1)

    game = RPSGame(moves)

    if len(sys.argv) < 4:
        print("Invalid number of arguments. Provide at least 3 unique moves.")
        sys.exit(1)

    game.play_game()


if __name__ == "__main__":
    main()