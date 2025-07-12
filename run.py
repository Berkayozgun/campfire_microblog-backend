#!/usr/bin/env python3
"""
Campfire Microblog API Runner
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """Main function to run the application"""
    print("🚀 Starting Campfire Microblog API...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if MongoDB connection string is set
    mongodb_connection = os.getenv('MONGODB_CONNECTION_STRING')
    if not mongodb_connection:
        print("⚠️  Warning: MONGODB_CONNECTION_STRING not set, using default")
    
    # Check if secret key is set
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key or secret_key == 'your-secret-key-change-in-production':
        print("⚠️  Warning: Using default SECRET_KEY, change in production")
    
    # Import and run the Flask app
    try:
        from main import app
        print("✅ Application loaded successfully")
        print("📚 API Documentation available at: http://localhost:5000/docs/")
        print("🌐 API Base URL: http://localhost:5000")
        print("🔄 Starting server...")
        
        app.run(
            debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
            host='0.0.0.0',
            port=5000
        )
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 