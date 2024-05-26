from itertools import combinations


class Apriori:
    """
    This class is for handling apriori algorithm
    """

    def __init__(self, transactions, min_support):
        self.itemsets = {}
        self.transactions = transactions
        self.min_support = min_support

    def subsets(self, itemset, transaction):
        """
        This function is to building subsets of the items
        """
        return [
            subset for subset in combinations(
                transaction,
                len(itemset)) if set(subset).issubset(itemset)]

    def is_valid_candidate(self, candidate, l_k_minus, k):
        """
        This function is for validating a candidate item
        """
        # Check if all subsets of size k-1 are in Lk_minus_1
        subsets = combinations(candidate, k - 1)
        for subset in subsets:
            if subset not in l_k_minus:
                return False
        return True

    def generate_candidates(self, l_k_minus, k):
        """
        This function is to generating candidate
        """
        candidates = set()
        for itemset1 in l_k_minus:
            for itemset2 in l_k_minus:
                if len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if self.is_valid_candidate(candidate, l_k_minus, k):
                        candidates.add(candidate)
        return candidates

    def apriori(self):
        """
        This is the main function to building apriori
        """
        itemsets = {}
        # Inisialisasi L1
        l1 = {}
        for transaction in self.transactions:
            for item in transaction:
                l1[frozenset([item])] = l1.get(frozenset([item]), 0) + 1

        # Pruning
        l1 = {item: support for item, support in l1.items() if support >=
              self.min_support}
        itemsets[1] = l1

        k = 2
        while True:
            # Generate Ck
            ck = self.generate_candidates(itemsets[k - 1], k)
            if not ck:
                break

            # Count support for Ck
            count = {}
            for transaction in self.transactions:
                ct = self.subsets(ck, transaction)
                for candidate in ct:
                    count[candidate] = count.get(candidate, 0) + 1

            # Pruning
            lk = {itemset: support for itemset,
                  support in count.items() if support >= self.min_support}
            if not lk:
                break

            itemsets[k] = lk
            k += 1

        return itemsets
