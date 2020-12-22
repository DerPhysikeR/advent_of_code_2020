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


def run_recursive_game(*players, depth=0):
    players = [deque(p) for p in players]
    prev_decks = tuple([set() for _ in players])
    while all(len(p) > 0 for p in players):
        # check if configuration existed before
        if all(tuple(p) in prev for p, prev in zip(players, prev_decks)):
            return players, 0
        for player, prev in zip(players, prev_decks):
            prev.add(tuple(player))
        # draw cards
        draw = [p.popleft() for p in players]
        # check if amount leftover cards >= value of drawn card
        if all(len(p) >= d for p, d in zip(players, draw)):
            _, winner = run_recursive_game(
                *[list(p)[:d] for p, d in zip(players, draw)], depth=depth + 1
            )
        else:
            winner = draw.index(max(draw))
        # add drawn cards to winning player
        players[winner].append(draw[winner])
        players[winner].append(draw[(winner + 1) % 2])
    return players, winner


if __name__ == "__main__":
    player1, player2 = read_player_decks(argv[-1])

    # part 1
    result1, result2 = run_game(player1, player2)
    winner = result1 if len(result1) > 0 else result2
    print(winner)
    print(score_deck(winner))

    # part 1
    result, winner = run_recursive_game(player1, player2)
    print(list(result[winner]))
    print(score_deck(result[winner]))
