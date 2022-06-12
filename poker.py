#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

import itertools


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    c2r = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    ranks = []
    for card in hand:
        r = card[0]
        ranks.append(int(r) if r.isdecimal() else c2r[r])

    return sorted(ranks, reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    suit = hand[0][1]
    for card in hand:
        if card[1] != suit:
            return False
    return True


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    z = sorted(list(set(ranks)))
    if len(z) < 5:
        return False

    for rank in z:
        print(rank)

    return


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    return


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    return


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт"""
    return


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    return


def test_best_hand():
    print("test_best_hand...")
    assert sorted(best_hand("6C 7C 8C 9C TC 5C JS".split())) == [
        "6C",
        "7C",
        "8C",
        "9C",
        "TC",
    ]
    assert sorted(best_hand("TD TC TH 7C 7D 8C 8S".split())) == [
        "8C",
        "8S",
        "TC",
        "TD",
        "TH",
    ]
    assert sorted(best_hand("JD TC TH 7C 7D 7S 7H".split())) == [
        "7C",
        "7D",
        "7H",
        "7S",
        "JD",
    ]
    print("OK")


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split())) == [
        "7C",
        "8C",
        "9C",
        "JC",
        "TC",
    ]
    assert sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split())) == [
        "7C",
        "TC",
        "TD",
        "TH",
        "TS",
    ]
    assert sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split())) == [
        "7C",
        "7D",
        "7H",
        "7S",
        "JD",
    ]
    print("OK")


if __name__ == "__main__":
    # print(hand_rank("JD TC TH 7C 7D 7S 7H".split()))
    ranks = card_ranks("JD TC TH 7C 7D 7S 7H".split())
    print(card_ranks("JD TC TH 7C 7D 7S 7H".split()))
    straight(ranks)

    # test_best_hand()
    # test_best_wild_hand()