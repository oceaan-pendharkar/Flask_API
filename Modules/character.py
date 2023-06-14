"""
Oceaan Pendharkar A01253605
Martin Siu A01352270
"""
import itertools


def populate_custom_points(character: dict, points: int) -> None:
    """
    Add points to a selection of attributes of a character based on user input.

    :param character: a dictionary of attributes as strings for keys and integers for values
    :param points: a positive integer
    :precondition: character must be a dictionary
    :precondition: character's attributes must have integer values
    :precondition: to exit the function, the user MUST enter values other than zero
    :postcondition: adds points to the character's attributes
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if points is not an integer
    """
    if type(character) != dict or type(points) != int:
        raise TypeError("Character must be a dict! Points must be an int!")
    key_generator = itertools.cycle([key for key in character.keys() if key not in ["Name", "row", "column",
                                                                                    "Fitness", "Level", "alive",
                                                                                    "goal achieved", "Frustration"]])

    while points > 0:
        key = next(key_generator)
        point_increase = 0
        try:
            point_increase = int(input(f"How many points do you want to add to your {key}?"))
        except ValueError as e:
            print(e)

        if type(character[key]) == int:
            character[key] += point_increase
            points -= point_increase

        if points == 0:
            print(f"You've used all your points!")

        elif points < 0:
            print(f"Woah there, that was more points than we said!! \nSince you cheated, that's all the points you "
                  "get for now. \nAnd you can forget about getting points for the category you just over-filled. "
                  "\nThat's not how operation COMPLETE ASSIGNMENT 4 works...")
            character[key] -= point_increase
        print(f"You have {points} points left to distribute between your attributes.")


def make_preset_character(character: dict) -> None:
    """
    Give 10 extra points to a character in one attribute, depending on the selection.

    :param character: a dictionary with attributes as strings for keys and integers for values
    :precondition: character must be a dictionary
    :precondition: character's attributes must have zero as values to begin with
    :postcondition: adds 120 points total to the character's attributes
    :postcondition: the user selects 'n', 'l', 'g', or 'j' (otherwise will loop forever)
    :postcondition: the character's attribute is given 10 points based on the user's selection
    :raises TypeError: if character is not a dict
    """
    if type(character) != dict:
        raise TypeError("Character must be a dictionary! Selection must be a string!")
    selection = None
    while selection not in ['n', 'l', 'g', 'j']:
        selection = input(f"That's cool, we have a few preset categories. Type the first letter of the "
                          f"character type to select it.\nnerd: has a lot of intelligence, obviously(n)\n"
                          f"leprechaun: has a lot of luck, obviously(l)\ngreat ape: has a lot of self control "
                          f"(maybe not obvious) (g)\njock: has a lot of speed(j) ")
        if selection == 'n':
            character["Intelligence"] += 10
        elif selection == 'l':
            character["Luck"] += 10
        elif selection == 'g':
            character["Self-Control"] += 10
        elif selection == 'j':
            character["Speed"] += 10
        else:
            print(f"You must enter 'n', 'l', 'g', or 'j'. Try again...")


def create_character() -> dict:
    """
    Create a character.

    :postcondition: creates a character, as a dictionary of attributes as keys and values
    :return: the character, as a dictionary
    """
    character = {"Motivation": 80, "Max Frustration": 60, "Self-Control": 5, "Intelligence": 5, "Luck": 5, "Speed": 5,
                 "Fitness": 5, 'Name': input("What's your character's name? "), "row": 0, "column": 0, "Level": 1,
                 "alive": True, "goal achieved": False, "Frustration": 0}
    choice = None
    while choice != 'y' and choice != 'n':
        choice = input(f"Would you like to choose the categories to which you want to distribute your 10 points? y/n ")
        if choice == 'y':
            print(f"Alright! Here are your base stats:\n{character}\nYou have ***10 points*** to distribute between "
                  "Motivation, Max Frustration, Self-Control, Intelligence, Luck, and Speed.\nMotivation: helps you "
                  "stay alive\nMax Frustration: the higher this is, the longer you last in battle\nSelf-Control: like "
                  "defense\nIntelligence: helps you damage your enemies\nLuck: determines how likely you are to meet "
                  "difficult opponents\nSpeed: helps you be quicker than your enemies!\nYou also have Fitness, which "
                  "keeps track of your experience level (0 for now!).")
            populate_custom_points(character, 10)

        elif choice == 'n':
            make_preset_character(character)
        else:
            print(f"You entered something other than 'y' or 'n'. Try again...")
    return character


def check_alive(character: dict) -> bool:
    """
    Check to see if a character's motivation has dropped to or below zero in a game.

    :param character: the character, as a dictionary
    :precondition: character must be a dictionary
    :precondition: character must contain the keys "Motivation" and "alive" as strings
    :precondition: the value of character["Motivation"] must be an integer
    :return: True if alive, else False
    :raises TypeError: if character is not a dictionary
    :raises ValueError: if character does not contain the keys "Motivation" or "alive"
    :raises TypeError: if character["Motivation"] is not an integer
    >>> my_guy = {"Motivation": 0, "alive": True}
    >>> check_alive(my_guy)
    False
    >>> my_guy = {"Motivation": 50, "alive": True}
    >>> check_alive(my_guy)
    True
    """
    if type(character) != dict:
        raise TypeError("Character must be a dictionary to call check_alive!")
    if "Motivation" not in character.keys() or "alive" not in character.keys():
        raise ValueError("Character must have 'Motivation' and 'alive' keys to check if they're alive!")
    if type(character["Motivation"]) != int:
        raise TypeError("character['Motivation'] must be an integer!")

    if character["Motivation"] <= 0:
        return False
    else:
        return True


