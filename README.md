# 🔥 Campfire Microblog Backend

A RESTful API built with **Flask**, **MongoDB**, and **Docker**. Designed to handle social interactions like posting, commenting, and voting with high performance and scalability.

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white) 
![Flask](https://img.shields.io/badge/Flask-RESTx-black?style=for-the-badge&logo=flask&logoColor=white) 
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white) 
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white) 
![Swagger](https://img.shields.io/badge/Swagger-API_Docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

---

### 🌟 Features

- **🔐 JWT Authentication:** Secure, stateless authentication using `Flask-JWT-Extended`.
- **📝 Posts:** Create, read, and delete micro-blogging posts.
- **💬 Comments:** Reference-based architecture to handle thousands of comments per post.
- **🗳️ Voting:** Atomic upvote/downvote mechanism with real-time updates.
- **🐳 Containerized:** Ready for deployment with Docker and Docker Compose.
- **📖 Auto-Docs:** Interactive Swagger UI for easy API testing.

---

### 🚀 Quick Start (Docker)

This is the preferred method to run the application in a consistent environment.

#### Step 1: Clone the repository
```bash
git clone https://github.com/Berkayozgun/campfire_microblog-backend.git
cd campfire_microblog-backend
```

#### Step 2: Create Environment Variables
Create a `.env` file in the root directory:
```env
MONGODB_CONNECTION_STRING=your_mongodb_connection_string
SECRET_KEY=your_secured_secret_key
FLASK_DEBUG=True
```

#### Step 3: Launch with Docker Compose
```bash
sudo docker compose up --build
```

The API will be available at: `http://localhost:5000`

---

### 📖 API Documentation

The project includes built-in Swagger documentation powered by **Flask-RESTx**. You can explore and test the endpoints interactively:

🔗 **Interactive Docs:** [http://localhost:5000/docs](http://localhost:5000/docs)

---

### 🛠 Tech Stack

- **Core Framework:** [Flask](https://flask.palletsprojects.com/)
- **API Engine:** [Flask-RESTx](https://flask-restx.readthedocs.io/)
- **Database (ODM):** [MongoEngine](http://mongoengine.org/)
- **Auth:** [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- **Security:** [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
- **Deployment:** [Docker](https://www.docker.com/) & [Gunicorn](https://gunicorn.org/)