import Modules.battle_module


def mid_boss_event(character: dict, boss: dict) -> None:
    """
    Generate an event for when the boss HP is less than half.

    Increases boss stats and does 10 frustration damage to player.

    :param character: a dictionary
    :param boss: another dictionary
    :precondition: character must be a dictionary
    :precondition: character must have key named 'Frustration'
    :precondition: boss must be a dictionary
    :precondition: boss must have keys named 'Intelligence' and 'Speed'
    :postcondition: mulitplies the 'Intelligence' and 'Speed' stats of the boss by 10% and increases frustration by 10
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if boss is not a dictionary
    :raises KeyError: if character does not have key 'Frustration'
    :raises KeyErrr: if boss does not have keys 'Intelligence' and 'Speed'
    """
    if type(character) is not dict or type(boss) is not dict:
        raise TypeError("Character and Enemy must be dictionaries!")
    if 'Frustration' not in character or not all(key in boss for key in ['Intelligence', 'Speed']):
        raise KeyError("Character must have 'Frustration' key! Boss must have 'Intelligence' and 'Speed' keys!")

    print("You've finished making all the code for assignment 4! You bask in your achievement before a sinking "
          "realization dawns upon you.\nYou still have to unit test everything... The thought of the endless unit tests"
          " makes you more frustrated and makes Assignment 4 so much harder to complete.\nAssignment 4's stats have "
          "increased and your frustration increases by 5.")
    boss["Intelligence"] = round(boss["Intelligence"] * 1.1)
    boss["Speed"] = round(boss["Speed"] * 1.1)
    character["Frustration"] += 5


def boss_lose(character: dict, enemy: dict) -> None:
    """
    Print a message for character upon losing to boss.

    :param character: a dictionary
    :param enemy: another dictionary
    :precondition: character must be a dictionary
    :precondition: character must have key named 'Name'
    :precondition: boss must be a dictionary
    :precondition: boss must have keys named 'Name'
    :postcondition: print a message to user consoling them for their loss
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if boss is not a dictionary
    :raises KeyError: if character does not have key 'Name'
    :raises KeyError: if boss does not have keys 'Name'
    >>> character_boss_lose = {'Name': 'Bob'}
    >>> boss = {"Name": "Assignment 4"}
    >>> boss_lose(character_boss_lose, boss)
    Assignment 4 has frustrated you so much, that you just gave up. Sorry you didn't win Bob.
    You decided that life is too short to be working all the time, and you need to enjoy life.
    """
    if type(character) is not dict or type(enemy) is not dict:
        raise TypeError("Character and Enemy must be dictionaries!")
    if 'Name' not in character or 'Name' not in enemy:
        raise KeyError("Character must have 'Name' key! Enemy must have 'Name' key!")

    print(f"{enemy['Name']} has frustrated you so much, that you just gave up. Sorry you didn't win "
          f"{character['Name']}.\nYou decided that life is too short to be working all the time, and you need "
          f"to enjoy life.")


def boss_win(character: dict, enemy: dict) -> None:
    """
    Print a congratulatory message to the user after beating the boss.

    :param character: a dictionary
    :param enemy: another dictionary
    :precondition: character must be a dictionary
    :precondition: character must have key named 'Name'
    :precondition: boss must be a dictionary
    :precondition: boss must have keys named 'Name'
    :postcondition: print a message to user congratulating their win
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if boss is not a dictionary
    :raises KeyError: if character does not have key 'Name'
    :raises KeyError: if boss does not have keys 'Name'
    >>> character_boss_win = {'Name': 'Alfred'}
    >>> boss = {'Name': 'Assignment'}
    >>> boss_win(character_boss_win, boss)
    Congratulations Alfred! You've beaten Assignment and have completed the game!
    Hopefully your instructor will give you a good mark for it? Please?
    """
    if type(character) is not dict or type(enemy) is not dict:
        raise TypeError("Character and Enemy must be dictionaries!")
    if 'Name' not in character or 'Name' not in enemy:
        raise KeyError("Character must have 'Name' key! Enemy must have 'Name' key!")

    print(f"Congratulations {character['Name']}! You've beaten {enemy['Name']} and have completed the game!\nHopefully "
          f"your instructor will give you a good mark for it? Please?")


def boss_fight(character: dict) -> None:
    """
    Drive the boss fight sequence

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'
    :postcondition: Drive the battle sequence between character and the boss
    :raises TypeError: if character is not a dictionary
    :raises KeyError: if character does not have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                      'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'
    """
    if type(character) is not dict:
        raise TypeError("Character needs to be a dictionary!")
    if not all(key in character for key in ['Frustration', 'Name', 'Intelligence', 'Self-Control',
                                            'Max Frustration', 'Luck', 'Motivation', 'Fitness', 'Level']):
        raise KeyError("Character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',"
                       "'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'")

    boss = {"Name": "Assignment 4", "Frustration": 0, "Max Frustration": 100, "Intelligence": 13, "Speed": 30,
            "Self-Control": 10, "Luck": 0, 'Exp': 0}
    character_is_faster = Modules.battle_module.check_first(character, boss)
    Modules.battle_module.battle(character_is_faster, character, boss, boss["Max Frustration"] / 2)
    if character["Frustration"] < character["Max Frustration"]:
        mid_boss_event(character, boss)
    Modules.battle_module.battle(character_is_faster, character, boss, boss["Max Frustration"])
    Modules.battle_module.check_result(character, boss, boss_lose, boss_win)


def endgame(character: dict, alive: bool) -> None:
    """
    Determine if player is dead or can fight the boss.

    :param character: a dictionary describing the players stats
    :param alive: a boolean describing if the character is alive or not
    :precondition: character must be a dictionary
    :precondition: character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'
    :precondition: alive must be a boolean
    :postcondition: determine if player is alive based on alive boolean and launches boss fight if they are
    :postcondition: print a consolation message to the user if they are not alive
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if alive is not a boolean
    :raises KeyError: if character does not have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                      'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'
    """
    if type(character) is not dict or type(alive) is not bool:
        raise TypeError("Character needs to be a dictionary! Alive must be a boolean!")
    if not all(key in character for key in ['Frustration', 'Name', 'Intelligence', 'Self-Control',
                                            'Max Frustration', 'Luck', 'Motivation', 'Fitness', 'Level']):
        raise KeyError("Character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',"
                       "'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'")
    if alive:
        boss_fight(character)
    else:
        print("You lost all your motivation to finish assignment 4 and you decided that it's not worth it. It's such "
              "a nice day out right now you might as well go and enjoy life. Like a normal person...")


def main():
    """
    Drive the program.
    """
    character = {'Name': 'Bob', 'Motivation': 100, 'Frustration': 0, "Max Frustration": 500, 'Intelligence': 100,
                 'Speed': 85, "Self-Control": 5, 'Level': 3, 'Fitness': 30, 'Luck': 45, "row": 85, "column": 85}
    endgame(character, True)


if __name__ == '__main__':
    main()
