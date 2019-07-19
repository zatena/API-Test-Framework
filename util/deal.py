import core.myrequest as request
import json


def login(user, pwd):
    data = {"email": user, "password": pwd}
