from flask_restx import fields
from .extensions import api

article_model = api.model("Article", {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String
})

comment_model = api.model("Comment", {
    "id": fields.Integer,
    "content": fields.String,
    "article_id": fields.Integer
})


article_input_model = api.model("ArticleInput", {
    "title": fields.String,
    "content": fields.String
})