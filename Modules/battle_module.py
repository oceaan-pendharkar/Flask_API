"""
Oceaan Pendharkar A01253605
Martin Siu A01352270
"""
import random
import copy
import Modules.character


def determine_enemy(level: int) -> dict:
    """
    Select enemy from list of enemies.

    :parameter level: an integer
    :precondition: level must be a positive integer
    :postcondition: randomly selects and returns a copy of enemy from a dictionary of preset enemy dictionaries
    :return: a copy of the randomly selected enemy dictionary
    :raises TypeError: if level is not an integer
    :raises ValueError: if level is not positive
    """
    if type(level) is not int:
        raise TypeError("Level must be an integer!")
    if level <= 0:
        raise ValueError("Level must be a positive integer!")

    enemies = {1: {'Name': 'Chicken Sandwich', 'Description': 'On the table lies a delicious chicken sandwich. The '
                                                              'crisp, juicy, and tender chicken strips lie between 2 '
                                                              'slices of freshly baked bread. You can feel the '
                                                              'growling in our stomach drawing you towards it...',
                   'Frustration': 0, 'Max Frustration': 18, 'Intelligence': 21, 'Speed': 5, "Self-Control": 3,
                   "Luck": 0, "Exp": 4},
               2: {'Name': 'Donut', 'Description': 'You can see a donut on display by the front counter. The glaze '
                                                   'on top of the donut glistens in the light, tempting you towards '
                                                   'its sweetness.',
                   'Frustration': 0, 'Max Frustration': 11, 'Intelligence': 19, 'Speed': 3, "Self-Control": 7,
                   "Luck": 0, "Exp": 5},
               3: {'Name': 'Latte', 'Description': 'Looking at the menu, you dream about holding a warm latte in your '
                                                   'hands. The scent of the tea and milk fills your mind and you can'
                                                   'almost taste the contrast of the smooth milky foam and the '
                                                   'green tea under it. Will you end up ordering it?',
                   'Frustration': 0, 'Max Frustration': 14, 'Intelligence': 24, 'Speed': 11, "Self-Control": 1,
                   "Luck": 0, "Exp": 5},
               4: {'Name': 'Breakfast Sandwich', 'Description': 'You see someone eating a warm breakfast sandwich '
                                                                'through the window. The perfectly cooked egg, crispy'
                                                                'bacon and melted cheese beckon you towards the store.',
                   'Frustration': 0, 'Max Frustration': 25, 'Intelligence': 15, 'Speed': 4, "Self-Control": 3,
                   "Luck": 0, "Exp": 4},
               5: {'Name': 'Hashbrowns', 'Description': 'The thought of hashbrowns fill your mind. From the satisfying '
                                                        'crunch of the potatoes to the savory flavors of the potatoes'
                                                        'your body craves for a rest to indulge in this fried '
                                                        'delicacy.',
                   'Frustration': 0, 'Max Frustration': 20, 'Intelligence': 20, 'Speed': 4, "Self-Control": 3,
                   "Luck": 0, "Exp": 3},
               6: {'Name': 'Soft Drink', 'Description': 'A cold soft drink sits on the counter here. The fizzing of '
                                                        'the bubble reaches your ears, inviting you to partake in the '
                                                        'sweet beverage. You resist its temptation as you try to pop'
                                                        'your cravings.',
                   'Frustration': 0, 'Max Frustration': 18, 'Intelligence': 20, 'Speed': 6, "Self-Control": 2,
                   "Luck": 0, "Exp": 3},
               7: {'Name': 'Muffin', 'Description': 'The aroma of freshly baked muffins hits you. You think of the '
                                                    'golden brown exterior of the muffin, and its soft fruity interior. '
                                                    'You wonder if you should sit down and enjoy this breakfast treat.',
                   'Frustration': 0, 'Max Frustration': 16, 'Intelligence': 19, 'Speed': 4, "Self-Control": 5,
                   "Luck": 0, "Exp": 4},
               8: {'Name': 'Ice Cream', 'Description': 'As you watch someone eat their delicious ice cream cone, you '
                                                       'imagine the smooth, creamy texture of it. The sweet milky'
                                                       'flavor of the ice cream mixed with whatever flavor you desire. '
                                                       'Vanilla, chocolate, and oreo, it could all be yours...',
                   'Frustration': 0, 'Max Frustration': 20, 'Intelligence': 21, 'Speed': 6, "Self-Control": 4,
                   "Luck": 0, "Exp": 3}}

    selector = random.randint(1, len(enemies))
    enemy = copy.deepcopy(enemies[selector])
    for key, value in enemy.items():
        if key not in ["Name", "Description", "Frustration", "Exp"]:
            increased_stat = value * (1 + level * 0.1)
            enemy[key] = round(increased_stat)
    print(enemies[selector]['Description'])
    return enemy


