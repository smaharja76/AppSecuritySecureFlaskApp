import requests
from bs4 import BeautifulSoup
import unittest

url = 'http://127.0.0.1:5000/'

def getElemById(text, id):
    result = BeautifulSoup(text, "html.parser").find(id=id)
    return result

class MyAppTest(unittest.TestCase):

    def testRegisterPage(self):
        resp = requests.get(url + 'login')
        assert resp.status_code == 200
        
    def testLoginPage(self):
        resp = requests.get(url + 'register')
        assert resp.status_code == 200

    def testSpellCheckPage(self):
        resp = requests.get(url + 'spell_check')
        assert resp.status_code == 200

    def testRegister(self):
        creds = {"username":"JaneDoe", "password":"password", "twofactor":"4021111111" }
        resp = requests.Session().post(url+'register', data=creds)
        assert resp.status_code == 200

        result = getElemById(resp.text, "success")
        #print(result)
        assert "success" in result.text

    def testRegisterDupUser(self):
        creds = {"username":"JaneDoe", "password":"password", "twofactor":"4021111111" }
        resp = requests.Session().post(url+'register', data=creds)
        assert resp.status_code == 200

        result = getElemById(resp.text, "success")
        #print(result)

        assert "failure" in result.text

    def testLogin(self):
        creds = {"username": "JaneDoe", "password": "password", "twofactor": "4021111111"}
        resp = requests.Session().post(url + 'login', data=creds)
        assert resp.status_code == 200

        result = getElemById(resp.text, "result")
        #print(result)

        assert "success" in result.text

    def badLogin(self):
        creds = {"username": "JaneXDoe", "password": "password", "twofactor": "4021111111"}
        resp = requests.Session().post(url + 'login', data=creds)
        assert resp.status_code == 200

        result = getElemById(resp.text, "result")
        #print(result)

        assert "Incorrect" in result.text


    def testSpellCheck(self):
        words = {"words": "Testword"}
        resp = requests.Session().post(url + 'spell_check', data=words)
        assert resp.status_code == 200
