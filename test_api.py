import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_api():
    """Test the API endpoints"""
    print("🧪 Testing Campfire Microblog API...")
    
    # Test 1: Get all posts (should work without auth)
    print("\n1. Testing GET /posts/all...")
    try:
        response = requests.get(f"{BASE_URL}/posts/all")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Success: Can get all posts")
        else:
            print("   ❌ Failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Register a new user
    print("\n2. Testing POST /auth/register...")
    register_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test{int(time.time())}@example.com",
        "password": "123456",
        "name": "Test",
        "surname": "User",
        "birthdate": "1990-01-01",
        "gender": "male",
        "profile_image_url": "https://example.com/profile.jpg"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Success: User registered")
            token = response.json().get("access_token")
        else:
            print(f"   ❌ Failed: {response.text}")
            token = None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        token = None
    
    # Test 3: Login
    print("\n3. Testing POST /auth/login...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Success: User logged in")
            token = response.json().get("access_token")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Create a post (with auth)
    print("\n4. Testing POST /posts/create...")
    if token:
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/posts/create",
                json=post_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                print("   ✅ Success: Post created")
                post_id = response.json().get("post", {}).get("_id")
            else:
                print(f"   ❌ Failed: {response.text}")
                post_id = None
        except Exception as e:
            print(f"   ❌ Error: {e}")
            post_id = None
    else:
        print("   ⏭️  Skipped: No token available")
        post_id = None
    
    # Test 5: Get user profile (with auth)
    print("\n5. Testing GET /users/profile...")
    if token:
        try:
            response = requests.get(
                f"{BASE_URL}/users/profile",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Success: Profile retrieved")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ⏭️  Skipped: No token available")
    
    # Test 6: Add comment (with auth)
    print("\n6. Testing POST /comments/<post_id>...")
    if token and post_id:
        comment_data = {
            "content": "This is a test comment"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/comments/{post_id}",
                json=comment_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                print("   ✅ Success: Comment added")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ⏭️  Skipped: No token or post_id available")
    
    # Test 7: Vote on post (with auth)
    print("\n7. Testing POST /votes/<post_id>...")
    if token and post_id:
        vote_data = {
            "vote_type": "upvote"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/votes/{post_id}",
                json=vote_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                print("   ✅ Success: Vote added")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ⏭️  Skipped: No token or post_id available")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api() 