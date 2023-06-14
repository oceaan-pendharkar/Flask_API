from flask import Flask, session, jsonify, request, render_template
from Modules import battle_module, board, character, end_game
import random

app = Flask(__name__)
app.secret_key = 'secret!!'


def generate_room(character_in_play) -> str:
    """
    Pseudo-randomly select a room for a player to enter, in a game.

    :precondition: LOCATIONS must exist as a non-empty tuple of strings
    :precondition: the character must be in the game
    :postcondition: the room is selected for the player
    :return: the name of the room, as a string
    """
    if character_in_play["Luck"] > 35:
        room_indices = [7, 9, 4, 5, 4, 5, 1]  # more lucky rooms than not
        selection = room_indices[random.randint(0, 6)]
    else:
        selection = random.randint(0, 9)
    return str(board.LOCATIONS[selection])


@app.route('/')
def welcome():
    session['board'] = board.make_board(10, 10)
    output = "Welcome to the game! Type your character's name to begin..."
    return render_template('index.html', output=output)


@app.route('/create_character', methods=['POST'])
def create_character():
    name = request.form.get('welcome-input')
    session['character'] = {"Motivation": 80, "Max Frustration": 60, "Self-Control": 5, "Intelligence": 5, "Luck": 5, "Speed": 5,
                            "Fitness": 5, 'Name': name, "row": 0, "column": 0, "Level": 1,
                            "alive": True, "goal achieved": False, "Frustration": 0}
    output = "Alright, " + name + ". You are on MISSION: COMPLETE ASSIGNMENT 4.<br>You're at the end of your first term in CST and things have been hectic as HECK.<br>But don't worry, we know you can do it!<br>Your mission is to stay Motivated enough to stay alive, achieve enough Fitness level to defeat the final boss, and<br>make it to the last square of the board for the final battle..."
    session.modified = True
    return render_template('create_character.html', output=output, character=session['character'])


@app.route('/enter_first_room', methods=['POST'])
def enter_first_room():
    selection = request.form.get('user-input')

    if selection == 'nerd':
        session['character']["Intelligence"] += 10
    elif selection == 'leprechaun':
        session['character']["Luck"] += 10
    elif selection == 'great ape':
        session['character']["Self-Control"] += 10
    elif selection == 'jock':
        session['character']["Speed"] += 10

    output = "Your points have been added!"
    room_name = generate_room(session['character'])
    event = ''
    chance = None

    if room_name == board.LOCATIONS[0] or room_name == board.LOCATIONS[3]:
        event = 'get assigned ANOTHER assignment'
        chance = 3

    elif room_name in [board.LOCATIONS[1], board.LOCATIONS[2], board.LOCATIONS[8], board.LOCATIONS[9]]:
        event = 'have to fight'
        chance = 2

    elif room_name == board.LOCATIONS[6] or room_name == board.LOCATIONS[7]:
        event = 'lose self-control'
        chance = 2

    else:
        event = 'gain motivation'
        chance = 3

    output += "<br>You're in " + room_name + ". There is a 1/" + \
        str(chance) + " chance that you will " + event + \
        ". Type a number between 1 and " + str(chance) + " inclusive."

    session['generated_number'] = random.randint(1, chance)
    session['event'] = event
    print(session['event'])
    session.modified = True
    return render_template('guessing_game.html', output=output, generated_number=session['generated_number'], acceptable_numbers=[number for number in range(1, chance + 1)], event=session['event'], character=session['character'])


