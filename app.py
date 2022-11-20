from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
import certifi
ca = certifi.where()

from pymongo import MongoClient
# client = MongoClient('mongodb+srv://ckdals1994:ckdalsla94@cluster0.xtrzoeq.mongodb.net/Cluster0?retryWrites=true&w=majority',  tlsCAFile=ca)
# db = client.mini_project
client = MongoClient('mongodb+srv://test:sparta@cluster0.ecmqblf.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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

# POST
@app.route("/api/comments", methods=["POST"])
def homework_post():
  name_receive = request.form['name_give']
  comment_receive = request.form['comment_give']
  time_receive = request.form['time_give']
  doc = {
    'name': name_receive,
    'comment': comment_receive,
    'time': time_receive
  }
  # db.guest.insert_one(doc)
  db.miniProject.insert_one(doc)
  return jsonify({'msg':'코멘트 등록이 완료되었습니다!'})

# GET
@app.route("/api/comments", methods=["GET"])
def homework_get():
  comments_list = list(db.guest.find({},{'_id':False}))
  return jsonify({'comments_list': comments_list})



if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)