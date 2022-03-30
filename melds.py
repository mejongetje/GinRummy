from functools import reduce
from itertools import chain, combinations, groupby

import more_itertools as mit


def find_runs(cards):
    """Function returns all runs in a sequence of cards"""
    hand_copy = cards[:]
    hand_id = [card.id for card in hand_copy]
    hand_id.sort()
    for group in mit.consecutive_groups(hand_id):
        group = list(group)
        if len(group) >= 3:
            raw_runs = [card for card in hand_copy for id in group if id == card.id]
            raw_runs.sort()
            yield raw_runs
        else:
            pass

def find_sets(cards):
    """Function returns all sets in a sequence of cards"""
    hand_copy = cards[:]
    hand_sort = sorted(hand_copy, key=lambda x: x.rank)
    raw_sets = []        
    result = groupby(hand_sort, key=lambda x: x.rank)
    groups_list = [(key, list(items)) for key, items in result]
    for i in range(len(groups_list)):
        sets = groups_list[i][1]
        if len(sets) >= 3:
            raw_sets += [sets]
    return raw_sets
    

def find_overlaps(raw_runs, raw_sets):
    """Returns a list of cards that overlap runs and sets"""
    overlaps = set(set(chain(*raw_runs))).intersection(set(chain(*raw_sets)))
    if list(overlaps):
        return list(overlaps)
    return []


class Melds:

    def __init__(self, cards):
        self.cards = cards
        self.melds = self.set_melds()


    def set_melds(self):
        raw_runs_it = find_runs(self.cards)
        raw_runs = list(raw_runs_it)
        raw_sets = find_sets(self.cards)
        if find_overlaps(raw_runs, raw_sets):
            return self.find_best_meld_combination(raw_runs, raw_sets)
        return [*raw_runs, *raw_sets]


    def find_all_set_combinations(self, sets):
        """Helper method for find_all_combinations()"""
        all_sets = []
        for set_ in sets:
            set_combos = []
            for i in range(len(set_)+1):
                for set_combo in combinations(set_, i):
                    if len(set_combo) >= 3:
                        set_combos.append(list(set_combo))
            all_sets += set_combos
        return all_sets


    def find_all_run_combinations(self, runs):
        """Helper method for find_all_combinations()"""
        combos = self.find_all_combinations_in_runs(runs)
        l = list(combos)
        for run in list(chain(*l)):
            run_ids = [card.id for card in run]
            for group in mit.consecutive_groups(run_ids):
                group = list(group)
                if len(group) >= 3:
                    run_group = [card for card in run for id in run_ids if id == card.id]
                    run_group.sort()
                    yield run_group


    def find_all_combinations_in_runs(self, runs):
        """Helper function for find_all_run_combinations()"""
        all_combos = []
        for run in runs:
            combos = []
            for i in range(len(run)+1):
                for combo in combinations(run, i):
                    if len(combo) >= 3:
                        combos.append(combo)
            all_combos += combos
        yield all_combos


    def find_all_combinations(self, raw_runs: list, raw_sets: list) -> list:
        """Method returns all valid meld combinations in a sequence of cards"""
        runs_it = self.find_all_run_combinations(raw_runs)
        runs = list(runs_it)
        sets = self.find_all_set_combinations(raw_sets)
        raw_melds = list(chain(runs, sets))
        combos = []
        for i in range(len(raw_melds)+1):
            for combo in combinations(raw_melds, i):
                combos.append(list(combo))
        return combos


    def find_all_combinations_without_overlap(self, all_combos: list) -> list:
        """Method returns al list of all meld combinations without any overlapping cards"""
        no_overlap_combos = []
        for combo in all_combos:
            combo_ids = [card.id for card in list(chain(*combo))]
            if len(combo_ids) == len(set(combo_ids)):
                no_overlap_combos.append(combo)
        return no_overlap_combos


    def find_best_meld_combination(self, raw_runs, raw_sets):
        """Method returns the best meld combination from a sequence of meld combinations"""
        all_combos = self.find_all_combinations(raw_runs, raw_sets)
        no_overlap_combos = self.find_all_combinations_without_overlap(all_combos)
        best_combo = reduce(lambda a,b: a if sum([card.value for card in list(chain(*a))]) >
        sum([card.value for card in list(chain(*b))]) else b, list(chain(no_overlap_combos)))
        return best_combo