@app.route('/event_happens', methods=['POST'])
def event_happens():
    generated_number = request.form.get('generated-number')
    print('generated number in event happens: ' + generated_number)
    acceptable_numbers_string = request.form.get('acceptable-numbers')
    guess = request.form.get('guess-input')
    event = session['event']
    output = ''

    try:
        guess_int = int(guess)
    except ValueError:
        output += "Looks like you entered something other than an int between 1 and " + \
            acceptable_numbers_string[-2] + " . Try again..."
        return render_template('guessing_game.html', output=output, generated_number=generated_number, acceptable_numbers=acceptable_numbers_string, character=session['character'])
    else:
        if guess not in acceptable_numbers_string:
            output += "Looks like you entered an integer outside the bounds of 1 and " + \
                acceptable_numbers_string[-2] + " inclusive . Try again..."
            return render_template('guessing_game.html', output=output, generated_number=generated_number, acceptable_numbers=acceptable_numbers_string, character=session['character'])

        if guess == generated_number:
            if event == 'get assigned ANOTHER assignment':
                session['character']["Intelligence"] += 5
                session['character']["Luck"] -= 2
                session.modified = True
                output += "You KNEW this would happen! You got assigned ANOTHER assignment. Your Intelligence is increased by 5, but your Luck is decreased by 2. Type 'n', 's', 'e', or 'w' to move one square."
                return render_template('event_happens.html', output=output, generated_number=str(generated_number), character=session['character'])
            elif event == 'have to fight':
                output += 'You KNEW this would happen! You have to fight.<br>'
                enemy = battle_module.determine_enemy(
                    session['character']['Level'])

                output = enemy['Description']

                enemy_frustration = enemy['Frustration']
                session['character']["Frustration"] = 0
                character_is_faster = battle_module.check_first(
                    session['character'], enemy)
                if character_is_faster:
                    output += "<br>You have higher speed and attack first!"
                else:
                    output += '<br>' + enemy['Name'] + \
                        ' has higher speed and attacks first!'

                while session['character']['Frustration'] < session['character']["Max Frustration"] and enemy['Frustration'] < enemy_frustration:
                    character_damage = battle_module.calculate_damage(
                        session['character'], enemy)
                    enemy['Frustration'] += character_damage
                    output += "You frustrated {enemy['Name']} by " + \
                        str(character_damage) + " points!<br>"
                    if session['character']['Frustration'] < session['character']["Max Frustration"] and enemy['Frustration'] < enemy_frustration:
                        enemy_damage = battle_module.calculate_damage(
                            enemy, session['character'])
                        session['character']['Frustration'] += enemy_damage
                        output += enemy['Name'] + " frustrated you by " + \
                            str(enemy_damage) + " points"

                if session['character']['Frustration'] >= session['character']["Max Frustration"]:
                    output += '<br>You gave into the temptation of ' + \
                        enemy['Name'] + \
                        '! You lost the battle and lost 2 motivation.'
                    session['character']["Motivation"] -= 2
                else:
                    session['character']['Fitness'] += enemy['Exp']
                    output += '<br>You defeated ' + \
                        enemy['Name'] + '!<br>You won the battle and gained ' + \
                        str(enemy['Exp']) + ' fitness.'

                    if session['character']["Fitness"] >= 15 and session['character']["Level"] < 2:
                        session['character']["Level"] = 2
                        output += " Congratulations! You have reached level 2! You have 10 points to allocate to your stats. <br>Type the name of the stat you want to increase: Intelligence, Self-Control, Speed, or Luck."
                        session.modified = True
                        return render_template('allocate_points.html', output=output, character=session['character'])
                    elif session['character']["Fitness"] >= 30 and session['character']["Level"] < 3:
                        session['character']["Level"] = 3
                        output += " Congratulations! You've reached level 3! Go get that boss now. You have 10 points to allocate to your stats. <br>Type the name of the stat you want to increase: Intelligence, Self-Control, Speed, or Luck. Case-sensitive!"
                        session.modified = True
                        return render_template('allocate_points.html', output=output, character=session['character'])
                    else:
                        output += "<br>Type 'n', 's', 'e', or 'w' to move one square."
                session.modified = True
                return render_template('battle.html', output=output, character=session['character'], enemy=enemy, generated_number=generated_number)

            elif event == 'lose self-control':
                session['character']["Self-Control"] -= 2
                output = "You KNEW this would happen! You lose self-control. Your Self-Control is decreased by 2. Type 'n', 's', 'e', or 'w' to move one square."
                session.modified = True
                return render_template('event_happens.html', output=output, generated_number=str(generated_number), character=session['character'])
            elif event == 'gain motivation':
                session['character']["Motivation"] += 2
                output = "You KNEW this would happen! You gain motivation. Your Motivation is increased by 2. Type 'n', 's', 'e', or 'w' to move one square."
                session.modified = True
                return render_template('event_happens.html', output=output, generated_number=str(generated_number), character=session['character'])
        else:
            output = "You did not " + event + \
                ". As you were...<br>Type 'n', 's', 'e', or 'w' to move one square."
            session.modified = True
            return render_template('event_happens.html', output=output, generated_number=str(generated_number), character=session['character'])