def check_goal(character: dict, board: tuple) -> None:
    """
    Check that a character has a high enough fitness level and has reached the correct square to defeat the boss.

    :param character: a dictionary
    :param board: a tuple with boundaries of a board as two sub-tuples of size 2
    :precondition: character must be a dictionary
    :precondition: character must contain the keys "column", "row", "Fitness", and "Name", as strings
    :precondition: values for keys "column", "row", "Fitness", and "Name" in character must be integers
    :postcondition: displays the character's progress towards their goal if their fitness level is 30 or higher or
                    if they've found the final square
    :postcondition: updates "goal achieved" attribute of character if Fitness >= 30 and coordinates = (9, 9)
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if board is not a tuple
    :raises ValueError: if character does not contain the keys "column", "row", "Fitness", or "Name"
    :raises TypeError: if character's values at "column", "row", "Fitness" are not integers
    :raises IndexError: if board is a tuple less than size 2
    >>> my_player = {"row": 0, "column": 0, "Motivation": 2, "Fitness": 2, "Name": "Player"}
    >>> check_goal(my_player, ((0, 9), (0, 9)))

    >>> my_player = {"row": 8, "column": 8, "Motivation": 2, "Fitness": 30, "Name": "Player"}
    >>> check_goal(my_player, ((0, 9), (0, 9)))
    Nice job, Player. You've reached the final square and you're ready to defeat the final boss!!!
    >>> my_player = {"row": 8, "column": 8, "Motivation": 2, "Fitness": 20, "Name": "Buzz"}
    >>> check_goal(my_player, ((0, 9), (0, 9)))
    Hey there, Buzz, you've found the final square, but you aren't ready to defeat the boss yet! Keep trucking...
    """
    if type(character) != dict or type(board) != tuple:
        raise TypeError("Character must be a dictionary and board must be a tuple to call check_goal!")
    for key in ["column", "row", "Fitness", "Name"]:
        if key not in character.keys():
            raise ValueError("Character does not contain all necessary keys to check_goal!")
    for key in ["column", "row", "Fitness"]:
        if type(character[key]) != int:
            raise TypeError("Character's column, Fitness, and row must all have integer values!")

    if character["Fitness"] >= 30 and (character["row"] + 1, character["column"] + 1) == (board[0][1], board[1][1]):
        print(f"Nice job, {character['Name']}. You've reached the final square and you're ready to defeat the final "
              f"boss!!!")
        character["goal achieved"] = True
    elif character["Fitness"] >= 30 and (character["row"] + 1, character["column"] + 1) != (board[0][1], board[1][1]):
        print(f"Alright, {character['Name']}. You've got enough fitness points to defeat the final boss! Make your "
              f"way to the final square for the final battle...")
    elif character["Fitness"] < 30 and (character["row"] + 1, character["column"] + 1) == (board[0][1], board[1][1]):
        print(f"Hey there, {character['Name']}, you've found the final square, but you aren't ready to defeat the "
              f"boss yet! Keep trucking...")


def check_vitals(character: dict, board: tuple) -> None:
    """
    Check if a character is alive and whether they have achieved their goal

    :param character: a dictionary containing the keys "Name", "row", "column", "Fitness", and "Motivation", as strings
    :param board: a tuple with boundaries of a board as two sub-tuples of size 2
    :precondition: board must be a tuple
    :precondition: character must be a dictionary
    :precondition: character must contain the keys "Name", "row", "column", "Fitness", "Motivation", "alive" as strings
    :precondition: character's values at keys "row", "column", "Fitness", and "Motivation" must be integers
    :return: True if character is still in the game, else False
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if board is not a tuple
    :raises TypeError: if character values at specified keys are not integers
    :raises ValueError: if character does not contain specified keys
    >>> my_player = {"row": 0, "column": 0, "Motivation": 2, "Fitness": 2, "Name": "Player", "alive": True}
    >>> check_vitals(my_player, ((0, 2), (0, 2)))

    >>> my_guy = {"Motivation": 0, "alive": True, "row": 5, "column": 9, "Fitness": 30, "Name": "Bob"}
    >>> check_vitals(my_guy, ((0, 9), (0, 9)))
    Sorry, you lost all your motivation... you're basically dead. Have fun in the afterlife!
    >>> my_player = {"row": 8, "column": 8, "Motivation": 20, "Fitness": 20, "Name": "Buzz", "alive": True}
    >>> check_vitals(my_player, ((0, 9), (0, 9)))
    Hey there, Buzz, you've found the final square, but you aren't ready to defeat the boss yet! Keep trucking...
    """
    keys = ["Name", "alive", "row", "column", "Fitness", "Motivation"]
    if type(character) != dict or type(board) != tuple:
        raise TypeError("Character must be a dictionary! Board must be a tuple!")

    for key in keys:
        if key not in character.keys():
            raise ValueError('Character must contain keys "Name", "row", "column", "Fitness", "Motivation", "alive"!')

    keys_with_int_values = keys[2:]
    for key in keys_with_int_values:
        if type(character[key]) != int:
            raise TypeError("One or more of the specified keys do not have integer values!")

    alive = check_alive(character)
    if alive:
        check_goal(character, board)
    else:
        character["alive"] = False
        print(f"Sorry, you lost all your motivation... you're basically dead. Have fun in the afterlife!")


def main():
    """
    Drive the program.
    """


if __name__ == "__main__":
    main()
