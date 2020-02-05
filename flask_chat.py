''' app runner module '''

from flask_chat import app, socketio

#--------------
# app running |
#--------------
if __name__ == '__main__':
    socketio.run(app, debug=True)