@ app.route('/battle', methods=['POST'])
def battle():
    enemy = session['enemy']
    enemy_frustration = enemy['Max Frustration']
    character_is_faster = battle_module.check_first(
        session['character'], enemy)
    output = ""

    while session['character']['Frustration'] < session['character']["Max Frustration"] and enemy['Frustration'] < enemy_frustration:
        character_damage = battle_module.calculate_damage(
            session['character'], enemy)
        enemy['Frustration'] += character_damage
        output += "You frustrated {enemy['Name']} by " + \
            str(character_damage) + " points!<br>"
        if session['character']['Frustration'] < session['character']["Max Frustration"] and enemy['Frustration'] < enemy_frustration:
            enemy_damage = battle_module.calculate_damage(
                enemy, session['character'])
            session['character']['Frustration'] += enemy_damage
            output += enemy['Name'] + " frustrated you by " + \
                str(enemy_damage) + " points"

    if character['Frustration'] >= character["Max Frustration"]:
        output = 'You gave into the temptation of ' + enemy['Name'] + \
            '! You lost the battle and lost 2 motivation.<br>Type "n", "s", "e", or "w" to move one square.'
        session['character']["Motivation"] -= 2
        session.modified = True
        return render_template('move.html', output=output)
    else:
        session['character']['Fitness'] += enemy['Exp']
        output += 'You defeated ' + enemy['Name'] + \
            '! You won the battle and gained ' + \
            str(enemy['Exp']) + ' fitness.'

        if session['character']["Fitness"] >= 15 and session['character']["Level"] < 2:
            session['character']["Level"] = 2
            output += "Congratulations! You have reached level 2! You have 10 points to allocate to your stats. <br>Type the name of the stat you want to increase: Intelligence, Fitness, Self-Control, Speed, or Luck."
            session.modified = True
            return render_template('allocate_points.html', output=output, character=session['character'])
        elif session['character']["Fitness"] >= 30 and session['character']["Level"] < 3:
            session['character']["Level"] = 3
            output += "Congratulations! You've reached level 3! Go get that boss now. You have 10 points to allocate to your stats. <br>Type the name of the stat you want to increase: Intelligence, Fitness, Self-Control, Speed, or Luck. Case-sensitive!"
            session.modified = True
            return render_template('allocate_points.html', output=output, character=session['character'])
        else:
            output += "<br>Type 'n', 's', 'e', or 'w' to choose which direction to move on the board."
            return render_template('move.html', output=output, character=session['character'])


@ app.route('/allocate_points_check', methods=['POST'])
def allocate_points():
    stat_to_allocate = request.form.get('stat-to-allocate')

    if stat_to_allocate not in ['Intelligence', 'Self-Control', 'Speed', 'Luck']:
        output = "Uh-oh. You can only allocate your 10 points to Intelligence, Self-Control, Speed, or Luck. Case-sensitive!"
        session.modified = True
        return render_template('allocate_points.html', output=output, character=session['character'])
    else:
        session['character'][stat_to_allocate] += 10
        output = "<br>Alright, you've allocated 10 points to " + \
            stat_to_allocate + ".<br>Type 'n', 's', 'e', or 'w' to move one square."
        session.modified = True
        return render_template('move.html', output=output, character=session['character'])


