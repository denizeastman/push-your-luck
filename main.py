from drafter import *
from dataclasses import dataclass, field
from bakery import assert_equal
import random

set_website_title("Push Your Luck")

set_site_information(
    author="Deniz Eastman",
    description="Higher or Lower probability game",
    sources="Drafter documentation and course notes",
    planning=["Final Project"],
    links=[""]
)

hide_debug_information()

@dataclass
class Round:
    """
    Stores one completed round.
    """
    round_number: int
    player_choice: str
    result: str
    score_after_round: int
    
    
@dataclass
class State:
    """
    Stores all game information.
    """
    player_name: str
    score: int
    high_score: int
    current_number: int
    rounds_played: int
    number_range: str
    show_probability: str
    status: str
    history: list[Round]
    
    
def generate_number(max_range: int) -> int:
    """
    Chooses a random number
    Arg:
    
        max_range:int this is the max range
        
    Returns:
        a randum number from 1 to max_range
    """
    return random.randint(1, max_range)


def calculate_higher_probability(current_number: int, max_range: int) -> float:
    """
    This helps calculate the probability percentage of the higher probability.
    
    args:
        current_number: int, This uses the current number thats show on screen 
        max_range: int, This is the max range that you choose
        
    return:
        this return rounds the 'max_range' subtracted by the 'current_number', then divides by the 'max_range', then multiplied by 100
    """
    return round(((max_range - current_number)/ max_range) * 100, 1)


def calculate_lower_probability(current_number: int, max_range: int) -> float:
    """
    This helps calculate the probability percentage of the lower probability.
    
    args:
        current_number: int, This uses the current number thats show on screen 
        max_range: int, This is the max range that you choose
        
    return:
        returns the percentage of what the lower chance would be    
    """
    return round(((current_number - 1)/ max_range) * 100, 1)

assert_equal(calculate_higher_probability(10, 20), 50.0)
assert_equal(calculate_lower_probability(10, 20), 45.0)


@route
def index(state: State) -> Page:
    """
    The first page or the Home page
    
    args:
    state: State, stores all the info about the player name and game.
    
    return:
        A page that will allow the player to create a name/game name to set the number between 20,30, and 50,
        decide whether they want help or not, and start the game. 
    """
    
    return Page(state, [
        
        Header("Push Your Luck"),
        state.status,
        
        "Player Name:",
        TextBox("player_name", state.player_name),
        
        "Number Range (20,30,50):",
        TextBox("number_range", state.number_range),
        
        "Show Probabilities? (yes/no):",
        TextBox("show_probability", state.show_probability),
        Button("Start Game", "start_game"),
        Button("Statistics", "statistics"),
        Button("History", "history_page"),
        Button( "Probability Guide", "guide")])


@route
def start_game(state: State, player_name: str, number_range: str, show_probability: str) -> Page:
    """
    Starts a new game
    
    args:
        state: State, stores all the info about the player name and game
        player_name: str, the name entered by the player
        number_range: str, the range thats preset between 20,30,50
        show_probability: str, deterimens wether the player wants to see the percent of if the number is higher or lower or not.
    returns:
        The main game page

    """
    
    if number_range not in ["20", "30", "50"]:
        
        state.status = ("Error: Number Range must be 20, 30, or 50.")
        
        return index(state)
    
    state.player_name = player_name
    state.number_range = number_range
    state.show_probability = show_probability
    state.score = 0
    state.rounds_played = 0
    state.history = []
    
    max_range = int(number_range)
    
    state.current_number = generate_number(max_range)
    state.status = "Game Started!"
    
    return play(state)


@route
def play(state: State) -> Page:
    """
    Main game page
    
    args:
        state: State, stores all the info about the player name and game
        
    return:
        page showing players score, random number, probibility, buttons for higher, lower, cashout, and reset"
    """
    
    pieces = [Header("Current Game"), "Player: " + state.player_name, "Current Number: " + str(state.current_number),
              "Score: " + str(state.score)]
    
    if state.show_probability.lower() == "yes":
        
        higher_prob = (calculate_higher_probability(state.current_number, int(state.number_range)))
        lower_prob = (calculate_lower_probability(state.current_number, int(state.number_range)))
        
        pieces.append("Higher Chance: " + str(higher_prob) + "%")
        pieces.append("Lower Chance: " + str(lower_prob) + "%")
        
    pieces.append(Button("Higher", "higher"))
    pieces.append(Button("Lower", "lower"))
    pieces.append(Button("Cash Out", "cash_out"))
    pieces.append(Button("Reset", "reset_game"))
    
    return Page(state, pieces)


