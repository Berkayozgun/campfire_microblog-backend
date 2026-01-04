# 🔥 Campfire Backend API

A scalable micro-blogging platform backend built with **Flask**, **MongoDB**, and **Clean Architecture** principles. Designed to handle social interactions like posting, commenting, and voting with high performance.

![Python](https://img.shields.io/badge/Python-3.9-blue) ![Flask](https://img.shields.io/badge/Flask-RESTx-black) ![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

### ⚡ Key Technical Highlights

#### 1. Database Modeling (Reference Strategy)
Instead of embedding all data into a single document, this project uses a **Reference-Based Architecture** with `MongoEngine`.
- **Why?** To bypass MongoDB's 16MB document limit and ensure scalability for posts with thousands of comments.
- **Implementation:** `PostModel` stores references (`ListField(ReferenceField)`) to independent Comment documents.

#### 2. Advanced Voting Logic
Implemented a smart voting mechanism that handles `upvote`, `downvote`, and `un-vote` actions atomically.
- Checks `existing_vote` to prevent duplicate actions.
- Updates references in real-time without locking the entire collection.

#### 3. Secure Authentication
- **JWT Implementation:** Uses `Flask-JWT-Extended` for stateless authentication.
- **Automatic User Loading:** Leveraging `@jwt.user_lookup_loader` to inject the `current_user` object into protected endpoints automatically, keeping controllers clean.

#### 4. Modular API Design
- Built with `flask-restx` namespaces (`/auth`, `/posts`, `/comments`).
- **Auto-Documentation:** Fully integrated Swagger UI available at `/docs`.

---

### 🛠 Installation & Setup

```bash
# Clone the repository
git clone [https://github.com/Berkayozgun/campfire_microblog-backend.git](https://github.com/Berkayozgun/campfire_microblog-backend.git)

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py