def luck_roll(luck: int, lower: int, upper: int, luck_multiplier=0) -> int:
    """
    Determine the number of a roll with luck modifiers.

    Randomly generates a number for a roll and adds on luck modifiers to the roll.

    :param luck: an integer
    :param lower: another integer
    :param upper: another integer
    :param luck_multiplier: a number, default is 0
    :precondition: luck must be an integer
    :precondition: lower must be an integer
    :precondition: upper must be an integer greater than or equal to lower
    :precondition: luck_multiplier must a number, either a float or an int
    :precondition: if no argument is passed for luck_multiplier, default value is 0
    :postcondition: generates and returns a number that is randomly between lower and upper inclusive and
                    adds a luck multiplier to the number
    :return: the random number as an int
    :raises TypeError: if luck is not an integer
    :raises TypeError: if lower is not an integer
    :raises TypeError: if upper is not an integer
    :raises TypeError: if luck_multiplier is not an integer or a float
    :raises ValueError: if upper is not greater than or equal to lower
    """
    if type(luck) is not int:
        raise TypeError("Luck stat needs to be an integer!")
    if type(lower) is not int:
        raise TypeError("Lower bound needs to be an integer!")
    if type(upper) is not int:
        raise TypeError("Upper bound needs to be an integer!")
    if type(luck_multiplier) is not float and type(luck_multiplier) is not int:
        raise TypeError("Luck multiplier must be a number!")
    if upper < lower:
        raise ValueError("upper needs to be greater than lower!")
    roll = round(random.randint(lower, upper) + luck * luck_multiplier)
    return roll


def check_first(character: dict, enemy: dict) -> bool:
    """
    Check if the character is faster or enemy is faster.

    :param character: a dictionary describing the character's stats
    :param enemy: a dictionary describing the enemy's stats
    :precondition: character must be a dictionary
    :precondition: character must have at least 2 keys named 'Speed' and 'Luck'
    :precondition: enemy must be a dictionary
    :precondition: enemy must have at least 2 keys named 'Speed' and 'Name'
    :postcondition: compare speed of character and enemy and return True if character is faster and False if enemy is
    :postcondition: print a statement informing user who goes first depending on if character is faster or not
    :return: True if character is faster and False if enemy is faster
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if enemy is not a dictionary
    :raises KeyError: if 'Speed' key or 'Luck' key is not in character
    :raises KeyError: if 'Speed' key or 'Name' key is not in enemy
    """
    if type(character) is not dict or type(enemy) is not dict:
        raise TypeError("Character and Enemy must be dictionaries!")
    if 'Speed' not in character or 'Luck' not in character:
        raise KeyError("Character must have speed and luck stats!")
    if 'Speed' not in enemy or 'Name' not in enemy:
        raise KeyError("Enemy must have speed stat and a name")
    character_speed = character['Speed'] + \
        luck_roll(character['Luck'], -2, 2, 0.3)
    enemy_speed = enemy['Speed'] + luck_roll(0, -2, 2)
    if character_speed >= enemy_speed:
        print("You have higher speed and attack first")
        return True
    else:
        print(f"{enemy['Name']} has higher speed and attacks first")
        return False


