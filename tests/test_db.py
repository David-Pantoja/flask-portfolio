import unittest
from urllib import response
from peewee import *
import sys
sys.path.insert(0,'app/')
from __init__ import TimelinePost, get_time_line_post

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_time_line_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello World! I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello World! I\'m Jane!')
        assert second_post.id == 2
        responses = get_time_line_post()['timeline_posts']
        assert responses[0]['id'] == 2
        assert responses[0]['name'] == 'Jane Doe'
        assert responses[0]['email'] == 'jane@example.com'
        assert responses[0]['content'] == 'Hello World! I\'m Jane!'
        assert responses[1]['id'] == 1
        assert responses[1]['name'] == 'John Doe'
        assert responses[1]['email'] == 'john@example.com'
        assert responses[1]['content'] == 'Hello World! I\'m John!'


if __name__ == '__main__':
    unittest.main()