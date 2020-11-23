from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient
from flask import render_template
from flask import send_from_directory
from flask import json
import os

app = Flask(__name__)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsof.icon')


if "&w=majority" not in os.environ["MONGO_URI"]:
    os.environ["MONGO_URI"] += "&w=majority"

mongo_client = MongoClient(os.environ["MONGO_URI"])
db = mongo_client.db

master = db.master
india = db.india
arr = []
for r in india.find({}, {'_id': 1, 'Brand': 1, 'Notes': 1}):
    arr.append(r['Brand'])
    if r['Notes'] != '' and r['Notes'] != None:
        notes = r['Notes'].split(',')
        for note in notes:
            if note != '' and note not in arr:
                arr.append(note)
for r in master.find({}, {'_id': 1, 'Brand': 1}):
    arr.append(r['Brand'])


# arr=set(arr)
# arr=list(arr)
# print(arr)
@app.route('/response', methods=['GET'])
def get_all_stars():
    master = db.master
    india = db.india
    searched = db.search
    notes = ''
    Category = ''
    print(request)
    input = request.args.get('q')
    searched.insert_one({'input': input})
    # Brand,Category,Notes,Country,Wiki
    results = india.find({"Brand": {'$regex': "^" + input + "$", '$options': 'i'}})
    if results.count() == 1:
        res = []
        for result in results:
            # print(res["Brand"])
            res = result
        print(3)
        return render_template('results.html', results=res, type=3, input=input, arr=arr)

    results = master.find({"Brand": {'$regex': "^" + input + "$", '$options': 'i'}},
                          {'_id': 1, 'Category': 1, 'Notes': 1})
    if results.count() == 1:
        notes = ''
        Category = ''
        for res in results:
            notes = res.get('Notes')
        notes = notes.split(',')
        print(notes)
        jsn = {}
        nots = set()
        for note in notes:
            pk = set()
            result = []
            print(note)
            if (note.endswith('s')):
                note = note[:-1]
            results = india.find({"Notes": {'$regex': ".*" + note + ".*", '$options': 'i'}})
            for res in results:
                if res["Brand"] in pk:
                    continue
                # print(res["Brand"])
                pk.add(res["Brand"])
                result.append(res)
            cnt = len(result)
            if cnt:
                jsn[note] = {'res': {}, 'count': 0}
                jsn[note]['res'] = result
                jsn[note]['count'] = len(result)
                nots.add(note)
        print(jsn)
        nots = list(nots)
        if jsn == {}:
            return render_template('results.html', results=0, type=1, input=input, arr=arr)
        print(nots)
        return render_template('results.html', results=jsn, type=2, input=input, arr=arr, notes=nots)
    newinput = input
    if (input.endswith('s')):
        newinput = input[:-1]
    results = india.find({'$or': [{"Notes": {'$regex': ".*" + newinput + ".*", '$options': 'i'}}]})
    if results.count() == 0:
        none = db.none
        none.insert_one({'input': input})
        print(1, results)
        return render_template('results.html', results=0, type=1, input=input, arr=arr)
    result = []
    pk = set()
    for res in results:
        if res["Brand"] in pk:
            continue
        pk.add(res["Brand"])
        # print(res["Brand"])
        result.append(res)
    print(2)
    return render_template('results.html', results=result, type=4, count=len(result), input=input, arr=arr)


@app.route('/', methods=['GET'])
def home():
    # print(arr)
    return render_template('index.html', arr=arr)


@app.route('/query', methods=['POST'])
def query():
    queries = db.queries
    message = request.form.get('message')
    queries.insert_one({'problem': message})
    return render_template('index.html', arr=arr)


@app.route('/test')
def test():
    if "MONGO_URI" in os.environ:
        return "Works!"
    else:
        return "Error"


if __name__ == "__main__":
    app.run(use_reloader=True, debug=False)