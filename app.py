import json
from flask import Flask, request, jsonify

def create_app(debug=True):
    app = Flask(__name__)
    app.debug = debug
    return app

app = create_app()

def read_club_json(filepath='./club.json'):
    with open(filepath, 'r') as f:
        club = json.loads(f.read())

    return club

def write_club_json(club, filepath='./club.json'):
    with open(filepath, 'w') as f:
        f.write(json.dumps(club))

    return True

def call_the_cops(filepath='./club.json'):
    '''EVERYONE OUT OF THE CLUB
    '''
    write_club_json([])
    return True

@app.route('/')
def index():
    pass

@app.route('/club', methods=['GET', 'POST'])
def club():
    '''Get current club members/add new club member

    Well-formed club POST includes:
        + username (slack username)
        + nickname (user-specified name)
        + time_added (from slack)
    '''
    club_json = read_club_json()
    if request.method == 'POST':
        request_json = json.loads(request.form['payload'])
        club_json.append({
            'username': request_json.get('username'),
            'nickname': request_json.get('nickname', ''),
            'time_added': request_json.get('time_added', '')
        })
        write_club_json(club_json)
    return jsonify({'club': club_json})

@app.route('/cops', methods=['POST'])
def cops():
    '''CLEAR THE CLUB
    '''
    call_the_cops()
    return jsonify({'club': []})

if __name__ == '__main__':
    app.run(port=9000)