def deal_damage(character_is_faster: bool, character: dict, enemy: dict) -> None:
    """
    Deal damage to the character or the enemy.

    :param character_is_faster: a boolean telling if the character is faster than the enemy or not
    :param character: a dictionary showing the character's stats
    :param enemy: a dictionary showing the enemy's stats
    :precondition: character_is_faster must be a boolean
    :precondition: character must be a dictionary
    :precondition: character must have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control', and 'Luck'
    :precondition: enemy must be a dictionary
    :precondition: enemy must have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control', and 'Luck
    :postcondition: deal damage to the enemy if character is faster, otherwise deal damage to the character
    :postcondition: print the amount of damage character took, or the amount of damage character dealt
    :raises TypeError: if character_is_faster is not a boolean
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if enemy is not a dictionary
    :raises KeyError: if character does not have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  and 'Luck'
    :raises KeyError: if enemy does not have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  and 'Luck'
    """
    if type(character_is_faster) is not bool or type(character) is not dict or type(enemy) is not dict:
        raise TypeError(
            "character_is_faster needs to be a boolean! Character and enemy need to be dictionaries!")
    if not all(key in character for key in ['Frustration', 'Name', 'Intelligence', 'Self-Control', 'Luck']) or \
            not all(key in enemy for key in ['Frustration', 'Name', 'Intelligence', 'Self-Control', 'Luck']):
        raise KeyError("Character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control', and 'Luck'"
                       "! Enemy must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control', and 'Luck'!")

    def calculate_critical(luck: int) -> bool:
        """
        Calculate if the attacker will land a critical.

        :param luck: an integer
        :precondition: luck must be an integer
        :postcondition: calculate if the attacker will land a critical attack based on a base critical chance and a
                        luck roll
        :postcondition: returns True if the attacker lands a critical hit and False if the attacker does not
        :return: True if the attacker lands a critical hit and False if they do not
        :raises TypeError: if luck is not an integer
        """
        if type(luck) is not int:
            raise TypeError("Luck needs to be an integer!")
        base_crit_chance = 5
        random_number = random.randint(1, 100)
        critical = base_crit_chance + luck_roll(luck, 0, 0, 0.5)
        if random_number <= critical:
            return True
        else:
            return False

    def validate_damage(damage) -> int:
        """
        Validate the damage dealt.

        Ensures that the damage dealt is not negative or zero.

        :param damage: a number
        :precondition: damage must be a number, either an int or a float
        :postcondition: check if damage is less than or equal to zero and returns damage of 1 if it is
        :postcondition: return damage unchanged if it is greater than zero
        :return: the validated damage as an int
        :raise TypeError: if damage is not an int or a float
        """
        if type(damage) is not int and type(damage) is not float:
            raise TypeError("Damage needs to be a number!")
        if damage <= 0:
            damage = 1
            return damage
        else:
            return round(damage)

    def calculate_damage(attacker: dict, defender: dict) -> int:
        """
        Calculate damage from the attacker to the defender.

        :param attacker: a dictionary
        :param defender: a dictionary
        :precondition: character must be a dictionary with at least 3 keys called 'Name', 'Luck', and 'Intelligence'
        :precondition: defender must be a dictionary with at least 1 key called 'Self-Control'
        :postcondition: calculate the damage done by attacker to the defender
        :postcondition: ensure the damage is not negative or zero by calling the validate_damage function
        :return: the value of the validated damage as an int
        :raises TypeError: if attacker is not a dictionary
        :raises TypeError: if defender is not a dictionary
        :raises KeyError: if attacker does not have at least 3 keys called 'Name', 'Luck', and 'Intelligence'
        :raises KeyError: if defender does not have at least 1 key called 'Self-Control'
        """
        if type(attacker) is not dict or type(defender) is not dict:
            raise TypeError("Attacker and defender need to be dictionaries!")
        if 'Name' not in attacker or 'Luck' not in attacker or 'Intelligence' not in attacker:
            raise KeyError(
                "Attacker must have at least 3 keys named 'Name', 'Luck, and 'Intelligence'")
        if 'Self-Control' not in defender:
            raise KeyError("Defender must have a key call 'Self-Control")
        attacker_critical = calculate_critical(attacker["Luck"])
        if attacker_critical:
            attacker_damage = attacker["Intelligence"] * 1.5
            print(f"{attacker['Name']} landed a critical hit!")
        else:
            attacker_damage = attacker['Intelligence'] - \
                defender["Self-Control"]

        return validate_damage(attacker_damage)

    if character_is_faster:
        character_damage = calculate_damage(character, enemy)
        enemy['Frustration'] += character_damage
        print(f"You frustrated {enemy['Name']} by {character_damage} points")
    else:
        enemy_damage = calculate_damage(enemy, character)
        character['Frustration'] += enemy_damage
        print(f"{enemy['Name']} frustrated you by {enemy_damage} points")


def level_up(character: dict) -> None:
    """
    Give the user points to allocate to stats.

    :param character: must be a dictionary
    :precondition: character must be a dictionary
    :precondition: character must have keys 'Frustration', 'Intelligence', 'Self-Control', and 'Luck', 'Motivation',
                   and 'Max Frustration'
    :postcondition: Assigns 10 points between 'Frustration', 'Intelligence', 'Self-Control', and 'Luck', 'Motivation',
                    and 'Max Frustration'
    :raises TypeError: if character is not a dictionary
    :raises KeyError: if character does not have keys 'Frustration', 'Intelligence', 'Self-Control', and 'Luck',
                      'Motivation', and 'Max Frustration'
    """
    if type(character) is not dict:
        raise TypeError("Character must be a dictionary!")
    if not all(key in character for key in ['Frustration', 'Intelligence', 'Self-Control', 'Luck', 'Motivation',
                                            'Max Frustration']):
        raise KeyError("Character must have keys 'Frustration', 'Intelligence', 'Self-Control', and 'Luck', "
                       "'Motivation', and 'Max Frustration'")
    points = 10
    print(f"You have {points} to allocate to your stats. Possible stats to increase are Motivation, Max Frustration,"
          "Self-Control, Intelligence, Luck, and Speed. Please allocate your points. ")
    Modules.character.populate_custom_points(character, points)


