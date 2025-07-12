#imports
from datetime import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
    current_user,
    unset_jwt_cookies,
)
from mongoengine import connect
from flask_bcrypt import Bcrypt
from config import MONGODB_CONNECTION_STRING, SECRET_KEY, Config
from models.models import UserModel, PostModel, CommentModel, VoteModel
from bson import ObjectId
from bson.errors import InvalidId
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# flask uygulamasını oluşturuyoruz. 
# JWT_SECRET_KEY değerini config.py dosyasından alıyoruz. 
# JWTManager ile JWT kimlik doğrulaması yapabilmek için JWTManager nesnesi oluşturuyoruz.
# Bcrypt ile şifreleme yapabilmek için Bcrypt nesnesi oluşturuyoruz.
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
bcrypt = Bcrypt()
CORS(app, supports_credentials=True)

# API ve Swagger dokümantasyonu
api = Api(
    app,
    version='1.0',
    title='Campfire Microblog API',
    description='Twitter-like micro blogging platform API',
    doc='/docs/',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type 'Bearer <JWT>' where JWT is the token"
        }
    },
    security='apikey'
)

# Namespaces
auth_ns = Namespace('auth', description='Authentication operations')
user_ns = Namespace('users', description='User operations')
post_ns = Namespace('posts', description='Post operations')
comment_ns = Namespace('comments', description='Comment operations')
vote_ns = Namespace('votes', description='Vote operations')

# Add namespaces to API
api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(post_ns)
api.add_namespace(comment_ns)
api.add_namespace(vote_ns)

# mongodb bağlantısını gerçekleştiriyoruz.
db = connect("my_database", host=MONGODB_CONNECTION_STRING)

# API Models for Swagger documentation
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'name': fields.String(required=True, description='First name'),
    'surname': fields.String(required=True, description='Last name'),
    'birthdate': fields.String(required=True, description='Birth date'),
    'gender': fields.String(required=True, description='Gender'),
    'profile_image_url': fields.String(required=True, description='Profile image URL')
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

post_model = api.model('Post', {
    'title': fields.String(required=True, description='Post title'),
    'content': fields.String(required=True, description='Post content')
})

comment_model = api.model('Comment', {
    'content': fields.String(required=True, description='Comment content')
})

vote_model = api.model('Vote', {
    'vote_type': fields.String(required=True, enum=['upvote', 'downvote'], description='Vote type')
})

