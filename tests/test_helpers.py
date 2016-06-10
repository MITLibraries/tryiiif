from tryiiif.helpers import b64safe


def test_b64safe_with_string():
    assert(b64safe('https://mit.edu/bitstream/1721.3/249875_cp.jpg') ==
           'aHR0cHM6Ly9taXQuZWR1L2JpdHN0cmVhbS8xNzIxLjMvMjQ5ODc1X2NwLmpwZw==')
