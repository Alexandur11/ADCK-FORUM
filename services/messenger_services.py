from data.database import *
from fastapi import HTTPException
from pydantic import Field

from models.models import Message


async def check_all_conversations(user_id):
    data = read_query('SELECT c.name, gm.conversation_id FROM conversation c JOIN group_member gm ON c.conversation_Id = gm.conversation_id WHERE gm.user_id = %s',
                      (user_id,))


    if any(data):
        result = format_chat_details(data)
        return {'Total conversations': len(data)}, result
    else:
        raise HTTPException(status_code=404, detail='You are currently participating in 0 conversations!')


async def conversation_history(conversation_id: int = Field(..., gt=0)):
    data = get_history(conversation_id)
    if any(data):
        return format_chat_history(data)
    else:
        raise HTTPException(status_code=404, detail='No messages in this conversation yet')



async def delete_conversation_by_id(conversation_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM conversation WHERE conversation_id = %s', (conversation_id,))
    if any(data):
        update_query('DELETE FROM conversation WHERE conversation_id = %s', (conversation_id,))
        return f'Conversation with ID {conversation_id} was successfully deleted!'
    else:
        raise HTTPException(status_code=404, detail=f'No conversation with ID {conversation_id} was found!')


async def room(username, desired_person: str = Field(..., min_items=0), group_name=None):
    if not find_user(desired_person):
        raise HTTPException(status_code=404, detail='Desired person not found!')

    room_name = f'{username}|{desired_person}' if group_name is None else group_name

    existing_rooms = read_query('SELECT * FROM conversation WHERE name = %s', (room_name,))
    if any(existing_rooms):
        return """Write the logic which prompts the user the conversation tab 
        between him and the desired person
        """
    else:
        insert_query('INSERT INTO conversation(name) VALUES (%s)', (room_name,))
        id = read_query('SELECT conversation_id FROM conversation WHERE name = %s', (room_name,))
        return id[0][0]


async def initial_members(room_id, user_id, desired_person):
    desired_person_id = read_query('SELECT user_id FROM users WHERE username = %s', (desired_person,))

    insert_query('INSERT INTO group_member(user_id, conversation_id) VALUES(%s, %s)', (user_id, room_id))
    insert_query('INSERT INTO group_member(user_id, conversation_id) VALUES(%s, %s)', (desired_person_id[0][0], room_id))
    return 'Users successfully added to the chat.'



async def add_another_member(username: str = Field(..., ), conversation_id: int = Field(..., gt=0)):
    user_id = read_query('SELECT user_id FROM users WHERE username = %s', (username,))

    update_query('INSERT INTO group_member(user_id, conversation_id) VALUES (%s, %s)', (user_id[0][0], conversation_id))
    return f'Member with ID {user_id[0][0]} was successfully added to conversation with ID {conversation_id}'


async def your_message(user_id, message: Message):
    # We should also get the sender credentials and parse them from the TOKEN, AND the conversation_id also somehow
    update_query('INSERT INTO message(sender, text, sent_time, conversation_id) VALUES (%s, %s, NOW(), %s)',
                 (user_id, message.text, message.conversation_id))
    return 'Message successfully sent'

def find_user(desired_person):
    return read_query('SELECT user_id FROM users WHERE username = %s', (desired_person,))

def get_history(conversation_id):
    data = read_query('''
        SELECT m.sender, m.text, m.sent_time, u.firstname, u.lastname
        FROM message m
        INNER JOIN users u ON m.sender = u.user_id
        WHERE m.conversation_id = %s
    ''', (conversation_id,))
    return data

def format_chat_history(data):
    return [
        {
            'Sender': f'{info[3]} {info[4]}',
            'Sent time': info[2],
            'Message': info[1]
        }for info in data
    ]

def format_chat_details(conversation_list):
    return [{
        'Chat ID': conversation_detail[1],
        'Chat Name': conversation_detail[0]
    } for conversation_detail in conversation_list]
