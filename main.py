import operator


CARD_RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
              'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def get_hands(file):
    hands = open(file).read().rstrip().split('\n')
    first_player = [hand.split()[:5] for hand in hands]
    second_player = [hand.split()[5:] for hand in hands]
    return first_player, second_player


def get_card_value(card):
    return card[:-1]


def get_card_suit(card):
    return card[-1]


def is_one_pair(hand):
    """Возвращает True и значение пары карт с одинаковым значением, если такая пара нашлась, иначе False"""
    hand_values = [get_card_value(card) for card in hand]
    val_count = {card: hand_values.count(card) for card in hand_values}
    pair_val = [card for card in hand_values if hand_values.count(card) == 2]
    pair_count = sum(1 for val in val_count.values() if val == 2)
    return (True, pair_val[0]) if pair_count == 1 else False


def is_two_pair(hand):
    """Возвращает True, если нашлись 2 пары карт, иначе False"""
    hand_values = [get_card_value(card) for card in hand]
    val_count = {card: hand_values.count(card) for card in hand_values}
    pair_count = sum(1 for val in val_count.values() if val == 2)
    return pair_count == 2


def is_three_of_a_kind(hand):
    """Возвращает True, если нашлись 3 карты с одинаковым значением, иначе False"""
    hand_values = [get_card_value(card) for card in hand]
    val_count = {card: hand_values.count(card) for card in hand_values}
    return 3 in val_count.values()


def is_straight(hand):
    """Ввозвращает True, если выпал Стрит, иначе False"""
    valid_ranges = [['A', '2', '3', '4', '5'], ['6', '7', '8', '9', 'T']]
    for index in range(2, 6):
        valid = [str(num) for num in range(index, index + 5)]
        valid_ranges.append(valid)
    hand_vals = [get_card_value(card) for card in hand]
    for valid_range in valid_ranges:
        check = 1
        for value in valid_range:
            if value not in hand_vals:
                check = 0
        if check == 1:
            return True
    return False


def is_flush(hand):
    """Ввозвращает True, если выпал Флеш, иначе False"""
    return len(set(get_card_suit(card) for card in hand)) == 1


def is_full_house(hand):
    """Ввозвращает True, если выпал Фулл-хаус, иначе False"""
    return is_one_pair(hand) and is_three_of_a_kind(hand)


def is_four_of_a_kind(hand):
    """Ввозвращает True, если выпал Каре, иначе False"""
    hand_values = [get_card_value(card) for card in hand]
    val_count = {card: hand_values.count(card) for card in hand_values}
    return 4 in val_count.values()


def is_straight_flush(hand):
    """Ввозвращает True, если выпал Стрит-флеш, иначе False"""
    return is_straight(hand) and is_flush(hand)


def is_royal_flush(hand):
    """Ввозвращает True, если выпал Флеш-рояль, иначе False"""
    hand_vals = [get_card_value(card) for card in hand]
    valid_cards = ['A', 'K', 'Q', 'J', 'T']
    if is_flush(hand):
        for valid in valid_cards:
            return valid not in hand_vals
    return False


def get_first_hand_max(hand):
    """Возвращает значение первой максимальной карты в руке"""
    hand_vals = {card: CARD_RANKS[card[:-1]] for card in hand}
    return max(hand_vals.values())


def get_second_hand_max(hand):
    """Возвращает значение второй максимальной карты в руке"""
    hand_vals = sorted([(card, CARD_RANKS[card[:-1]]) for card in hand], key=operator.itemgetter(1), reverse=True)
    return hand_vals[1][1]


def get_hand_score(hand):
    """Возвращает руку и её счёт"""
    hand_score = {is_one_pair(hand): 1, is_two_pair(hand): 2, is_three_of_a_kind(hand): 3, is_straight(hand): 4,
                  is_flush(hand): 5, is_full_house(hand): 6, is_four_of_a_kind(hand): 7, is_straight_flush(hand): 8,
                  is_royal_flush(hand): 9}
    total = 0
    for x, y in hand_score.items():
        if x:
            total += y
    return hand, total


def compare_hands(hand1, hand2):
    """Возвращает 1, если выиграл первый игрок, и 2, если выиграл второй игрок"""
    hand1, score1 = get_hand_score(hand1)
    hand2, score2 = get_hand_score(hand2)
    if score1 == score2 == 0:
        max1 = get_first_hand_max(hand1)
        max2 = get_first_hand_max(hand2)
        if max1 > max2:
            return 1
        if max2 > max1:
            return 2
        if max1 == max2:
            max11 = get_second_hand_max(hand1)
            max22 = get_second_hand_max(hand2)
            if max11 > max22:
                return 1
            if max22 > max11:
                return 2
    if score1 == score2 == 1:
        max1 = CARD_RANKS[is_one_pair(hand1)[1]]
        max2 = CARD_RANKS[is_one_pair(hand2)[1]]
        if max1 > max2:
            return 1
        if max2 > max1:
            return 2
    if score1 > score2:
        return 1
    if score2 > score1:
        return 2


if __name__ == '__main__':
    hands1, hands2 = get_hands('p054_poker.txt')
    scores = [compare_hands(hands1[i], hands2[i]) for i in range(len(hands1) - 1)]
    player1_score = sum(1 for player in scores if player == 1)
    print(f'Player 1 score: {player1_score}')
