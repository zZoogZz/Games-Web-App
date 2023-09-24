'''
with client:
    # set a user id without going through the login route
    response = client.get("/")
    assert response.status_code == 200'''