@ app.route('/move', methods=['POST'])
def move():
    print(session['character'])
    direction = request.form.get('direction-input')

    if direction not in ['n', 's', 'e', 'w']:
        output = "Uh-oh. You can only move n, s, e, or w. Single Letter. Case-sensitive!"
        return render_template('event_happens.html', output=output, character=session['character'])
    else:
        alive = character.check_alive(session['character'])
        output = ""
        if direction == "n" or direction == "s":
            potential_row = board.get_row_coordinate(
                session['character'], direction)
            print('potential row', potential_row)
            if potential_row <= session['board'][0][0] or potential_row >= session['board'][0][1]:
                output = "Uh-oh. You can't move off the board. Try again: n, s, e, or w."
                return render_template('event_happens.html', output=output, character=session['character'], generated_number="N/A")
            else:
                session['character']["row"] = potential_row
        elif direction == 'e' or direction == 'w':
            potential_column = board.get_column_coordinate(
                session['character'], direction)
            print('potential column', potential_column)
            if potential_column <= session['board'][1][0] or potential_column >= session['board'][1][1]:
                output = "Uh-oh. You can't move off the board. Try again: n, s, e, or w."
                return render_template('event_happens.html', output=output, character=session['character'], generated_number="N/A")
            else:
                session['character']["column"] = potential_column
        output += "Success! You've moved. Type anything to enter the room."
        if alive:
            if session['character']["Fitness"] >= 30 and (session['character']["row"] + 1, session['character']["column"] + 1) == (session['board'][0][1], session['board'][1][1]):
                output += "<br>Nice job, " + session['character']['Name'] + \
                    " . You've reached the final square and you're ready to defeat the final boss!!! Type anything to fight the boss."
                return render_template('endgame.html', output=output, character=session['character'])
            elif session['character']["Fitness"] >= 30 and (session['character']["row"] + 1, session['character']["column"] + 1) != (session['board'][0][1], session['board'][1][1]):
                output += "Alright, " + session['character']['Name'] + \
                    ". You've got enough fitness points to defeat the final boss! Make your way to the final square for the final battle..."
            elif session['character']["Fitness"] < 30 and (session['character']["row"] + 1, session['character']["column"] + 1) == (session['board'][0][1], session['board'][1][1]):
                output += "<br>Hey there, " + session['character']['Name'] + \
                    ", you've found the final square, but you aren't ready to defeat the boss yet! Keep trucking..."
        else:
            output += "Sorry, you lost all your motivation... you're basically dead. Have fun in the afterlife! Enter a character name to start a new game."
            return render_template('index.html', output=output)

        session.modified = True
        return render_template('move.html', output=output, character=session['character'])


@ app.route('/enter_room', methods=['POST'])
def enter_room():
    room_name = generate_room(session['character'])
    event = ''
    chance = None

    if room_name == board.LOCATIONS[0] or room_name == board.LOCATIONS[3]:
        event = 'get assigned ANOTHER assignment'
        chance = 3

    elif room_name in [board.LOCATIONS[1], board.LOCATIONS[2], board.LOCATIONS[8], board.LOCATIONS[9]]:
        event = 'have to fight'
        chance = 2

    elif room_name == board.LOCATIONS[6] or room_name == board.LOCATIONS[7]:
        event = 'lose self-control'
        chance = 3

    else:
        event = 'gain motivation'
        chance = 3

    output = "You're in " + room_name + ". There is a 1/" + \
        str(chance) + " chance that you will " + event + \
        ". Type a number between 1 and " + str(chance) + " inclusive."

    session['generated_number'] = random.randint(1, chance)
    session['event'] = event
    print(session['event'])
    return render_template('guessing_game.html', output=output, generated_number=session['generated_number'], acceptable_numbers=[number for number in range(1, chance + 1)], event=session['event'], character=session['character'])


