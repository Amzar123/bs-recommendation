"""
Import required dependencies
"""
from src.service.data_preprocessing import DataPreProcessing
from src.repository.recommendation_repo import RecommendationRepo
from src.repository.student_repository import StudentRepo

from mlxtend.frequent_patterns import fpgrowth, association_rules



import pandas as pd


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
