import random

def pick_winner(names, winners):
    if not names:
        return None, names, winners
    
    winner = random.choice(names)
    names.remove(winner)   # IMPORTANT: no repeat
    winners.append(winner)
    
    return winner, names, winners