from collections import deque
from sys import argv


def read_player_decks(filename):
    with open(filename) as stream:
        decks = stream.read().strip().split("\n\n")
        return [[int(card) for card in deck.split("\n")[1:]] for deck in decks]


def run_game(*players):
    players = [deque(p) for p in players]
    while all(len(p) > 0 for p in players):
        draw = [p.popleft() for p in players]
        maximum = max(draw)
        players[draw.index(maximum)].extend(reversed(sorted(draw)))
    return [list(p) for p in players]


def score_deck(deck):
    return sum(i * c for i, c in enumerate(reversed(deck), 1))


if __name__ == "__main__":
    player1, player2 = read_player_decks(argv[-1])
    print(player1)
    print(player2)
    player1, player2 = run_game(player1, player2)
    winner = player1 if len(player1) > 0 else player2
    print(winner)
    print(score_deck(winner))
