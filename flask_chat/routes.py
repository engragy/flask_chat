""" app views / routes """
import secrets
import os
from PIL import Image
from datetime import datetime
from flask import render_template, request, url_for, flash, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit

from flask_chat import app, db, crypt, socketio
from flask_chat.forms import (
    RegForm,
    LoginForm,
    ImgUploadForm,
    CreateChannelForm,
    CreateMessegeForm,
)
from flask_chat.models import User, Channel, Messege


# function to save/store user's profile image
def save_img(form_img):
    # creating random name for the image file using secrets module
    random_hex = secrets.token_hex(8)
    _, _ext = os.path.splitext(form_img.filename)
    img_file = random_hex + _ext
    img_path = os.path.join(app.root_path, "static/profile_pics", img_file)
    # resizing the uploaded image
    new_size = (50, 50)
    new_img = Image.open(form_img)
    new_img.thumbnail(new_size)
    new_img.save(img_path)
    return img_file


##############
# app routes #
##############
@app.route("/", methods=["GET", "POST"])
def index():
    imgform = ImgUploadForm(prefix='imgform')
    chform = CreateChannelForm(prefix='chform')
    channels = Channel.query.all()

    # validate user input to ((create channel))
    if chform.validate_on_submit() and current_user.is_authenticated:
        new_ch = Channel(title=chform.chname.data)
        db.session.add(new_ch)
        db.session.commit()
        flash("you've successfuly created a  new Channel", "success")
        return redirect(url_for("index"))
    elif chform.validate_on_submit() and not current_user.is_authenticated:
        flash("you have to login first", "danger")
        return redirect(url_for("login"))

    # validate user input to ((change profile picture))
    elif imgform.validate_on_submit() and current_user.is_authenticated:
        # use the save pictures function
        picture_file = save_img(imgform.image.data)
        # update database
        current_user.image_file = picture_file
        db.session.commit()
        return redirect(url_for("index"))
    elif imgform.validate_on_submit() and not current_user.is_authenticated:
        flash("you have to login first", "danger")
        return redirect(url_for("login"))

    # Get request (display index page, user has loged in)
    elif request.method == "GET" and current_user.is_authenticated:
        userimg = url_for("static", filename="profile_pics/" + current_user.image_file)
        return render_template(
            "index.html",
            imgform=imgform,
            chform=chform,
            u_img=userimg,
            ch_list=channels,
            title="Home",
        )
    # Get request (display index page, no user is loged in)
    else:
        return render_template(
            "index.html",
            imgform=imgform,
            chform=chform,
            ch_list=channels,
            title="Home",
        )


@app.route("/channel/<string:ch_name>", methods=["GET", "POST"])
@login_required
def channel(ch_name):
    # is there a channel by that name
    if Channel.query.filter_by(title=ch_name).first():
        imgform = ImgUploadForm(prefix="imgform")
        chform = CreateChannelForm(prefix="chform")
        msgform = CreateMessegeForm(prefix="msgform")
        channels = Channel.query.all()
        userimg = url_for(
            "static", filename="profile_pics/" + current_user.image_file
        )
        # validate user input to create channel
        if chform.validate_on_submit():
            new_ch = Channel(title=chform.chname.data)
            db.session.add(new_ch)
            db.session.commit()
            flash("you've successfuly created a  new Channel", "success")
            return redirect(url_for("channel", ch_name=ch_name))
        # validate user input to change profile picture
        elif imgform.validate_on_submit():
            # use the save pictures function
            picture_file = save_img(imgform.image.data)
            # update database
            current_user.image_file = picture_file
            db.session.commit()
            return redirect(url_for("channel", ch_name=ch_name))
        # Get request, prepare the list of channels for display and return channel page
        elif request.method == "GET":
            return render_template(
                "channel.html",
                imgform=imgform,
                chform=chform,
                msgform=msgform,
                u_img=userimg,
                ch_list=channels,
                title="Channel-" + ch_name,
            )
    # that channel doesn't exist
    return abort(404)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = RegForm()
        # validate user inputs to (form rules)
        if form.validate_on_submit():
            hashed_pw = crypt.generate_password_hash(form.password.data).decode("utf-8")
            new_user = User(
                username=form.username.data, email=form.email.data, password=hashed_pw
            )
            db.session.add(new_user)
            db.session.commit()
            # return a success message on new account creation
            flash("you've successfuly created an Account, Now you can LogIn", "success")
            return redirect(url_for("login"))
        # Get request (display Register page)
        else:
            return render_template("register.html", form=form, title="Registeration")


