def test_user1(test_user2):
    assert test_user2.email=="rohit13138@gmail.com"

def test_user2(test_user1):
    assert test_user1.email=="spal13138@gmail.com"
