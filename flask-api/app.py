from flask import Flask, jsonify, Response
import requests
import hashlib
import redis

app = Flask(__name__)

rds = redis.Redis(host="redis-server")

@app.route('/md5/<string:talk>')
def info(talk):
    result = hashlib.md5(talk.encode())
    final = result.hexdigest()
    return jsonify(
        input=talk,
        output=final)


@app.route('/fibonacci/<int:val>')
def term(val):
    Out = 0
    Sequence = [0, 1]

    if val > 0:
        while Out < val:
            Out = Sequence[-1] + Sequence[-2]
            if (Out < val):
                Sequence.append(Out)
        return f"The result is: {Sequence}."
    elif val <= 0:
        return jsonify(
            input=val,
            output={Sequence})


@app.route('/factorial/<int:x>')
def bit(x):
    output = 1
    fact = x
    if x < 0:
        return ('You must provide a positive number')
    else:
        while x > 0:
            output = output * x
            x = x - 1
            return jsonify(
                input=fact,
                output=output)


@app.route('/is-prime/<int:num>')
def prime_response(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                resp = False
                break
            else:
                resp = True
    else:
        resp = True
    return jsonify(
            input=num,
            output=resp)


@app.route('/slack-alert/<string:talky>')
def trip(talky):
    if __name__ == '__main__':
        wekbook_url = 'https://hooks.slack.com/services/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'
        data = {
            'text': talky,
            'username': 'Script-kitty',
            'icon_emoji': 'smiley_cat'
        }
        response = requests.post(wekbook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        return jsonify(
            input=talky,
            output=response)

@app.route('/key', methods=["POST"])
def add_data():
    post = request.get_json()
    res = list(post.keys())
    n = 0    
    for i in res:
        if res[n] in rds:   
            n += 1            
        else:
            rds.set(res[n], post[res[n]])
            n += 1
    return  ''

@app.route('/key/<n>', methods=["GET"])
def get_val(n):
    if n in rds:        
        return rds.get(n)
    else:
        return ("Key does not exist in the database")        
 
@app.route('/key', methods=["PUT"])
def update_data():
    post = request.get_json()
    res = list(post.keys())
    n = 0    
    for i in res:
        if res[n] in rds:
            rds.set(res[n], post[res[n]])   
            n += 1            
        else:
            continue
    return  ''   

@app.route('/key/<n>', methods=["DELETE"])
def delete_data(n):
    if n in rds:
        rds.delete(n)
        return 'Key deleted'
    else:
        return "Key inputted does not exist"          

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
