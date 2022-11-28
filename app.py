import flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
#
# import certifi
# ca = certifi.where()

from pymongo import MongoClient

# client = MongoClient('mongodb+srv://ckdals1994:ckdalsla94@cluster0.xtrzoeq.mongodb.net/Cluster0?retryWrites=true&w=majority',  tlsCAFile=ca)
# db = client.mini_project
client = MongoClient('mongodb+srv://test:sparta@cluster0.ecmqblf.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import datetime

import bson.json_util as json_util
from bson.objectid import ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index_1():
    return render_template('index2.html')


@app.route('/red')
def red():
    return render_template('members/red.html')


@app.route('/blue')
def blue():
    return render_template('members/blue.html')


@app.route('/black')
def black():
    return render_template('members/black.html')


@app.route('/yellow')
def yellow():
    return render_template('members/yellow.html')


@app.route('/pink')
def pink():
    return render_template('members/pink.html')


@app.route('/about_jn')
def about_jn():
    return render_template('members/about_jn.html')


# # POST
# @app.route("/api/comments", methods=["POST"])
# def comment_post():
#     name_receive = request.form['name_give']
#     comment_receive = request.form['comment_give']
#     time_receive = request.form['time_give']
#     doc = {
#         'name': name_receive,
#         'comment': comment_receive,
#         'time': time_receive
#     }
#     # db.guest.insert_one(doc)
#     db.miniProject.insert_one(doc)
#     return jsonify({'msg': '코멘트 등록이 완료되었습니다!'})


# parse ObjectId to JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))


# # GET all
# @app.route("/api/comments", methods=["GET"])
# def comments_get():
#     # comments_list = list(db.miniProject.find({}, {'_id': False}))
#     comments_list = list(db.miniProject.find({}))
#
#     objectId = comments_list[0]['_id']
#     print()
#     # print(objectId.str)
#     # print(objectId.toString())
#     # print(objectId.getTimestamp())
#     # print(objectId.valueOf())
#     # print(datetime.datetime.fromtimestamp(int(str(objectId)[:7], 16)))
#     # print(str(objectId))
#     # print(objectId.generation_time)
#
#     # a = parse_json(comments_list)
#     # print(a[0]['_id'], type(a[0]['_id']), a[0]['_id']['$oid'])
#     return jsonify({'comments_list': parse_json(comments_list)})
#
# # DELETE
# @app.route("/api/comments", methods=["DELETE"])
# def comment_delete():
#     _id = request.form['_id']
#     print(db.miniProject.find_one({'_id': _id}))
#     db.miniProject.delete_one({'_id': _id})
#     return jsonify({'msg': '코맨트를 삭제하였습니다'})




# https://www.youtube.com/watch?v=HyDACIfdPs0
# 강의 듣고 거의 그대로 해본 CRUD 재현:


# POST, using ID
@app.route("/api/comments", methods=["POST"])
def post_comment():
    name = request.form['name_give']
    comment = request.form['comment_give']
    time = request.form['time_give']
    _password = request.form['pwd_give']

    if name and comment and time and request.method == "POST":
        _hashed_password = generate_password_hash(_password)
        doc = {
            'name': name,
            'comment': comment,
            'time': time,
            'pwd': _hashed_password,
        }
        id = db.miniProject.insert_one(doc)

        resp = jsonify("Comment added successfully!")
            # 'msg': 라고 안해줬는데 출력이 잘 될까?
        resp.status_code = 200
        return resp
    else:
        return not_found()


# GET all comments
@app.route("/api/comments", methods=["GET"])
def get_comments():
    comments_list = list(db.miniProject.find())
    resp = json_util.dumps(comments_list)  # json_util.dumps가 아니기 때문에 에러날 것 같다 체크 필요!
    return resp


# GET specific comment
@app.route('/api/comments/<id>', methods=["GET"])
def get_comment(id):
    comment = db.miniProject.find_one({'_id': ObjectId(id)})
    resp = json_util.dumps(comment)
    return resp


# DELETE a comment
@app.route("/api/comments/delete/<id>", methods=["DELETE"])
def delete_comment(id):
    db.miniProject.delete_one({'_id': ObjectId(id)})
    resp = jsonify("The comment was deleted successfully")
    resp.status_code = 200
    return resp


# UPDATE a comment as a whole, which is PUT
@app.route("/api/comments/update/<id>", methods=["PUT"])
def update_comment(id):
    _id = id
    name = request.form['name_give']
    comment = request.form['comment_give']
    # 시간은 어떻게 업데이트되게 하지? 처음 포스팅시간으로 남겨둬야 하나,
    # 수정한 시간으로 바꿔야 하나?
    _password = request.form['pwd_give']

    # (내가 추가) 비번이 안 맞으면 '권한 없음' 메세지 반환
    comment = db.miniProject.find_one({'_id': ObjectId(id)})
    if not check_password_hash(comment['pwd'], _password):
        return unauthorized()

    # 패스워드 통과시 업데이트:
    if name and comment and _id and request.method == "PUT":
        _hashed_password = generate_password_hash(_password)
        search_doc = {
            '_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id),
        }
        data_doc = {
            '$set': {'name': name,
                     'comment': comment,
                     # 'time': time,
                     'pwd': _hashed_password,
                     }
        }
        db.miniProject.update_one(search_doc, data_doc)
        resp = jsonify("Comment updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()
# => 엇, 근데 비밀번호를 확인하는 과정이 없다..!


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': "Not Found" + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(401)
def unauthorized(error=None):
    message = {
        'status': 401,
        'message': "Unauthorized: Password not matched",
    }
    resp = jsonify(message)
    resp.status_code = 401
    return resp


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
