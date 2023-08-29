import random
import Modules.battle_module
LOCATIONS = ('Some BCIT Classroom', 'Tim Hortons', "McDonald's", 'Home',
             'Granville Station', 'Waterfront Station', 'Pacific Centre',
             'Levels Nightclub', 'Nemesis Coffee', 'Kita No Donburi')


def guessing_game(upper_bound: int) -> tuple:
    """
    Complete a guessing game by generating a pseudo-random number and having the user input a guess.

    :param upper_bound: an integer greater than 1
    :precondition: upper_bound must be an integer greater than 1
    :postcondition: a pseudo-random number is generated
    :postcondition: the user inputs a number within the specified range
    :postcondition: determines whether the user's number was the same as the number generated
    :return: True if the user guessed the generated number, else False as, and the random number, as a tuple of size 2
    """
    number = random.randint(1, upper_bound)
    guess = None
    acceptable_numbers = [number for number in range(1, upper_bound + 1)]

    while guess not in acceptable_numbers:
        try:
            guess = int(input(f"Type an integer [1, {upper_bound}]: "))
        except ValueError:
            print(f"Looks like you entered something other than an integer [1, {upper_bound}]. Try again...")
        else:
            if guess not in acceptable_numbers:
                print(f"Looks like you input a number outside the range [1, {upper_bound}]. Try again...")

    if number == guess:
        return True, number
    else:
        return False, number


def enter_room(character: dict) -> None:
    """
    Create a scenario for a player to engage with when they've entered a room in a game.

    :param character: the character, as a dictionary
    :precondition: character must be a dictionary
    :precondition: character's keys must include "Intelligence", "Luck", "Motivation", "Self-Control", "Level", "Speed",
                    "Frustration", "Max Frustration", "Fitness", "Fitness", "Name" as strings
    :postcondition: the player interacts with the room in a game
    :postcondition: a message saying the player is leaving the room is displayed
    :postcondition: the player's stats and points are displayed
    :raises ValueError: if character keys do not include the specified strings
    :raises TypeError: if the character's values of the specified strings, apart from Name, are not integers
    """

    def generate_room() -> str:
        """
        Pseudo-randomly select a room for a player to enter, in a game.

        :precondition: LOCATIONS must exist as a non-empty tuple of strings
        :precondition: the character must be in the game
        :postcondition: the room is selected for the player
        :return: the name of the room, as a string
        """
        if character["Luck"] > 35:
            room_indices = [7, 9, 4, 5, 4, 5, 1]  # more lucky rooms than not
            selection = room_indices[random.randint(0, 6)]
        else:
            selection = random.randint(0, 9)
        return LOCATIONS[selection]

    def complete_assignment() -> None:
        """
        Adjust a character's intelligence and luck points to complete an assignment in a game.

        :precondition: the character must be a dictionary
        :precondition: the character must contain "Intelligence" and "Luck" as keys, as strings
        :precondition: the values of "Intelligence" and "Luck" in character must be integers
        """
        character["Intelligence"] += 5
        character["Luck"] -= 2

    def event_happens(description: str, chance: int, event: str) -> None:
        """
        Generate the event in a room for a player to interact with in a game.

        :param description: the description of the room, as a string
        :param chance: the denominator of the fraction of chance an event will happen in the room, as an integer
        :param event: the event that might happen in that room
        :precondition: description must be one of the strings in the global tuple LOCATIONS
        :precondition: chance must be an integer
        :precondition: event must be a string
        :postcondition: the player interacts with the room
        """
        print(f"You're in {description}. There is a 1/{chance} chance you will {event} if you enter one of the listed "
              f"numbers.")

        guess = guessing_game(chance)

        if guess[0]:
            print(f"You KNEW this would happen! You {event}.")
            if event == 'get assigned ANOTHER assignment':
                complete_assignment()
            elif event == 'have to fight':
                Modules.battle_module.battle_sequence(character)
            elif event == 'gain motivation':
                character["Motivation"] += 2
            elif event == 'lose self-control':
                character["Self-Control"] -= 2
        else:
            print(f"The number was {guess[1]}.\nYou did not {event}. As you were...")

    def raise_errors() -> None:
        """
        Raise errors if a character does not contain certain keys, or if the corresponding values are not integers.

        :postcondition: determines whether errors need to be raised based on the keys and valyes in a character
        :raises ValueError: if character keys do not include the right keys as strings
        :raises TypeError: if certain of the character's key values are not integers
        """
        needed_keys = ["Intelligence", "Luck", "Motivation", "Self-Control", "Level", "Speed",
                       "Max Frustration", "Fitness", "Name"]
        for key in needed_keys:
            if key not in character.keys():
                raise ValueError("Your character is missing one or more essential attributes!")
        for key in needed_keys[:-1]:
            if type(character[key]) != int:
                raise TypeError("Your attribute values in your character must be integers!")

    raise_errors()

    room = generate_room()

    if room == LOCATIONS[0] or room == LOCATIONS[3]:
        event_happens(room, 3, 'get assigned ANOTHER assignment')

    elif room in [LOCATIONS[1], LOCATIONS[2], LOCATIONS[8], LOCATIONS[9]]:
        event_happens(room, 2, 'have to fight')

    elif room == LOCATIONS[6] or room == LOCATIONS[7]:
        event_happens(room, 3, 'lose self-control')

    else:
        event_happens(room, 3, 'gain motivation')

    print(f"You are now leaving {room}.\nHere's what your points and stats look like:\n{character}")


