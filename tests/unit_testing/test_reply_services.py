import pytest
from services import reply_services

REPLY_DETAILS_MOCK = [(1, '2024-05-09', 'Content', 2, 1, 1, 5)]
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
@pytest.mark.asyncio
async def test_get_all_replies(mocker):
    data = REPLY_DETAILS_MOCK
    expected = format_reply_details(data)
    mocker.patch('services.reply_services.read_query', mocker.MagicMock(return_value=data))
    result =  reply_services.get_all()
    assert result == ({'Total replies': len(data)}, expected)