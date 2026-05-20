## FastAPI Backend

This repository focuses strictly on the backend API architecture, covering CRUD operations, secure authentication, and data modeling without a decoupled frontend client. 

### Key Features Implemented
* User Authentication: Secure user registration and login endpoints utilizing hashed passwords and JWT tokens.
* Post Management: Full CRUD capability for creating, viewing, updating, and deleting blog posts.
* Data Validation: Request validation and structured response formatting using Pydantic schemas.
* Database Integration: Persistent data structures managed via SQLAlchemy with modular routing.

### How to Use and Test the Endpoints

Since this repository does not extract or serve a detached frontend layout, you can easily test all functionalities natively through FastAPI's built-in interactive documentation:

1. **Start the local server**: Run:  uvicorn main:app --reload , in server.
2. **Access Interactive Docs**: Open your browser and navigate to `http://127.0.0`.
   http://127.0.0.1:8000/docs go to docs
   There will be 3 things:
   1. Authentication Dashboard:
      Here u can see ur user id token
      Go to authorize button which is in right ,login using ur user credintionals adn then u can post anything in blog,,,,without login in here u cant access post operations.
   3. Posts Operations:
      After login in Authorize button page only u can post anything ,,,when u login the locks will be closed at right side ,,,then u can create a post ,delete ,update it.
   4. Users Operations :
      Create a user here user name and passowrd it will save in database

3.* **Secure Authentication**: User login and registration powered by hashed passwords (using passlib/bcrypt) and JWT tokens to protect user data.

