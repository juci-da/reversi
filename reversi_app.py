from flask import Flask,redirect,url_for,render_template,request
from flask_socketio import SocketIO
import reversi_utils as utils
import token_checker as tc

board=utils.generate_board()
who=utils.BLACK
app:Flask=Flask(__name__)
socketio=SocketIO(app)
tc.reset_tokens()

print("BLACK URL")
print(f"http://localhost:8888/?who=1&token={tc.get_token(1)}")

print("WHITE URL")
print(f"http://localhost:8888/?who=2&token={tc.get_token(2)}")

@app.route("/")
def index():
    me=int(request.args.get("who",who))
    token=request.args.get("token","")
    if me not in(utils.BLACK,utils.WHITE):
        return "プレイヤーの指定が正しくありません"
    if token=="":
        return redirect(url_for("index",who=me,token=tc.get_token(me)))
    if not tc.check_token(me,token):
        return "不正なアクセスです"
    black,white=utils.count_stone_both(board)
    msg=utils.STATUS[who]+"の手番"
    if black+white==64:
        if black>white:
            msg="黒の勝ち"
        elif white>black:
            msg="白の勝ち"
        else:
            msg="引き分け"
    can_place =who==me
    return render_template(
        "index.html",
        board=utils.add_flip_mark(board,who) if can_place else board,
        count=(black,white),token=token,
        msg=msg,me=me,can_place=can_place,
        black_token=tc.get_token(1),
        white_token=tc.get_token(2)
    )

@app.route("/place/<int:y>/<int:x>")
def place(y:int,x:int):
    global who
    me=int(request.args.get("who",who))
    token=request.args.get("token","")
    if me not in (utils.BLACK,utils.WHITE):
        return "不正なアクセスです"
    if who !=me:
        return redirect(url_for("index",who=me,token=token))
    if utils.can_flip(board,x,y,who):
        utils.flip(board,x,y,who)
        who=utils.toggle(who)
        socketio.emit("board_update")
    return redirect(url_for("index",who=me,token=token))

@app.route("/reset")
def reset():
    global board,who
    me=int(request.args.get("who",utils.BLACK))
    token=request.args.get("token","")
    if not tc.check_token(me,token):
        return "不正なアクセスです"
    board=utils.generate_board()
    who=utils.BLACK
    socketio.emit("board_update")
    return redirect(url_for("index",who=me,token=token))

@app.route("/skip")
def skip():
    global who
    me=int(request.args.get("who",who))
    token=request.args.get("token","")
    if me not in(utils.BLACK,utils.WHITE):
        return "プレイヤーーの指定が正しくありません"
    if who !=me:
        return redirect(url_for("index",who=me,token=token))
    if not tc.check_token(me,token):
        return "不正なアクセスです"
    who=utils.toggle(who)
    socketio.emit("board_update")
    return redirect(url_for("index",who=me,token=token))

if __name__=="__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=8888,
        debug=True
    )