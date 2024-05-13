from services.admin_services import format_user_details, category_members_details
from services.topics_services import format_reply_details
from services.messenger_services import format_chat_history, format_chat_details


def test_format_chat_history():
    # Arrange & Act
    data = [(1, 'Hello There', '2024-30-04', 'Alexandur', 'Daskalov'),
            (2, 'Hello Alex', '2024-30-05', 'Chavdar', 'Kostadinov')]

    empty_data = []

    expected = [{'Sender': 'Alexandur Daskalov', 'Sent time': '2024-30-04', 'Message': 'Hello There'},
                {'Sender': 'Chavdar Kostadinov', 'Sent time': '2024-30-05', 'Message': 'Hello Alex'}]

    # Assert
    assert format_chat_history(data) == expected
    assert format_chat_history(empty_data) == []


def test_format_chat_details():
    # Arrange & Act
    data = [('Teams', 1), ('Summer Vacation', 2)]
    expected = [{'Chat ID': 1, 'Chat Name': 'Teams'}, {'Chat ID': 2, 'Chat Name': 'Summer Vacation'}]

    # Assert
    assert format_chat_details(data) == expected


def test_format_topic_details():
    # Arrange & Act
    data = []
    empty_data = []
    expected = []

    # Assert


def test_format_reply_details():
    # Arrange & Act
    data = [(1, '2000-10-10', 'Australians are just British Texans', 22, 22, 1),
            (2, '2000-10-10', 'Milk is cereal sauce', 22, 22, 2)]
    empty_data = []
    expected = [
        {"Reply ID": 1, "Date posted": '2000-10-10', "Reply content": 'Australians are just British Texans',
         "Likes": 22, "Dislikes": 22, "User ID": 1},

        {"Reply ID": 2, "Date posted": '2000-10-10', "Reply content": 'Milk is cereal sauce',
         "Likes": 22, "Dislikes": 22, "User ID": 2}]

    # Assert
    assert format_reply_details(data) == expected
    assert format_reply_details(empty_data) == []


def test_category_members_details():
    # Arrange & Act
    data = [(1, 1, 1, 'Dog Toys', 'AlexD'), (2, 1, 2, 'Dog Toys', 'ChavK')]
    empty_data = []
    expected = [{'User ID': 1, 'Username': "AlexD", 'Category ID': 1, 'Category Name': 'Dog Toys',
                 'Access level': 'Read Only'},
                {'User ID': 2, 'Username': "ChavK", 'Category ID': 1, 'Category Name': 'Dog Toys',
                 'Access level': 'Full access'}]

    # Assert
    assert category_members_details(data) == expected
    assert category_members_details(empty_data) == []


def test_format_user_details():
    # Arrange & Act
    data = [(1, 'AlexD', '0000', 'Alexandur', 'Daskalov', 'owner', 'AlexD@gmail.com', '1888-10-10'),
            (2, 'ChavK', '0000', 'Chavdar', 'Kostadinov', 'owner', 'ChavK@gmail.com', '1888-10-10')]
    empty_data = []
    expected = [
        {'User ID': 1, 'Username': 'AlexD', 'Password': '0000', 'First name': 'Alexandur',
         'Last name': 'Daskalov', 'role': 'owner', 'E-mail:': 'AlexD@gmail.com', 'Birth date:': '1888-10-10'},

        {'User ID': 2, 'Username': 'ChavK', 'Password': '0000', 'First name': 'Chavdar',
         'Last name': 'Kostadinov', 'role': 'owner', 'E-mail:': 'ChavK@gmail.com', 'Birth date:': '1888-10-10'}]

    # Assert
    assert format_user_details(data) == expected
    assert format_user_details(empty_data) == []