@app.route("/login", methods=["GET", "POST"])
def login():
    # is this user already loged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = LoginForm()
        # validate user inputs to (form rules)
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and crypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # is there "next" (logged in users only page) in the url argument
                next_page = request.args.get("next")
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for("index"))
            else:
                # return a falier message on invalid login attempt
                flash(
                    "Login attempt unsuccessful, check your credentials and try again",
                    "danger",
                )
                return render_template("login.html", form=form, title="LogIn")
        # Get request (display Login page)
        else:
            return render_template("login.html", form=form, title="LogIn")


@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("you have Loged out, see you again", "info")
        return redirect(url_for("index"))


@app.errorhandler(404)
def error_404(error):
    imgform = ImgUploadForm(prefix='imgform')
    userimg = url_for(
        "static", filename="profile_pics/" + current_user.image_file
        )
    return render_template(
        'error.html',
        imgform=imgform,
        u_img=userimg,
        title="ERROR",
        ), 404

##############################
# flask socketIO decorators #
##############################

# listen for "all_msgs" to retrieve old messages if there is
@socketio.on("all_msgs")
@login_required
def a_messages(msg_data):
    # get user's active channel
    active_ch = Channel.query.filter_by(title=msg_data["ch_name"]).first()
    # get objects (instences) of all messeges
    allmsg = active_ch.channel_messeges
    # empty list to store all messeges as dictionaries
    msgs = []
    for m in allmsg:
        msg = m.as_dict()
        msg["timestamp"] = msg["timestamp"].strftime("%d %b %Y %I:%M%p")
        msg["user_img"] = url_for(
            "static",
            filename="profile_pics/" + User.query.get(msg["user_id"]).image_file,
        )
        msg["user_id"] = User.query.get(msg["user_id"]).username
        msgs.append(msg)
    # arranging messeges with timestamp as it may not due to deletion
    arranged = sorted(
        msgs, key=lambda x: datetime.strptime(x["timestamp"], "%d %b %Y %I:%M%p")
    )
    # send all messeges to the user
    emit("all_msgs", arranged, broadcast=False)
    socketio.sleep(0)


# listen for a new added messege
@socketio.on("submit_msg")
@login_required
def s_messages(msg_data):
    # get user's active channel
    active_ch = Channel.query.filter_by(title=msg_data["ch_name"]).first()
    # make messege instance
    msg = Messege(
        user_id=current_user.id, channel_id=active_ch.id, messege=msg_data["u_msg"]
    )
    # add messege and save the db
    db.session.add(msg)
    db.session.commit()
    # get the messege as a dictionary and update timestamp to str, user id to its name
    msg = msg.as_dict()
    msg["timestamp"] = msg["timestamp"].strftime("%d %b %Y %I:%M%p")
    msg["user_img"] = url_for(
        "static",
        filename="profile_pics/" + User.query.get(msg["user_id"]).image_file,
    )
    msg["user_id"] = current_user.username
    msg["chat_count"] = active_ch.chat_count()
    # send this new messege to everyone
    emit("new_msg", msg, broadcast=True)
    # work around issue in flasksocketio
    socketio.sleep(0)


# listen for a messege to delete
@socketio.on("delete_msg")
@login_required
def d_messages(msg_data):
    # get user's active channel
    active_ch = Channel.query.filter_by(title=msg_data["ch_name"]).first()
    # get messege instance
    msg = Messege.query.filter_by(
        user_id=current_user.id,
        channel_id=active_ch.id,
        messege=msg_data["u_msg"],
        id=msg_data["del_id"],
    ).first()
    if not msg:
        flash("you can't delete others messeges")
        return redirect(url_for("channel", ch_name=active_ch.title))
    # delete messege and save the db
    db.session.delete(msg)
    db.session.commit()
    # get the messege as a dictionary and update timestamp to str, user id to its name
    msg = msg.as_dict()
    msg["timestamp"] = msg["timestamp"].strftime("%d %b %Y %I:%M%p")
    msg["user_id"] = current_user.username
    msg["chat_count"] = active_ch.chat_count()
    # send this messege to every one to delete
    emit("delete_msg", msg, broadcast=True)
    # work around issue in flasksocketio
    socketio.sleep(0)
