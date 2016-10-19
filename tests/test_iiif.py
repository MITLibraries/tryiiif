from hashlib import sha1
from urllib import parse

from tryiiif.extensions import rc


def testGetRootReturns200(testapp):
    r = testapp.get('/')
    assert r.status_code == 200


def testPostWithoutURLReturns200(testapp):
    r = testapp.post('/')
    assert r.status_code == 200


def testPostWithoutURLIncludesWarning(testapp):
    r = testapp.post('/')
    assert 'A URL to an image is required.' in r


def testPostToNonexistentUrlIncludesWarning(testapp, iiif_server):
    url = 'http://{}:{}/404'.format(*iiif_server)
    r = testapp.post('/', {'url': url, 'submit': 'uv'})
    assert "It looks like there&#39;s nothing there." in r


def testPostWithValidFieldsToUVRedirectsToUV(testapp):
    url = 'https://dome.mit.edu/bitstream/handle/1721.3/176472/249875_cp.jpg'
    res = testapp.post('/', dict(title='whatevs', url=url, submit='uv'))
    assert res.status_code == 302
    assert '/viewer/uv/' in res.headers['Location']


def testPostWithValidFieldsToMiradorRedirectsToMirador(testapp):
    url = 'https://dome.mit.edu/bitstream/handle/1721.3/176472/249875_cp.jpg'
    res = testapp.post('/', dict(title='whatevs', url=url, submit='mirador'))
    assert res.status_code == 302
    assert '/viewer/mirador/' in res.headers['Location']


def testPostWithValidFieldsToInvalidViewerReturns404(testapp):
    url = 'https://dome.mit.edu/bitstream/handle/1721.3/176472/249875_cp.jpg'
    res = testapp.post('/', dict(title='whatevs', url=url, submit='x'),
                       expect_errors=True)
    assert res.status_code == 404


def testPostWithLeadingTrailingSpaces(testapp):
    url = ' https://dome.mit.edu/bitstream/handle/1721.3/176472/249875_cp.jpg '
    clean_url = url.strip()
    m_url = sha1()
    m_url.update(url.encode('utf-8'))
    m_clean = sha1()
    m_clean.update(clean_url.encode('utf-8'))
    res = testapp.post('/', dict(title='whatevs', url=url, submit='uv'))
    assert m_url.hexdigest() not in parse.unquote(res.headers['Location'])
    assert m_clean.hexdigest() in parse.unquote(res.headers['Location'])


def testGetUrlByHashReturnsUrl(testapp):
    h = sha1()
    h.update(u'mock://example.com'.encode('utf-8'))
    digest = h.hexdigest()
    rc.conn.set(digest, u'mock://example.com')
    r = testapp.get('/url/{}'.format(digest))
    assert r.text == 'mock://example.com'
