import datetime
import json
from flask import Flask, request, jsonify, Blueprint, url_for, redirect

bp = Blueprint('club', __name__)

def create_app(debug=True, testing=False):
    app = Flask(__name__)
    app.debug = debug
    app.testing = testing
    app.register_blueprint(bp)
    return app

def read_club_json(filepath='./club.json'):
    try:
        with open(filepath, 'r') as f:
            club = f.read()
    except IOError:
        # there is no club, so make one
        write_club_json([])
        return []

    try:
        return json.loads(club)
    except ValueError:
        return []

def write_club_json(club, filepath='./club.json'):
    try:
        data = json.dumps(club)
    except ValueError:
        data = '[]'

    with open(filepath, 'w') as f:
        f.write(data)

    return True

def call_the_cops(filepath='./club.json'):
    '''EVERYONE OUT OF THE CLUB
    '''
    write_club_json([])
    return True

@bp.route('/')
def index():
    club_json = read_club_json()

    if len(club_json) == 0:
        return '<marquee>Welcome to lunch club! Sign up in Slack with <code>/lunch</code>!</marquee>'

    return '<marquee>Welcome to lunch club! Today\'s club members: {}</marquee>'.format(
        ', '.join([i['username'] for i in club_json])
    )

@bp.route('/club', methods=['GET', 'POST'])
def club():
    '''Get current club members/add new club member

    Well-formed club POST includes:
        + username (slack username)
        + nickname (user-specified name)
        + time_added (from slack)
    '''
    club_json = read_club_json()
    if request.method == 'POST':
        if request.form.get('text') == 'clear':
            call_the_cops()
            return 'Cleared the club!'

        else:
            if request.form['user_name'] in [i.get('username') for i in club_json]:
                return 'You\'re already in the club!'
            club_json.append({
                'username': request.form['user_name'],
                'nickname': request.form.get('nickname', ''),
                'time_added': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'channel': request.form.get('channel_name', ''),
                'channel_id': request.form.get('channel_id', '')
            })
            write_club_json(club_json)
        return 'Welcome to lunch club!', 200

    return redirect(url_for('club'))

@bp.route('/cops', methods=['POST'])
def cops():
    '''CLEAR THE CLUB
    '''
    call_the_cops()
    return jsonify({'club': []})

if __name__ == '__main__':
    app = create_app()
    app.run()
