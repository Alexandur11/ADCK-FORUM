# Forum API

![Database Schema](https://i.imgur.com/buNwlNU.png)

## Project Description
The Forum API is a web application designed to facilitate online discussions. It provides endpoints for managing categories, topics, replies, user authentication, and administrative actions. Built with FastAPI, this API aims to streamline forum interactions by offering a robust and scalable backend solution.

## Table of Contents
- [How to Install and Run the Project](#installation)
- [How to Use the Project](#usage)
- [Credits](#credits)
- [License](#license)

## How to Install and Run the Project
To install and run the Forum API locally, follow these steps:
1. Clone the repository from GitHub.
2. Install the required dependencies using pip: `pip install -r requirements.txt`.
3. Set up a mySQL database and configure the connection settings in `database.py`.
4. Start the FastAPI server: `uvicorn main:app --reload`.

## How to Use the Project
### Endpoints

#### Authentication:
- `POST /login/token`: User login
- `POST /logout`: User logout
- `GET /register/`: Register page
- `POST /register/register_user`: Register user form

#### Category:
- `GET /categories`: Check all categories
- `DELETE /categories`: Delete category
- `GET /categories/{category_id}`: View category
- `GET /categories/{category_name}`: Get category by name
- `POST /categories/new`: New category

#### Topics:
- `GET /topics`: Check all topics
- `DELETE /topics`: Delete topic
- `GET /topics/{topic_id}`: View topic
- `GET /topics/name_search/{topic_name}`: Get topic by name
- `POST /topics/new`: New topic
- `POST /topics/best_reply/{topic_id}`: Pin best reply

#### Admin:
- `GET /user_panel`: User home
- `GET /admin_panel/users/all`: Get all users
- `GET /admin_panel/users/idsearch/{user_id}`: Search user by ID
- `GET /admin_panel/users/search/{username}`: Search user by username
- `GET /admin_panel/users/logged/{user_id}`: Check if user is logged in
- `GET /admin_panel/users/all/logged_now`: Get all logged-in users
- `DELETE /admin_panel/user/{user_id}`: Delete user
- `PUT /admin_panel/actions/topics/lock/{topic_id}`: Lock topic by ID
- `PUT /admin_panel/actions/topics/unlock/{topic_id}`: Unlock topic by ID
- `PUT /admin_panel/actions/categories/lock/{category_id}`: Lock category by ID
- `PUT /admin_panel/actions/categories/unlock/{category_id}`: Unlock category by ID
- `PUT /admin_panel/actions/users/ban/{user_id}`: Ban user by ID
- `PUT /admin_panel/actions/users/write_access`: Give write access
- `PUT /admin_panel/actions/users/read_access`: Give read access
- `PUT /admin_panel/actions/users/no_access`: Revoke access
- `GET /admin_panel/actions/categories/members/{category_id}`: Get category members

#### Messenger:
- `GET /messenger`: View conversations
- `GET /messenger/{conversation_id}`: View conversation history
- `POST /messenger/new`: New chat
- `DELETE /messenger/delete`: Delete conversation
- `PUT /messenger/add_members`: Insert members
- `POST /messenger/message/new`: Message someone

#### Owner:
- `PUT /owner_panel/promote/{user_id}`: Promote user to admin
- `PUT /owner_panel/demote/{user_id}`: Demote admin to user
- `DELETE /owner_panel/{admin_id}`: Delete admin

## Usage Instructions
### User Authentication:
- Use the `/login/token` endpoint to log in with your credentials.
- After successful login, access protected endpoints requiring authentication.

### Category and Topic Management:
- Create, view, delete, search categories and topics, and add replies to certain topics using the respective endpoints.

### Admin Actions:
- Perform administrative actions such as user management, category/topic locking, and access control.

### Messenger Service:
- Utilize the messenger service to engage in private conversations and send messages.

### Credits
- Developed by Alexander Daskalov and Chavdar Kostadinov
- Inspired by FastAPI documentation
- Database powered by mySQL