def get_row_coordinate(character: dict, move: str) -> int:
    """
    Get the row value for a character based on the move being validated or made.

    :param character: a dictionary
    :param move: the direction of the move, as a string 'n' or 's'
    :precondition: character must be a dictionary
    :precondition: character must contain keys "row"
    :precondition: move must be a string of size 1, either 'n' or 's'
    :postcondition: assigns a new column value to the character based on the move
    :return: the new coordinate, as an integer
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if move is not a string
    :raises ValueError: if move is not 'n' or 's'
    :raises KeyError: if character does not contain key "row"
    >>> get_row_coordinate({"row": 0, "column": 0}, 's')
    1
    >>> get_row_coordinate({"row": 5, "column": 3}, 'n')
    4
    >>> get_row_coordinate({"row": 0, "column": 5}, 'n')
    -1
    """
    if type(move) != str or type(character) != dict:
        raise TypeError("Character must be a dict! Move must be a string!")
    if move != 'n' and move != 's':
        raise ValueError("You can only use 'n' or 's' to validate or change the row coordinate")
    if move == 'n':
        return character["row"] - 1
    elif move == 's':
        return character["row"] + 1


def get_column_coordinate(character: dict, move: str) -> int:
    """
    Get the column value for a character based on the move being validated or made.

    :param character: a dictionary
    :param move: the direction of the move, as a string 'e' or 'w'
    :precondition: character must be a dictionary
    :precondition: move must be a string of size 1, either 'e' or 'w'
    :postcondition: assigns a new row value to the character based on the move
    :return: the new coordinate, as an integer
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if move is not a string
    :raises ValueError: if move is not 'e' or 'w'
    :raises KeyError: if character keys do not contain "column"
    >>> get_column_coordinate({"row": 0, "column": 0}, 'e')
    1
    >>> get_column_coordinate({"row": 5, "column": 3}, 'w')
    2
    >>> get_column_coordinate({"row": 6, "column": 0}, 'w')
    -1
    """
    if type(move) != str or type(character) != dict:
        raise TypeError("Character must be a dict! Move must be a string!")
    if move != 'e' and move != 'w':
        raise ValueError("You can only use 'e' or 'w' to validate or change the column coordinate")
    if move == 'e':
        return character["column"] + 1
    elif move == "w":
        return character["column"] - 1