def calculate_fitness(character: dict, enemy: dict) -> None:
    """
    Assign fitness points to character and determine if character leveled up.

    :param character: must be a dictionary
    :param enemy: must be another dictionary
    :precondition: character must be a dictionary
    :precondition: enemy must be a dictionary
    :precondition: character must have keys named 'Fitness' and 'Level'
    :precondition: enemy must have key named 'Exp'
    :postcondition: Assign fitness points to character and determine if character leveled up
    :raises TypeError: if character is not a dictionary
    :raises TyperError: if enemy is not a dictionary
    :raises KeyError: if character does not have keys named 'Fitness' and 'Level'
    :raises KeyError: if enemy does not have key named 'Exp'
    """
    if type(character) is not dict or type(enemy) is not dict:
        raise TypeError("Character and enemy must be dictionaries!")
    if not all(key in character for key in ['Fitness', 'Level']) or 'Exp' not in enemy:
        raise KeyError(
            "Character must have keys 'Fitness' and 'Level'! Enemy must have key 'Exp'!")

    def add_fitness() -> None:
        """
        Add fitness points to character dictionary.

        :postcondition: add fitness points to character dictionary
        :postcondition: print message to user informing them that they won the battle at the beginning
        :postcondition: print message to user informing them how many fitness points they gained
        """
        print("You won the battle!")
        character["Fitness"] += enemy["Exp"]
        print(
            f"You've gained {enemy['Exp']} fitness points from defeating {enemy['Name']}")

    add_fitness()
    if character["Fitness"] >= 15 and character["Level"] < 2:
        character["Level"] = 2
        print("Congratulations! You have reached level 2!")
        level_up(character)
    elif character["Fitness"] >= 30 and character["Level"] < 3:
        character["Level"] = 3
        print("Congratulations! You've reached level 3! Go get that boss now.")
        level_up(character)
    else:
        pass


def battle_loss(character: dict, enemy: dict) -> None:
    """
    Decrease character motivation after battle loss.

    :param character: a dictionary
    :param enemy: another dictionary
    :precondition: character must be a dictionary
    :precondition: character must have a key named 'Motivation'
    :precondition: enemy must be a dictionary
    :precondition: enemy must have a key named 'Name'
    :postcondition: decrease player motivation by 2
    :postcondition: prints message to player informing them they lost 2 motivation
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if enemy is not a dictionary
    :raises KeyError: if character does not have key 'Motivation'
    :raises KeyError: if enemy does not have key 'Name'
    >>> character_battle_loss = {'Motivation': 2}
    >>> enemy_battle_loss = {'Name': 'Nothing'}
    >>> battle_loss(character, enemy)
    You gave in to the temptation of Nothing! You lost 2 motivation.
    """
    if type(character) is not dict or type(enemy) is not dict:
        raise TypeError("Character and enemy must be dictionaries!")
    if 'Motivation' not in character:
        raise KeyError("Character must have key 'Motivation'!")
    if 'Name' not in enemy:
        raise KeyError("Enemy must have key 'Name'!")
    print(
        f"You gave in to the temptation of {enemy['Name']}! You lost 2 motivation.")
    character["Motivation"] -= 2


