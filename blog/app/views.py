from flask_restx import Resource , Namespace
from . models import Article , Comment , get_all_articles, get_all_comments, create_article
from . api_models import article_model, comment_model, article_input_model
# creation du namespace , racine de tous les endpoints
ns = Namespace ("api")


@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}
    
    
@ns.route("/articles")
class ArticleCollection(Resource):
    @ns.marshal_list_with(article_model)
    def get(self):
        return get_all_articles()
    @ns.expect(article_input_model)
    @ns.marshal_with(article_model)
    def post(self):
        article = create_article(title=ns.payload["title"], content = ns.payload["content"])
        return article, 201
    

@ns.route("/comments")
class CommentCollection(Resource):
    @ns.marshal_list_with(comment_model)
    def get(self):
        return get_all_comments()
