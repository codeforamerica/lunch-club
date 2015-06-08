from app import create_app, read_club_json, write_club_json
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True).test_client()

    def tearDown(self):
        write_club_json([])

    def test_index(self):
        index = self.app.get('/')
        self.assertEquals(index.status_code, 200)

    def test_add_club(self):
        add = self.app.post('/club', data={
            'user_name': 'test',
        })
        self.assertEquals(add.status_code, 200)
        self.assertEquals(add.data, 'Welcome to lunch club!')
        club_json = read_club_json()
        self.assertEquals(len(club_json), 1)
        # assert you can only be there once
        add = self.app.post('/club', data={
            'user_name': 'test',
        })
        club_json = read_club_json()
        self.assertEquals(len(club_json), 1)

    def test_clear(self):
        clear = self.app.post('/club', data={
            'text': 'clear'
        })
        club_json = read_club_json()
        self.assertEquals(clear.status_code, 200)
        self.assertEquals(clear.data, 'Cleared the club!')
        self.assertEquals(len(club_json), 0)

if __name__ == '__main__':
    unittest.main()
