from os import path

def test_gmail():
    assert path.exists('credentials.json') == True
    assert path.exists('token.pickle') == True