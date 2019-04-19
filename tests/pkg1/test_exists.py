import pkg1

def test_version():
    assert pkg1.__version__ >= '0.0.1'

def test_hello():
    assert pkg1.hello() >= '0.0.1'