@route
def higher(state: State) -> Page:
    """
    plays the players higher guess
    
    args:
        state: State, stores all the info about the player name and game
    return:
        The gameplay if it was correct you get points and move on if it is wrong you get sent to the loss screen and restart
    """
    next_number = generate_number(int(state.number_range))
    state.rounds_played += 1
    
    if next_number > state.current_number:
        state.score += 10
        state.history.append(Round(state.rounds_played, "Higher", "Win", state.score))
        state.current_number = next_number
        
        return play(state)
    
    else:
        state.history.append(Round(state.rounds_played, "Higher", "Loss", state.score))
        
        return lose_page(state)
    
    
@route
def lower(state: State) -> Page:
    """
    plays the players lower guess
    
    args:
        state: State, stores all the info about the player name and game
    return:
        The gameplay if it was correct you get points and move on if it is wrong you get sent to the loss screen and restart
    """
    next_number = generate_number(int(state.number_range))
    state.rounds_played += 1
    
    if next_number < state.current_number:
        
        state.score += 10
        state.history.append(Round(state.rounds_played, "Lower", "Win", state.score))
        state.current_number = next_number
        
        return play(state)
    
    else:
        state.history.append(Round(state.rounds_played, "Lower", "Loss", state.score))
        
        return lose_page(state)
    
    
@route
def cash_out(state: State) -> Page:
    """
    Cashes out the current score and keeps it noted
    
    args:
        state: State, stores all the info about the player name and game
    returns:
        Takes you to the home page after saving the score and updating the high score if needed
    """
    
    if state.score > state.high_score:
        state.high_score = state.score
    state.status = ("You cashed out with " + str(state.score) + " points!")
    
    return index(state)


@route
def statistics(state: State) -> Page:
    """
    The page that holds all the stats
    
    arg:
        state: State, stores all the info about the player name and game
    returns:
        The statistics of the game such as the highscore and the previous score that you settled with and the round played
    """
    
    return Page(state, [
        
        Header("Statistics"),
        
        "High Score: " + str(state.high_score),
        
        "Previous Score: " + str(state.score),
        
        "Rounds Played: " + str(state.rounds_played),
        
        Button("Home", "index")])


@route
def history_page(state: State) -> Page:
    """
    shows every games history
    
    args:
        state: State, stores all the info about the player name and game
    returns:
        this page shows ever Round object recorded in gameplay
    """
    
    output = [Header("History")]
    
    for round_info in state.history:
        output.append(
            
            "Round " + str(round_info.round_number) + " | " + round_info.player_choice + " | "
            
            + round_info.result + " | Score " + str(round_info.score_after_round))
        
    output.append(Button("Home", "index"))
    
    return Page(state, output)


@route
def guide(state: State) -> Page:
    """
    Explains how the games probability works out
    
    args:
        state: State, stores all the info about the player name and game
    returns:
        a page on how the game works and it probabilities
    """
    
    return Page(state, [Header("Probability Guide"),
                        "Lower numbers generally make Higher safer.",
                        
                        "Higher numbers generally make Lower safer.",
                        "Use percentages to decide whether to risk your points.",
                        
                        Button("Home", "index")])


@route
def lose_page(state: State) -> Page:
    """
    The screen that shows up when you fail your higher or lower outcome
    
    args:
        state: State, stores all the info about the player name and game
        
    returns:
        This show a screen that tells you when you lose and the amount of points you had and a restart button
    """

    return Page(state, [Header("Game Over"),
                        
                        "You guessed incorrectly.",
                        
                        "Final Score: " + str(state.score),
                        
                        Button("Start New Game","index")])


@route
def reset_game(state: State) -> Page:
    """
    resets the game
    
    args:
        state: State, stores all the info about the player name and game
    returns:
        resets all the game values
    """
    
    state.score = 0
    state.rounds_played = 0
    state.current_number = 1
    state.history = []
    state.status = "Game Reset"
    
    return index(state)


start_server(
    State("", 0, 0, 1, 0, "20", "yes", "Welcome to Push Your Luck!", []))