def check_result(character: dict, enemy: dict, lose_function, win_function) -> None:
    """
    Check if the character won the battle or not.

    :param character: a dictionary
    :param enemy: another dictionary
    :param lose_function: a function to execute when the character wins the battle
    :param win_function: a function to execute when the character loses the battle
    :precondition: character must be a dictionary
    :precondition: character must have keys named 'Frustration', 'Max Frustration', 'Motivation', 'Fitness',
                   'Name', and 'Level'
    :precondition: enemy must be a dictionary
    :precondition: enemy must have a keys named 'Name' and 'Exp'
    :postcondition: execute lose_function if the character lost the battle and win_function if they won
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if enemy is not a dictionary
    :raises TypeError: if lose_function is not a function
    :raises TypeError: if win_function is not a function
    :raises KeyError: if character does not have keys 'Motivation', 'Fitness', 'Name', and 'Level'
    :raises KeyError: if enemy does not have keys 'Name' and 'Exp'
    """
    if type(character) is not dict or type(enemy) is not dict:
        raise TypeError("Character and enemy must be dictionaries!")
    if not callable(win_function) or not callable(lose_function):
        raise TypeError("win_function and lose_function need to be functions!")
    if not all(key in character for key in ['Frustration', 'Max Frustration', 'Motivation', 'Fitness', 'Name',
                                            'Level']):
        raise KeyError("Character must have keys 'Frustration', 'Max Frustration', 'Motivation', 'Fitness', "
                       "'Name', and 'Level'!")
    if not all(key in enemy for key in ['Name', 'Exp']):
        raise KeyError("Enemy must have keys 'Name' and 'Exp'!")

    if character['Frustration'] >= character["Max Frustration"]:
        lose_function(character, enemy)
    else:
        win_function(character, enemy)


def battle(character_is_faster: bool, character: dict, enemy: dict, enemy_frustration) -> None:
    """
    Deal damage to character and enemy.

    Deals damage to the slower person and then deals damage to the faster person if slower is still alive.

    :param character_is_faster: a boolean telling if the character is faster than the enemy or not
    :param character: a dictionary showing the character's stats
    :param enemy: a dictionary showing the enemy's stats
    :param enemy_frustration: a number
    :precondition: character_is_faster must be a boolean
    :precondition: character must be a dictionary
    :precondition: character must have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                   'Max Frustration' and 'Luck'
    :precondition: enemy must be a dictionary
    :precondition: enemy must have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control', and 'Luck
    :precondition: enemy_frustration must be either an int or a float that is positive
    :postcondition: deal damage to slower person and then deals damage to faster person if slower is still alive.
    :postcondition: repeats until either character or enemy have max frustration
    :raises TypeError: if character_is_faster is not a boolean
    :raises TypeError: if character is not a dictionary
    :raises TypeError: if enemy is not a dictionary
    :raises TypeError: if enemy_frustration is not an int or a float
    :raises ValueError: if enemy_frustration is not positive
    :raises KeyError: if character does not have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  'Max Frustration' and 'Luck'
    :raises KeyError: if enemy does not have keys named 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  and 'Luck'
    """
    if type(character_is_faster) is not bool or type(character) is not dict or type(enemy) is not dict \
            or type(enemy_frustration) is not int and type(enemy_frustration) is not float:
        raise TypeError("character_is_faster needs to be a boolean! Character and enemy need to be dictionaries!"
                        "enemy_frustration needs to be a number!")
    if enemy_frustration <= 0:
        raise ValueError("enemy_frustration needs to be positive!")
    if not all(key in character for key in ['Frustration', 'Name', 'Intelligence', 'Self-Control', 'Max Frustration',
                                            'Luck']) or not all(key in enemy for key in
                                                                ['Frustration', 'Name', 'Intelligence', 'Self-Control',
                                                                 'Luck']):
        raise KeyError("Character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control', "
                       "'Max Frustration', and 'Luck'! Enemy must have keys 'Frustration', 'Name', 'Intelligence', "
                       "'Self-Control', and 'Luck'!")

    while character['Frustration'] < character["Max Frustration"] and enemy['Frustration'] < enemy_frustration:
        deal_damage(character_is_faster, character, enemy)
        if character['Frustration'] < character["Max Frustration"] and enemy['Frustration'] < enemy_frustration:
            deal_damage(not character_is_faster, character, enemy)


def battle_sequence(character: dict) -> None:
    """
    Drive the battle sequence.

    :param character: a dictionary describing the character's stats
    :precondition: character must be a dictionary
    :precondition: character must have keys 'Frustration', 'Name', 'Intelligence', 'Self-Control',
                  'Max Frustration', 'Luck', 'Motivation', 'Fitness', and 'Level'
    :postcondition: drive the battle sequence between a character and the enemy
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

    enemy = determine_enemy(character['Level'])
    character["Frustration"] = 0
    character_is_faster = check_first(character, enemy)
    battle(character_is_faster, character, enemy, enemy["Max Frustration"])
    check_result(character, enemy, battle_loss, calculate_fitness)


def main():
    """
    Drive the program.
    """
    character = {'Name': 'Bob', 'Motivation': 100, 'Frustration': 0, 'Intelligence': 10, 'Speed': 3, 'Luck': 5,
                 "Self-Control": 4, "Level": 1, "Fitness": 14, "Max Frustration": 100}
    battle_sequence(character)


if __name__ == '__main__':
    main()
