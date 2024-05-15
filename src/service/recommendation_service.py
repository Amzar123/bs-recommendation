"""
Import required dependencies
"""
from itertools import combinations
from src.repository.recommendation_repo import RecommendationRepo
from src.repository.student_repository import StudentRepo


class TreeNode:
    """
    This class is for building tree as a node
    """

    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None


class FpGrowth:
    """
    Class for building fp-growth algorithm
    """

    def build_tree(self, dataset, min_support):
        """
        Function for handling building tree
        """
        header_table = {}
        for transaction in dataset:
            for item in transaction:
                header_table[item] = header_table.get(
                    item, 0) + dataset[transaction]

        header_table = {
            k: v for k,
            v in header_table.items() if v >= min_support}
        frequent_items = set(header_table.keys())

        if len(frequent_items) == 0:
            return None, None

        for k in header_table:
            header_table[k] = [header_table[k], None]

        fp_tree = TreeNode('Null Set', 1, None)
        for transaction, count in dataset.items():
            filtered_transaction = [
                item for item in transaction if item in frequent_items]
            filtered_transaction.sort(key=lambda x: (
                header_table[x][0], x), reverse=True)
            if len(filtered_transaction) > 0:
                self.update_tree(
                    filtered_transaction,
                    fp_tree,
                    header_table,
                    count)

        return fp_tree, header_table

    def update_tree(self, transaction, node, header_table, count):
        """
        Function for handling updated tree
        """
        if transaction[0] in node.children:
            node.children[transaction[0]].count += count
        else:
            node.children[transaction[0]] = TreeNode(
                transaction[0], count, node)

            if header_table[transaction[0]][1] is None:
                header_table[transaction[0]][1] = node.children[transaction[0]]
            else:
                self.update_header(
                    header_table[transaction[0]][1], node.children[transaction[0]])

        if len(transaction) > 1:
            self.update_tree(transaction[1:],
                             node.children[transaction[0]],
                             header_table,
                             count)

    def update_header(self, node_to_test, target_node):
        """
        This function handle header update
        """
        while node_to_test.link is not None:
            node_to_test = node_to_test.link
        node_to_test.link = target_node

    def projecting_tree(self, item, header_table):
        """
        This function is for projecting tree
        """
        conditional_pattern_bases = {}
        node = header_table[item][1]
        while node is not None:
            prefix_path = []
            self.ascend_tree(node, prefix_path)
            if len(prefix_path) > 1:
                conditional_pattern_bases[frozenset(
                    prefix_path[1:])] = node.count
            node = node.link
        return conditional_pattern_bases

    def ascend_tree(self, node, prefix_path):
        """
        This is for ascending tree
        """
        if node.parent is not None:
            prefix_path.append(node.name)
            self.ascend_tree(node.parent, prefix_path)

    def pruning_tree(self, header_table, min_support):
        """
        This function for prunning tree
        """
        for item in list(header_table.keys()):
            if header_table[item][0] < min_support:
                del header_table[item]
        for item in header_table:
            if header_table[item][1] is not None:
                header_table[item][1] = None
        return header_table

    def fp_growth(self, dataset, min_support):
        """
        This is for generate fp growth
        """
        fp_tree, header_table = self.build_tree(dataset, min_support)
        frequent_patterns = []

        if fp_tree is None:
            return frequent_patterns

        header_table = self.pruning_tree(header_table, min_support)

        for item in header_table:
            conditional_pattern_bases = self.projecting_tree(
                item, header_table)
            conditional_fp_tree, _ = self.build_tree(
                conditional_pattern_bases, min_support)
            if conditional_fp_tree is not None:
                frequent_sub_patterns = self.fp_growth(
                    conditional_pattern_bases, min_support)
                for pattern in frequent_sub_patterns:
                    frequent_patterns.append(pattern.union([item]))
            else:
                frequent_patterns.append({item})

        return frequent_patterns


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
        # Create object apriori and fp growth

        # get student by ids
        students = self.student_repo.get_student_by_ids(ids)

        # Preprocessing data
        # transactions = []

        # apriori = Apriori(transactions, 3)
        # fpgrowth = FpGrowth()

        # # generate item set with apriori
        # itemsets = apriori.apriori()

        # # generate item set with fpgrowth
        # items = fpgrowth.fp_growth(transactions, 3)

        # print(items, itemsets)

        return students
