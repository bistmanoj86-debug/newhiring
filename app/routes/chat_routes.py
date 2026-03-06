from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.models.chat import Chat
from app.models.user import User
from extensions import db

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


# ================= CHAT ROOM =================
@chat_bp.route("/", methods=["GET", "POST"])
def chat_home():

    # ---- LOGIN CHECK ----
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    current_user_id = session["user_id"]
    current_role = session.get("role")

    selected_user_id = request.args.get("user_id")

    # ---------- SEND MESSAGE ----------
    if request.method == "POST":

        receiver_id = request.form.get("receiver_id")
        message = request.form.get("message")

        if not receiver_id or not message:
            flash("Message cannot be empty")
            return redirect(url_for("chat.chat_home"))

        new_chat = Chat(
            sender_id=current_user_id,
            receiver_id=int(receiver_id),
            message=message.strip()
        )

        db.session.add(new_chat)
        db.session.commit()

        # redirect back to selected conversation
        return redirect(url_for("chat.chat_home", user_id=receiver_id))


    # ---------- FETCH CHAT MESSAGES ----------
    if selected_user_id:

        selected_user_id = int(selected_user_id)

        chats = Chat.query.filter(
            ((Chat.sender_id == current_user_id) &
             (Chat.receiver_id == selected_user_id)) |

            ((Chat.sender_id == selected_user_id) &
             (Chat.receiver_id == current_user_id))
        ).order_by(Chat.created_at.asc()).all()

    else:

        chats = []


    # ---------- USER FILTER BASED ON ROLE ----------

    if current_role == "candidate":

        users = User.query.filter_by(role="recruiter").all()

    elif current_role == "recruiter":

        users = User.query.filter_by(role="candidate").all()

    elif current_role == "admin":

        users = User.query.filter(User.id != current_user_id).all()

    else:

        users = []


    return render_template(
        "chat/chat_room.html",
        chats=chats,
        users=users,
        selected_user_id=selected_user_id
    )


# ================= ADD TEST CHAT =================
@chat_bp.route("/add-test")
def add_test_chat():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    test_chat = Chat(
        sender_id=session["user_id"],
        receiver_id=1,
        message="Hello 👋"
    )

    db.session.add(test_chat)
    db.session.commit()

    return "Test chat added successfully ✅"