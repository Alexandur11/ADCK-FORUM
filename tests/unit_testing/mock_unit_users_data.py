from models.models import AccessControl
import os

NOT_AUTHORIZED = "Not authorized"
NOT_AUTHENTICATED = "Not authenticated"
USER_NOT_FOUND = 'User not found!'
IS_ADMIN = 'Is admin'
secret_key = os.getenv("SECRET_KEY")


def user_mock():
    return {"role": 'user'}

def admin_mock():
    return {"role": 'admin'}

def owner_mock():
    return {"role": 'owner'}

def read_access_mock():
    return AccessControl(category_id=1, user_id=1)

def write_access_mock():
    return AccessControl(category_id=1, user_id=1)

def revoke_access_mock():
    return AccessControl(category_id=1, user_id=1)


mock_user_details_list = [
        (1, 'username1', 'password1', 'first_name1', 'last_name1', 'role1', 'email1', 'birth_date1'),
        (2, 'username2', 'password2', 'first_name2', 'last_name2', 'role2', 'email2', 'birth_date2')]
def mock_format_user_details(mock_user_details_list):

    mock_formatted_user_details = [
        {
            'User ID': user_detail[0],
            'Username': user_detail[1],
            'First name': user_detail[3],
            'Last name': user_detail[4],
            'role': user_detail[5],
            'E-mail:': user_detail[6],
            'Birth date:': user_detail[7]
        } for user_detail in mock_user_details_list
    ]

    return mock_formatted_user_details


OPEN_CATEGORY_MOCK = [(3, 'Test', 1)]
CLOSED_CATEGORY_MOCK = [(3, 'Test', 0)]
OPEN_TOPIC_MOCK = [(1, 1, 'Test', 1, 1, 10)]
CLOSED_TOPIC_MOCK = [(1, 1, 'Test', 1, 0, 10)]

def mock_format_category_details(category_details_list):
    return [{
        'Category ID': category_detail[0],
        'Category Name': category_detail[1]
    } for category_detail in category_details_list]


MESSAGE_DETAILS_MOCK = [(1, 'Message','Sent time', 'sender', 'sender' )]
CONVERSATIONS_DETAILS_MOCK = [(1, 'Chat name')]
REPLY_DETAILS_MOCK = [(1, '2024-05-09', 'Content', 2, 1, 1, 5)]

def format_chat_history(data):
    return [
        {
            'Sender': f'{info[3]} {info[4]}',
            'Sent time': info[2],
            'Message': info[1]
        }for info in data]

def format_chat_details(conversation_list):
    return [{
        'Chat ID': conversation_detail[1],
        'Chat Name': conversation_detail[0]
    } for conversation_detail in conversation_list]


def format_reply_details(reply_details_list):
    formatted_replies = [{
        "Reply ID": reply_detail[0],
        "Date posted": reply_detail[1],
        "Reply content": reply_detail[2],
        "Likes": reply_detail[3],
        "Dislikes": reply_detail[4],
        "User ID": reply_detail[5],
        "Topic ID": reply_detail[6]
    } for reply_detail in reply_details_list]

    return formatted_replies