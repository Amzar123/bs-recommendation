"""
Import required dependencies
"""
from itertools import combinations
from src.repository.recommendation_repo import RecommendationRepo
from src.repository.student_repository import StudentRepo
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

from CoreNLG.NlgTools import NlgTools
from CoreNLG.PredefObjects import TextVar

import pandas as pd


class NLGCore:
    """
    Class to handle NLGCore
    """

    def __init__(self) -> None:
        self.nlg = NlgTools()

    def generate_text(self, text_list):
        """
        Function to generate text using CoreNLG
        """
        text_rule = TextVar(
            self.nlg.nlg_syn('Kamu harus belajar',
                             'Untuk meningkatkan kemampuan bahasa inggrismu, maka kamu harus belajar '),
            ', '.join([text.lower() for text in text_list[:-1]]) + ', dan ' + text_list[-1].lower() + '.',
            self.nlg.nlg_syn('Semoga rekomendasi nya bisa menjadikan motivasi untuk meningkatkan kemampuanmu!.',
                             'Semangat, semoga sukses pada assessment selanjutnya')
        )

        text = self.nlg.write_text(text_rule)
        return text


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


class DataPreProcessing:
    """
    Class for handling data preprocessing
    """

    def __init__(self) -> None:
        self.obj_nlg = NLGCore()

    def recommend_materials(self, student_competencies, rules):
        """
        Generate recommendation materials
        """
        student_recommendations = {}

        # Define the mapping of competencies to materials
        competency_to_material = {
            "main_verbs": "materi 1",
            "tense": "materi 2",
            "infinitives": "materi 3",
            "passives": "materi 4",
            "have_+_participle": "materi 5",
            "auxiliary_verbs": "materi 6",
            "pronouns": "materi 7",
            "nouns": "materi 8",
            "determiners": "materi 9",
            "other_adjectives": "materi 10",
            "prepositions": "materi 11",
            "conjunctions": "materi 12",
            "subject_verb_agreement": "materi 13"
        }

        material_details = {
            "materi 1": [
                "Penggunaan kata kerja utama dalam kalimat",
                "Perbedaan antara kata kerja aksi dan kata kerja statis",
                "Bentuk kata kerja dalam tenses berbeda"],
            "materi 2": [
                "Present Simple dan Present Continuous",
                "Past Simple dan Past Continuous",
                "Future Simple dan Future Continuous",
                "Present Perfect dan Past Perfect",
                "Penggunaan tenses dalam konteks berbeda"],
            "materi 3": [
                "Penggunaan infinitive (to + verb) dalam kalimat",
                "Infinitive dengan dan tanpa 'to'",
                "Penggunaan infinitive setelah kata kerja tertentu"],
            "materi 4": [
                "Struktur kalimat pasif",
                "Perubahan dari kalimat aktif ke pasif",
                "Penggunaan pasif dalam berbagai tenses"],
            "materi 5": [
                "Penggunaan Present Perfect Tense",
                "Struktur kalimat Present Perfect",
                "Penggunaan Past Perfect Tense"],
            "materi 6": [
                "Penggunaan kata kerja bantu (do, does, did)",
                "Penggunaan modal verbs (can, could, may, might, must, etc.)",
                "Bentuk negatif dan pertanyaan menggunakan kata kerja bantu"],
            "materi 7": [
                "Penggunaan pronoun subjek (I, you, he, she, it, we, they)",
                "Penggunaan pronoun objek (me, you, him, her, it, us, them)",
                "Penggunaan possessive pronouns (my, your, his, her, its, our, their)"],
            "materi 8": [
                "Penggunaan kata benda dalam kalimat",
                "Singular dan plural nouns",
                "Countable dan uncountable nouns"],
            "materi 9": [
                "Penggunaan determiners (a, an, the)",
                "Penggunaan quantifiers (some, any, few, many, etc.)",
                "Penggunaan demonstrative determiners (this, that, these, those)"],
            "materi 10": [
                "Penggunaan adjective dalam kalimat",
                "Perbandingan adjective (comparative dan superlative)",
                "Penggunaan adjective dalam berbagai posisi dalam kalimat"],
            "materi 11": [
                "Penggunaan prepositions of place (in, on, at, etc.)",
                "Penggunaan prepositions of time (in, on, at, etc.)",
                "Prepositions setelah kata kerja tertentu (depend on, listen to, etc.)"],
            "materi 12": [
                "Penggunaan coordinating conjunctions (and, but, or, etc.)",
                "Penggunaan subordinating conjunctions (because, although, if, etc.)",
                "Penggunaan correlative conjunctions (either...or, neither...nor, etc.)"],
            "materi 13": [
                "Kesepakatan antara subjek dan kata kerja",
                "Penggunaan kata kerja dengan subjek tunggal dan jamak",
                "Kesepakatan dalam kalimat kompleks"]}

        # Iterate through each student's competencies
        for student_data in student_competencies:
            student_name = student_data["name"]
            competencies = set(student_data["competencies"])
            # Initialize an empty set to store recommended materials for each
            # student
            recommendations = set()

            # Iterate through each association rule
            for idx, rule in rules.iterrows():
                antecedents = set(rule['antecedents'])
                consequents = set(rule['consequents'])

                uncompeten = list(
                    set(competency_to_material.keys()) - competencies)

                # Check if the student is missing any antecedents
                missing_antecedents = antecedents - set(uncompeten)

                if missing_antecedents:
                    # Recommend all materials related to the missing
                    # antecedents
                    for antecedent in missing_antecedents:
                        if antecedent in competency_to_material:
                            recommendations.add(
                                competency_to_material[antecedent])

            # Map student to recommended materials with details
            student_material_details = []
            for material in recommendations:
                if material in material_details:
                    student_material_details.extend(material_details[material])

            student_recommendations[student_name] = self.obj_nlg.generate_text(
                student_material_details)

        return student_recommendations

    def transform_result_to_biner(self, test_result, questions):
        """
        This function is to transform result to biner data
        """
        question_list = [
            "soal 1",
            "soal 2",
            "soal 3",
            "soal 4 ",
            "soal 5",
            "soal 6",
            "soal 7 ",
            "soal 8 ",
            "soal 9 ",
            "soal 10",
            "soal 11",
            "soal 12",
            "soal 13",
            "soal 14",
            "soal 15",
            "soal 16",
            "soal 17",
            "soal 18",
            "soal 19",
            "soal 20",
            "soal 21",
            "soal 22",
            "soal 23",
            "soal 24",
            "soal 25",
        ]
        index = 0
        for q in question_list:
            for i in range(len(test_result)):
                if questions["key"][index] == "":
                    test_result[q][i] = 0
                elif test_result[q][i] == questions["key"][index]:
                    test_result[q][i] = 1
                else:
                    test_result[q][i] = 0
            index += 1

        return test_result

    def mapping_student_competency(
            self,
            transformed_data,
            df_mapping_question_comp):
        '''
        Implement to map student wrong answers with competencies.
        '''

        # Convert the first column (score) to a separate series and drop it
        # from the DataFrame
        scores = transformed_data.iloc[:, 0]
        student_answers = transformed_data.iloc[:, 1:]

        # Competencies list
        lib = [
            "main_verbs",
            "tense",
            "infinitives",
            "passives",
            "have_+_participle",
            "auxiliary_verbs",
            "pronouns",
            "nouns",
            "determiners",
            "other_adjectives",
            "prepositions",
            "conjunctions",
            "subject_verb_agreement"
        ]

        student_list = []

        for idx, row in student_answers.iterrows():
            student = {"name": f"student_{idx+1}", "competencies": set()}

            for question_index, answer in row.items():
                if answer == 0:  # If the answer is wrong
                    try:
                        # Strip any leading or trailing spaces
                        question_index = question_index.strip()
                        # Extract the question number
                        question_num = int(question_index.split(' ')[-1]) - 1
                        if question_num < len(df_mapping_question_comp):
                            for comp in lib:
                                if df_mapping_question_comp.at[question_num, comp]:
                                    student["competencies"].add(comp)
                    except (ValueError, IndexError) as e:
                        print(
                            f"Skipping invalid question index '{question_index}' for student {idx+1}: {e}")

            # Convert the set to a list for JSON serialization or other
            # processing
            student["competencies"] = list(student["competencies"])
            student_list.append(student)

        return student_list

    def generate_final_dataset(self, mapped_data):
        """
        This function can generate final dataset
        """
        final_dataset = []
        for element in mapped_data:
            final_dataset.append(element['competencies'])
        return final_dataset

    def data_transformation(self, final_dataset):
        """
        This function is to transform data after final data set was generated
        """
        tr = TransactionEncoder()
        tr_ary = tr.fit(final_dataset).transform(final_dataset)
        df_incorrect = pd.DataFrame(tr_ary, columns=tr.columns_)
        return df_incorrect


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
        # Create object for data preprocessing
        data_preprocessing = DataPreProcessing()
        # fp_growth = FpGrowth()

        # read data from csv file
        df_mapping_question_comp = pd.read_csv(
            "./data/kompetensi-soal-etp.csv")
        df_questions = pd.read_csv("./data/soal-etp.csv")
        df_test_results = pd.read_csv("./data/hasil-tes-etp.csv")

        # Data preprocessing
        transormed_data = data_preprocessing.transform_result_to_biner(
            df_test_results, df_questions)
        student_comp = data_preprocessing.mapping_student_competency(
            transormed_data, df_mapping_question_comp)
        final_dataset = data_preprocessing.generate_final_dataset(student_comp)
        transform_dataset = data_preprocessing.data_transformation(
            final_dataset)

        # Data modelling
        items = fpgrowth(transform_dataset, 0.9, use_colnames=True)

        # Building association rules
        rules = association_rules(
            items, metric="confidence", min_threshold=0.9)

        # Generate recommendation materials
        student_recommendations = data_preprocessing.recommend_materials(
            student_comp[:12], rules)

        return student_recommendations
