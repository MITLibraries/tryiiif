from urllib import parse

from tryiiif.helpers import b64safe


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


def testPostWithValidFieldsToUVRedirectsToMirador(testapp):
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
    res = testapp.post('/', dict(title='whatevs', url=url, submit='uv'))
    assert b64safe(url) not in parse.unquote(res.headers['Location'])
    assert b64safe(clean_url) in parse.unquote(res.headers['Location'])
