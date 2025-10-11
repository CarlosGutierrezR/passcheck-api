from app.hibp import pwned_count

def test_known_weak_password():
    assert pwned_count("password") > 0
