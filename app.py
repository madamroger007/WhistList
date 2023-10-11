from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://adam:adamsjr123@ac-fgud05a-shard-00-00.posdf04.mongodb.net:27017,ac-fgud05a-shard-00-01.posdf04.mongodb.net:27017,ac-fgud05a-shard-00-02.posdf04.mongodb.net:27017/?ssl=true&replicaSet=atlas-h6drk3-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num' : num,
        'bucket': bucket_receive,
        'done': 0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data Saved'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['done_bucket']
    db.bucket.update_one({'num' : int(num_receive)},{ '$set' : {'done': 1}})
    return jsonify({'msg': 'Update done'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id' : False}))
    return jsonify({'buckets': bucket_list})

@app.route('/delete',  methods=["POST"])
def bucket_del():
    num_receive = request.form['del_bucket']
    # Periksa apakah bucket dengan nomor tersebut ada
    bucket = db.bucket.find_one({"num": int(num_receive)})
    if bucket is None:
        return jsonify({"msg": "Bucket not found"})
    
    db.bucket.delete_one({'num' :int(num_receive)})
    return jsonify({'msg': 'Delete done'})
   


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)