# Campfire Microblog API

Twitter-like micro blogging platform backend API, built with Flask and MongoDB.

## 🚀 Features

- **User Authentication**: JWT-based authentication system
- **Post Management**: Create, read, update, delete posts
- **Comment System**: Add comments to posts
- **Voting System**: Upvote/downvote posts
- **API Documentation**: Interactive Swagger UI documentation
- **RESTful API**: Clean and organized REST endpoints

## 📋 Prerequisites

- Python 3.8+
- MongoDB
- pip

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Berkayozgun/campfire_microblog-backend.git
   cd campfire_microblog-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   MONGODB_CONNECTION_STRING=mongodb://localhost:27017/campfire_microblog
   SECRET_KEY=your-secret-key-change-in-production
   FLASK_DEBUG=True
   ```

4. **Start MongoDB**
   
   Make sure MongoDB is running on your system.

5. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Interactive Documentation

Once the application is running, you can access the interactive API documentation at:
- **Swagger UI**: `http://localhost:5000/docs/`

### API Endpoints

#### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login user | No |
| POST | `/auth/logout` | Logout user | Yes |

#### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/profile` | Get authenticated user profile | Yes |
| GET | `/users/users` | Get all users | No |

#### Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/posts/create` | Create a new post | Yes |
| GET | `/posts/user_posts` | Get posts by authenticated user | Yes |
| GET | `/posts/<post_id>` | Get a specific post | No |
| DELETE | `/posts/<post_id>` | Delete a post | Yes |
| GET | `/posts/all` | Get all posts | No |

#### Comments

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/comments/<post_id>` | Add a comment to a post | Yes |

#### Votes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/votes/<post_id>` | Vote on a post | Yes |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Register or login to get an access token
2. Include the token in the Authorization header:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

## 📝 Example Usage

### Register a new user
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456",
    "name": "John",
    "surname": "Doe",
    "birthdate": "1990-01-01",
    "gender": "male",
    "profile_image_url": "https://example.com/profile.jpg"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'
```

### Create a post (with authentication)
```bash
curl -X POST http://localhost:5000/posts/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "title": "My First Post",
    "content": "This is my first post content"
  }'
```

### Get all posts
```bash
curl -X GET http://localhost:5000/posts/all
```

## 🏗️ Project Structure

```
campfire_microblog-backend/
├── main.py              # Main application file
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── models/
│   └── models.py       # Database models
├── instance/           # Database files
└── README.md          # This file
```

## 🛡️ Security Features

- **Password Hashing**: Passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Validation**: Request data validation
- **Error Handling**: Comprehensive error responses

## 🔧 Configuration

The application can be configured through environment variables:

- `MONGODB_CONNECTION_STRING`: MongoDB connection string
- `SECRET_KEY`: JWT secret key (change in production)
- `FLASK_DEBUG`: Enable/disable debug mode

## 🚀 Deployment

For production deployment:

1. Set `FLASK_DEBUG=False`
2. Use a strong `SECRET_KEY`
3. Configure MongoDB with proper authentication
4. Use a production WSGI server (e.g., Gunicorn)
5. Set up proper CORS configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues or have questions, please open an issue on GitHub.
