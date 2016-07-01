from flask.ext.testing import TestCase
from app import create_app
from app.models import Result, db
from app.controllers import main

__author__ = 'bernardovale'


class ControllerTestCase(TestCase):


    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def create_app(self):

        # pass in test configuration
        return create_app(self)


    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_post_result(self):
        msg = "Database Size:"
        identifier = "size_db"
        output = "20.34"


        _, got = main.post_result(identifier, output, msg)

        self.assertEqual(got, 200)