class RecommendationRepo:
    def __init__(self, db):
        self.db = db

    def get_recommendations(self):
        return "this is response from repo"
        # query = f"""
        #     SELECT
        #         r.id,
        #         r.title,
        #         r.author,
        #         r.publication_year,
        #         r.genre,
        #         r.image_url
        #     FROM
        #         recommendations r
        #     WHERE
        #         r.user_id = {user_id}
        # """
        # return self.db.execute_query(query)