def keep_checking_move(board: tuple, character: dict) -> str:
    """
    Ensure the user enters an appropriate direction, and that the direction is a valid move.

    :param board: a tuple of sub-tuples of size 2 of the board's boundaries
    :param character: a dictionary
    :precondition: board must be a tuple of sub-tuples of size 2
    :precondition: character must be a dict
    :precondition: character must be on the board
    :postcondition: validates the move in the chosen direction
    :postcondition: ensures that the move is only 'n', 's', 'e', or 'w'
    :return: the direction of the valid move, as a string 'n', 's', 'e', or 'w'
    :raises TypeError: if board is not a tuple
    :raises TypeError: if character is not a dictionary
    """

    def get_user_choice() -> str:
        """
        Print a numbered list of directions and ask the user to enter the direction they wish to travel.

        :postcondition: the string prompt for user input is printed
        :postcondition: the user decides and types which direction to go next
        :return: the direction the user wishes to travel, as a string ('n', 's', 'e', or 'w')
        :raises ValueError: if direction is not 'n', 's', 'e', or 'w'
        """
        user_choice = input(f"Enter the direction you wish to go (n, s, e, or w): ")
        if user_choice != 'n' and user_choice != 's' and user_choice != 'w' and user_choice != 'e':
            raise ValueError
        return user_choice

    def validate_move(bounds: tuple, move: str) -> bool:
        """
        Check that a character's move in a particular direction lands on the board of a game being played.

        :param bounds: a tuple of the board boundaries
        :param move: the direction, as a string, either 'n', 's', 'e', or 'w'
        :precondition: bounds must be a tuple
        :precondition: move must be a string, either 'n', 's', 'e', or 'w'
        :postcondition: determines whether a character's move in a particular direction lands on the playing board
        :return: True if the move falls within the board, else False
        :raises TypeError: if bounds is not a tuple
        :raises TypeError: if move is not a string
        :raises ValueError: if move is not 'n', 's', 'e', or 'w'
        """
        if type(bounds) != tuple or type(move) != str:
            raise TypeError("You have passed an argument of the wrong type. Please check the function documentation!")
        if move not in ['n', 's', 'e', 'w']:
            raise ValueError("You have passed an invalid move argument to validate_move")

        row, column = character["row"], character["column"]

        if move == "n" or move == "s":
            row = get_row_coordinate(character, move)
        elif move == 'e' or move == 'w':
            column = get_column_coordinate(character, move)

        if bounds[0][0] <= row < bounds[0][1] and bounds[1][0] <= column < bounds[1][1]:
            return True
        else:
            print(f"Your move must stay within the bounds of the board!")
            return False

    if type(board) != tuple or type(character) != dict:
        raise TypeError

    choice_is_valid = False
    direction = None
    while not choice_is_valid:
        try:
            direction = get_user_choice()
        except ValueError:
            print(f"Direction must be 'n', 's', 'e', or 'w'!")
        else:
            choice_is_valid = validate_move(board, direction)
    return direction


def move_character(board: tuple, character: dict) -> None:
    """
    Move a character north, south, east, or west within a game board.

    :param board: the game board, as a tuple containing row and column boundaries as sub-tuples of size 2
    :param character: a dictionary
    :precondition: character must be a dictionary that contains keys "row" and "column" with integers as values
    :precondition: character must contain a key "Luck" which has an integer value
    :postcondition: the user enters a direction 'n', 's', 'e', or 'w' to move
    :postcondition: updates the character's row or column based on the move chosen by the user
    :raises TypeError: if board is not a tuple
    :raises TypeError: if character is not a dict
    :raises ValueError: if "Luck" is not a key in character
    :raises ValueError: if the value of "Luck" in character is not an integer
    :raises ValueError: if row is not a key in character
    :raises ValueError: if column is not a key in character
    :raises TypeError: if row or column values in character are not integers
    """
    if type(board) != tuple or type(character) != dict:
        raise TypeError("Board must be a tuple! Character must be a dict!")

    if "Luck" not in character.keys() or type(character["Luck"]) != int:
        raise ValueError("Your character must have a key called 'Luck' with an integer value!")

    if "row" not in character.keys() or "column" not in character.keys():
        raise ValueError("Your character must contain 'row' and 'column as keys")

    if type(character["row"]) != int or type(character["column"]) != int:
        raise TypeError("Your row and column keys must have integers as values in character!")

    direction = keep_checking_move(board, character)

    if direction == "n" or direction == "s":
        character["row"] = get_row_coordinate(character, direction)
    elif direction == 'e' or direction == 'w':
        character["column"] = get_column_coordinate(character, direction)


