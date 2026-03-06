from extensions import db
from app.models.chat import Chat


def send_message(sender_id, receiver_id, message):

    chat = Chat(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=message
    )

    db.session.add(chat)
    db.session.commit()

    return chat


def get_chat_history(user1, user2):

    chats = Chat.query.filter(
        ((Chat.sender_id == user1) & (Chat.receiver_id == user2)) |
        ((Chat.sender_id == user2) & (Chat.receiver_id == user1))
    ).order_by(Chat.created_at.asc()).all()

    return chats