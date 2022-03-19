def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Last 10 visits' in res.data