def make_board(rows: int, columns: int) -> tuple:
    """
    Create the bounds of a board for a game, lower bound inclusive, upper bound exclusive.

    :param rows: an integer 2 or greater
    :param columns: an integer 2 or greater
    :precondition: rows must be an integer 2 or greater
    :precondition: columns must be an integer 2 or greater
    :postcondition: creates the bounds of a board for a game, lower bound inclusive, upper bound exclusive
    :return: the boundaries of the board, as a tuple with 2 sub-tuples that give the row and column bounds respectively
    :raises ValueError: if rows < 2
    :raises ValueError: if columns < 2
    >>> board = make_board(5, 5)
    >>> board
    ((0, 5), (0, 5))
    >>> board = make_board(95, 3)
    >>> board
    ((0, 95), (0, 3))
    """
    if rows < 2 or columns < 2:
        raise ValueError("Dimensions must be 2 or greater")
    boundaries = ((0, rows), (0, columns))
    return boundaries


def initialize_game(game_board: tuple, character: dict) -> tuple:
    """
    Initialize a game.

    Create a board, create a character, and print an explanatory welcome messsage.

    :param game_board: the board, as a tuple of row and column boundaries
    :param character: the character, as a dictionary
    :precondition: game_board must be a tuple with 2 sets of row/column coordinates
    :precondition: character must be a dictionary
    :precondition: character must have a "Name" key with a string as a value
    :postcondition: creates a board
    :postcondition: creates a character
    :postcondition: prints an explanatory welcome message
    :return: the board and player as two elements within a tuple
    :raises TypeError: if game_board is not a tuple
    :raises TypeError: if player is not a dict
    :raises KeyError: if "Name" does not exist as a key within character
    >>> game = initialize_game(((0, 5), (0,5)), {"Name": "Chris"})
    Welcome to the game, Chris! You are on MISSION: COMPLETE ASSIGNMENT 4.
    You're at the end of your first term in CST and things have been hectic as HECK.
    But don't worry, we know you can do it!
    Your mission is to stay Motivated enough to stay alive, achieve enough Fitness level to defeat the final boss, and
    make it to the last square of the board for the final battle...
    >>> game
    (((0, 5), (0, 5)), {'Name': 'Chris'})

    >>> game = initialize_game(((0, 7), (0, 9)), {"Name": "Newton"})
    Welcome to the game, Newton! You are on MISSION: COMPLETE ASSIGNMENT 4.
    You're at the end of your first term in CST and things have been hectic as HECK.
    But don't worry, we know you can do it!
    Your mission is to stay Motivated enough to stay alive, achieve enough Fitness level to defeat the final boss, and
    make it to the last square of the board for the final battle...
    >>> game
    (((0, 7), (0, 9)), {'Name': 'Newton'})
    """
    if type(game_board) != tuple or type(character) != dict:
        raise TypeError("Your board must be a tuple and your player must be a dictionary!")
    message = "Welcome to the game, {character['Name']}! You are on MISSION: COMPLETE ASSIGNMENT 4.\nYou're at the end of your first term in CST and things have been hectic as HECK.\nBut don't worry, we know you can do it!\nYour mission is to stay Motivated enough to stay alive, achieve enough Fitness level to defeat the final boss, and\nmake it to the last square of the board for the final battle..."
    return {"board_output": game_board, "character_output": character, "message": message}


def main():
    """
    Drive the program.
    """


if __name__ == "__main__":
    main()