# Authentication endpoints
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    @auth_ns.response(201, 'User registered successfully')
    @auth_ns.response(400, 'Username already taken')
    def post(self):
        """Register a new user"""
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        surname = data.get("surname")
        birthdate = data.get("birthdate")
        gender = data.get("gender")
        profile_image_url = data.get("profile_image_url")

        # kullanıcı kontrolü
        existing_user = UserModel.objects(username=username).first()
        if existing_user:
            return {"message": "Kullanıcı adı zaten alınmış."}, 400

        new_user = UserModel(
            username=username,
            email=email,
            name=name,
            surname=surname,
            birthdate=birthdate,
            gender=gender,
            profile_image=profile_image_url,
        )
        new_user.set_password(password)
        new_user.save()

        access_token = create_access_token(identity=str(new_user.id))
        return {"message": "Kayıt başarılı.", "access_token": access_token}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Login user"""
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # kullanıcı adı ve şifre kontrolü
        user = UserModel.objects(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return {
                "message": "Giriş başarılı",
                "access_token": access_token,
                "username": user.username
            }, 200
        else:
            return {"message": "Kullanıcı adı veya şifre yanlış."}, 401

@auth_ns.route('/logout')
class Logout(Resource):
    @auth_ns.doc(security='apikey')
    @jwt_required()
    @auth_ns.response(200, 'Logout successful')
    def post(self):
        """Logout user"""
        return {"message": "Çıkış başarılı."}, 200

# User endpoints
@user_ns.route('/profile')
class Profile(Resource):
    @user_ns.doc(security='apikey')
    @jwt_required()
    @user_ns.response(200, 'Profile retrieved successfully')
    @user_ns.response(404, 'User not found')
    def get(self):
        """Get authenticated user profile"""
        user_id = get_jwt_identity()

        try:
            user = UserModel.objects(id=user_id).first()
        except:
            return {"message": "Kullanıcı bulunamadı."}, 404
        
        if user:
            return {
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "surname": user.surname
            }, 200
        else:
            return {"message": "Kullanıcı bulunamadı."}, 404

@user_ns.route('/users')
class Users(Resource):
    @user_ns.response(200, 'Users retrieved successfully')
    def get(self):
        """Get all users"""
        users = UserModel.objects().all()
        user_list = [user.to_dict() for user in users]
        return {"users": user_list}

# Post endpoints
@post_ns.route('/create')
class CreatePost(Resource):
    @post_ns.doc(security='apikey')
    @jwt_required()
    @post_ns.expect(post_model)
    @post_ns.response(201, 'Post created successfully')
    @post_ns.response(404, 'User not found')
    def post(self):
        """Create a new post"""
        data = request.get_json()
        author_id = get_jwt_identity()
        title = data.get("title")
        content = data.get("content")

        author = UserModel.objects(id=author_id).first()

        if not author:
            return {"message": "Kullanıcı bulunamadı."}, 404

        new_post = PostModel(author=author_id, title=title, content=content)
        new_post.save()

        return {
            "message": "Post başarıyla oluşturuldu.", 
            "post": new_post.to_dict()
        }, 201

@post_ns.route('/user_posts')
class UserPosts(Resource):
    @post_ns.doc(security='apikey')
    @jwt_required()
    @post_ns.response(200, 'User posts retrieved successfully')
    def get(self):
        """Get posts by authenticated user"""
        verify_jwt_in_request()
        author = get_jwt_identity()
        posts = PostModel.objects(author=author).all()
        post_list = [post.to_dict() for post in posts]
        return {"posts": post_list}

@post_ns.route('/<post_id>')
class Post(Resource):
    @post_ns.response(200, 'Post retrieved successfully')
    @post_ns.response(404, 'Post not found')
    def get(self, post_id):
        """Get a specific post"""
        post = PostModel.objects(id=post_id).first()
        if post:
            post_dict = post.to_dict()
            post_dict["_id"] = str(post_dict["_id"])
            return {"post": post.to_dict()}, 200
        else:
            return {"message": "Post bulunamadı."}, 404

    @post_ns.doc(security='apikey')
    @jwt_required()
    @post_ns.response(200, 'Post deleted successfully')
    @post_ns.response(404, 'Post not found or no permission')
    def delete(self, post_id):
        """Delete a post"""
        current_user = get_jwt_identity()
        post = PostModel.objects(id=post_id, author=current_user).first()

        if post:
            post.delete()
            return {"message": "Post başarıyla silindi."}, 200
        else:
            return {"message": "Post bulunamadı veya silme izni yok"}, 404

@post_ns.route('/all')
class AllPosts(Resource):
    @post_ns.response(200, 'All posts retrieved successfully')
    def get(self):
        """Get all posts"""
        posts = PostModel.objects().all()
        post_list = [post.to_dict() for post in posts]

        for post_dict in post_list:
            post_dict["_id"] = str(post_dict["_id"])

        return {"posts": post_list}

# Comment endpoints
@comment_ns.route('/<post_id>')
class AddComment(Resource):
    @comment_ns.doc(security='apikey')
    @jwt_required()
    @comment_ns.expect(comment_model)
    @comment_ns.response(201, 'Comment added successfully')
    @comment_ns.response(400, 'Comment content is empty')
    @comment_ns.response(404, 'Post not found')
    def post(self, post_id):
        """Add a comment to a post"""
        data = request.get_json()
        comment_content = data.get("content")

        if not comment_content:
            return {"message": "Yorum içeriği boş olamaz."}, 400

        try:
            post = PostModel.objects.get(pk=post_id)
        except:
            return {"message": "Post bulunamadı."}, 404

        user_id = str(current_user.id)

        comment = CommentModel(
            user=user_id, comment=comment_content, date=datetime.utcnow()
        )
        comment.save()
        post.comments.append(comment)
        post.save()

        return {"message": "Yorum başarıyla eklendi.", "post": post.to_dict()}, 201

# Vote endpoints
@vote_ns.route('/<post_id>')
class Vote(Resource):
    @vote_ns.doc(security='apikey')
    @jwt_required()
    @vote_ns.expect(vote_model)
    @vote_ns.response(201, 'Vote added successfully')
    @vote_ns.response(400, 'Invalid vote type')
    @vote_ns.response(404, 'Post not found')
    def post(self, post_id):
        """Vote on a post"""
        data = request.get_json()
        vote_type = data.get("vote_type")

        if vote_type not in ["upvote", "downvote"]:
            return {"message": "Geçersiz oy türü."}, 400

        try:
            post = PostModel.objects.get(pk=post_id)
        except:
            return {"message": "Post bulunamadı."}, 404

        user_id = str(current_user.id)

        # Check if user already voted
        existing_vote = VoteModel.objects(user=user_id, post=post_id).first()
        if existing_vote:
            existing_vote.vote_type = vote_type
            existing_vote.save()
        else:
            vote = VoteModel(user=user_id, post=post_id, vote_type=vote_type)
            vote.save()
            post.votes.append(vote)
            post.save()

        return {"message": "Oy başarıyla eklendi.", "post": post.to_dict()}, 201

# JWT kimliğini kullanarak MongoDB'den kullanıcı nesnesini çeken işlev
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    print(f"identity: {identity}")

    try:
        user_id = ObjectId(identity)
        print(f"user_id: {user_id}")
    except InvalidId:
        print("User id is not valid")
        return None
    except Exception as e:
        print("An error occurred", e)
        return None

    user = UserModel.objects(id=user_id).first()

    if user:
        return user
    else:
        print("User not found for id: {user_id}")
        return None

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
