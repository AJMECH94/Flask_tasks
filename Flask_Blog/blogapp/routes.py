from .database import User, Article, Comment
from blogapp import app, db
from flask import Flask, request, jsonify, make_response
import jwt, os
from flask import Flask, request, jsonify
from .auth_middleware import token_required
from datetime import datetime, timedelta


@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.json

    # gets name, email and password
    username, email = data.get('username'), data.get('email')
    password = data.get('password')
    print(data.get('username'))
    print(data.get('email'))
    print(data.get('password'))

    # checking for existing user
    user = User.query.filter_by(email=email).first()
    if not user:
        # database ORM object
        user = User(
            username=username,
            email=email,
            password=password
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.json
    print(auth.get('email'))
    print(auth.get('password'))
    email = auth.get('email')
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query.filter_by(email=email).first()
    print(user)
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if user:
        # generates the JWT Token
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route("/users/", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": current_user
    })


@app.route("/post/", methods=["POST"])
#@token_required
def add_post():
    try:
        post = request.json
        if not post:
            return {
                "message": "Invalid data, you need to give the book title, cover image, author id,",
                "data": None,
                "error": "Bad Request"
            }, 400
        article = Article(title=post['title'],content=post['content'] )
        #if post["user_id"] == current_user["_id"]:
        db.session.add(article)
        db.session.commit()
        if not post:
            return {
                "message": "The post has been created by user",
                "data": None,
                "error": "Conflict"
            }, 400

        return jsonify({
            "message": "successfully created a new post",
            "data": post
        }), 201

    except Exception as e:
        return jsonify({
            "message": "failed to create a new post",
            "error": str(e),
            "data": None
        }), 500


@app.route("/getarticle/", methods=["GET"])
#@token_required
def get_posts():
    data = request.json
    user_id = data['user_id']
    print(user_id)
    try:
        posts = Article().get_by_user_id(user_id)
        print(posts)
        return jsonify({
            "message": "successfully retrieved all posts",
            "data": posts
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all post",
            "error": str(e),
            "data": None
        }), 500


@app.route("/posts/<posts_id>", methods=["GET"])
@token_required
def get_post(current_user, post_id):
    try:
        post = Article().get_by_id(post_id)
        if not post:
            return {
                "message": "post not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a book",
            "data": post
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500


@app.route("/post/<post_id>", methods=["PUT"])
@token_required
def update_post(current_user, post_id):
    try:
        post = Article().get_by_id(post_id)
        if not book or book["user_id"] != current_user["_id"]:
            return {
                "message": "Book not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        post = request.json
        post = Article().update(post_id)
        return jsonify({
            "message": "successfully updated a book",
            "data": post
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to update a book",
            "error": str(e),
            "data": None
        }), 400


@app.route("/posts/<posts_id>", methods=["DELETE"])
@token_required
def delete_book(current_user, post_id):
    try:
        post = Article().get_by_id(post_id)
        if not post or post["user_id"] != current_user["_id"]:
            return {
                "message": "post not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        Article().delete(post_id)
        return jsonify({
            "message": "successfully deleted a post",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to delete a post",
            "error": str(e),
            "data": None
        }), 400


@app.route('/articles/<article_id/comments', methods=['GET'])
def list_comments(article_slug):
    page_size = request.args.get('page_size', 5)
    page = request.args.get('page', 1)
    article_id = Article.query.filter_by(slug=article_slug).with_entities('id').first()[0]
    comments = Comment.query.filter_by(article_id=article_id).order_by(desc(Comment.created_at)).paginate(page=page,
                                                                                                          per_page=page_size)
    return jsonify({
            "message": "successfully get a comments",
            "data": comments
        }), 200


@app.route('/comments/<comment_id>', methods=['GET'])
def show_comment(comment_id):
    comment = Comment.query.get(comment_id)
    return jsonify({
        "message": "successfully get a comments",
        "data": comment
    }), 200


@app.route('/articles/<article_slug>/comments', methods=['POST'])
def create_comment(article_slug):
    content = request.json.get('content')
    user_id = request.json.get('id')
    article_id = db.session.query(Article.id).filter_by(slug=article_slug).first()[0]
    comment = Comment(content=content, user_id=user_id, article_id=article_id)

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "message": "successfully create a comments",
        "data": comment
    }), 200
