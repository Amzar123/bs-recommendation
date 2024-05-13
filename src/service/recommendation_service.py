"""
Import required dependencies
"""
from itertools import combinations
from src.repository.recommendation_repo import RecommendationRepo
from src.repository.student_repository import StudentRepo


class RecommendationService:
    """
    This class is for serve recommendation
    """

    def __init__(
            self,
            recommendation_repo: RecommendationRepo,
            student_repo: StudentRepo):
        self.recommendation_repo = recommendation_repo
        self.student_repo = student_repo

    def __subsets(self, itemset, transaction):
        return [
            subset for subset in combinations(
                transaction,
                len(itemset)) if set(subset).issubset(itemset)]

    def __is_valid_candidate(self, candidate, Lk_minus_1, k):
        # Check if all subsets of size k-1 are in Lk_minus_1
        subsets = combinations(candidate, k - 1)
        for subset in subsets:
            if subset not in Lk_minus_1:
                return False
        return True

    def __generate_candidates(self, Lk_minus_1, k):
        candidates = set()
        for itemset1 in Lk_minus_1:
            for itemset2 in Lk_minus_1:
                if len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if self.__is_valid_candidate(candidate, Lk_minus_1, k):
                        candidates.add(candidate)
        return candidates

    def __apriori(self, transactions, min_support):
        itemsets = {}
        # Inisialisasi L1
        L1 = {}
        for transaction in transactions:
            for item in transaction:
                L1[frozenset([item])] = L1.get(frozenset([item]), 0) + 1

        # Pruning
        L1 = {item: support for item, support in L1.items() if support >=
              min_support}
        itemsets[1] = L1

        k = 2
        while True:
            # Generate Ck
            Ck = self.__generate_candidates(itemsets[k - 1], k)
            if not Ck:
                break

            # Count support for Ck
            count = {}
            for transaction in transactions:
                Ct = self.__subsets(Ck, transaction)
                for candidate in Ct:
                    count[candidate] = count.get(candidate, 0) + 1

            # Pruning
            Lk = {itemset: support for itemset,
                  support in count.items() if support >= min_support}
            if not Lk:
                break

            itemsets[k] = Lk
            k += 1

        return itemsets

    def __fpgrowth(self):
        return "to be implemented"

    def get_recommendations(self, ids: list):
        """
        Function to handle get recommendation
        """
        result = self.recommendation_repo.get_recommendations(ids)
        return result

    def generate_recommendations(self, ids: list):
        """
        Function to handle generate recommendation
        """
        # get student by ids
        students = self.student_repo.get_student_by_ids(ids)

        # Preprocessing data
        transactions = []

        # generate item set with apriori
        itemsets = self.__apriori(transactions, 3)

        # generate item set with fpgrowth
        items = self.__fpgrowth()

        print(items, itemsets)

        return students