@ app.route('/endgame', methods=['POST'])
def endgame():
    session['boss'] = {"Name": "Assignment 4", "Frustration": 0, "Max Frustration": 100, "Intelligence": 13, "Speed": 30,
                       "Self-Control": 10, "Luck": 0, 'Exp': 0}
    character_is_faster = battle_module.check_first(
        session['character'], session['boss'])
    # battle_module.battle(
    #     character_is_faster, character, boss, boss["Max Frustration"] / 2)

    output = ""

    enemy_frustration = session['boss']['Frustration']
    half_enemy_frustration = enemy_frustration / 2
    session['character']["Frustration"] = 0
    if character_is_faster:
        output += "<br>You have higher speed and attack first!"
    else:
        output += '<br>' + session['boss']['Name'] + \
            ' has higher speed and attacks first!'

    while session['character']['Frustration'] < session['character']["Max Frustration"] and session['boss']['Frustration'] < half_enemy_frustration:
        character_damage = battle_module.calculate_damage(
            session['character'], session['boss'])
        session['boss']['Frustration'] += character_damage
        output += "You frustrated {enemy['Name']} by " + \
            str(character_damage) + " points!<br>"
        if session['character']['Frustration'] < session['character']["Max Frustration"] and session['boss']['Frustration'] < half_enemy_frustration:
            enemy_damage = battle_module.calculate_damage(
                session['boss'], session['character'])
            session['character']['Frustration'] += enemy_damage
            output += session['boss']['Name'] + " frustrated you by " + \
                str(enemy_damage) + " points"

    if session['character']["Frustration"] < session['character']["Max Frustration"]:
        # mid_boss_event(character, boss)
        output += " You've finished making all the code for assignment 4! You bask in your achievement before a sinking " \
            "realization dawns upon you.<br>You still have to unit test everything... The thought of the endless unit tests" \
            " makes you more frustrated and makes Assignment 4 so much harder to complete.<br>Assignment 4's stats have " \
            "increased and your frustration increases by 5.<br>"
        session['boss']["Intelligence"] = round(
            session['boss']["Intelligence"] * 1.1)
        session['boss']["Speed"] = round(session['boss']["Speed"] * 1.1)
        session['character']["Frustration"] += 5

    # battle_module.battle(
    #     character_is_faster, session['character'], session['boss'], session['boss']["Max Frustration"])

    while session['character']['Frustration'] < session['character']["Max Frustration"] and session['boss']['Frustration'] < half_enemy_frustration:
        character_damage = battle_module.calculate_damage(
            session['character'], session['boss'])
        session['boss']['Frustration'] += character_damage
        output += "You frustrated {enemy['Name']} by " + \
            str(character_damage) + " points!<br>"
        if session['character']['Frustration'] < session['character']["Max Frustration"] and session['boss']['Frustration'] < half_enemy_frustration:
            enemy_damage = battle_module.calculate_damage(
                session['boss'], session['character'])
            session['character']['Frustration'] += enemy_damage
            output += session['boss']['Name'] + " frustrated you by " + \
                str(enemy_damage) + " points"

    # battle_module.check_result(
    #     session['character'], session['boss'], boss_lose, boss_win)
    if session['character']['Frustration'] >= session['character']["Max Frustration"]:
        output += "<br>" + session['boss']['Name'] + \
            " has frustrated you so much, that you just gave up. Sorry you didn't win " + \
            session['character']['Name'] + \
            ".<br>You decided that life is too short to be working all the time, and you need to enjoy life."
    else:
        output += "<br>Congratulations " + session['character']['Name'] + \
            "! You've beaten " + session['boss']['Name'] + \
            " and have completed the game! Enter a character name to play again."
    print(output)
    session.modified = True
    return render_template('index.html', output=output, character=session['character'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
