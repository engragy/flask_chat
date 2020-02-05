# Flask_chat
[![LOGO|Flask](https://hackr.io/tutorials/learn-flask/logo/logo-flask?ver=1527561020)](https://hackr.io/tutorials/learn-flask/logo/logo-flask?ver=1527561020)
*** Powered By ***
##### this is my frist attempt in the world of web-dev, it is a Flask WebApp for chatting.
#
### consists of a couple of pages!
> main page
> ![main_page](https://cdn-images-1.medium.com/max/1200/1*fD3qqMWNyfJ85XST9c1H2g.png)
> login/register pages
> ![register_page](https://coderseye.com/wp-content/uploads/Flask-vs-Django-best-python-web-framework.jpg)
> chat channel page
> ![chat_channel_page](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flask_logo.svg/1920px-Flask_logo.svg.png)

### Features:
* Nice looking Custom CSS style (no styling framework is used)
* Users can upload and use a profile image 
* add as much channels/users, there is no email validity as this is for development 
* using sqlite3 DataBase for development
* using JS to set window position when there is a new messege
* delete messeges from both chatting users
* custom error pages

### Used Flask extensions/packages/libraries including:
* [Flask] - the web framework
* [Flask-SocketIO] -- for websockets use (realtime chat)
* [Flask-Login] -- for managing users login / logout
* [Flask-SQLAlchemy] -- for database management
* [Flask-WTF] -- for creating and securing forms
* [Flask-Bcrypt] -- powerfull hashing algorithms
* [Pillow] -- for dealing with images

### Installation
```sh
just use a virtual environment for the app
$ pip3 install virtualenv
make a new folder for the app
$ mkdir ~/flask_chat_dir
$ cd flask_chat_dir
$ virtualenv flask_chat_env
$ git clone
$ source flask_chat_env/bin/activate 
$ pip -r install requirements
$ python flask_chat.py
```

[Flask]: <https://flask.palletsprojects.com/en/1.1.x/>
[Flask-SocketIO]: <https://flask-socketio.readthedocs.io/>
[Flask-Login]: <https://flask-login.readthedocs.io/en/latest/>
[Flask-SQLAlchemy]: <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>
[Flask-WTF]: <https://flask-wtf.readthedocs.io/>
[Flask-Bcrypt]: <https://flask-bcrypt.readthedocs.io/en/latest/>
[Pillow]: <https://pillow.readthedocs.io/en/stable/>
