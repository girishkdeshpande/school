# This file contains test cases for Course

# Test cases for POST (endpoint: add_new_course)

# Test case for http response 200
def test_new_course(client):
    response = client.post("/course", json={"course_name": "javascript"})
    assert response.status_code == 200
    assert response.json() == {"Message": "Course javascript added successfully", "Status": 200}


# Test case for http response 406
def test_new_course_special_char(client):
    response = client.post("/course", json={"course_name": "$#@%^&%"})
    assert response.status_code == 406
    assert response.json() == {"Message": "Course name should be alphanumeric", "Status": 406}


# Test case for http response 409
def test_new_course_existing(client):
    response = client.post("/course", json={"course_name": "Python"})
    assert response.status_code == 409
    assert response.json() == {"Message": "Course Name already exist", "Status": 409}


# Test cases for GET(endpoint: view_course by course_id)

# Test case for http response 200
def test_view_course(client):
    response = client.get("/course/", params={"course_id": 1})
    assert response.status_code == 200
    assert response.json() == {'course_id': 1,
                               'course_name': 'Python',
                               'course_status': True,
                               'students': [],
                               'teachers': [
                                   {'teacher_email': 'sita@example.com',
                                    'teacher_id': 1,
                                    'teacher_name': 'Sita'},
                                    {'teacher_email': 'rita@example.com',
                                     'teacher_id': 2,
                                     'teacher_name': 'Rita'}
                               ]}


# Test case for http response 404
def test_view_course_not_found(client):
    response = client.get("/course/", params={"course_id": 3})
    assert response.status_code == 404
    assert response.json() == {"Message": "Course id 3 does not exist", "Status": 404}


# Test cases for GET(api: view_all_course)
# Test case for http response 200
def test_view_all_course(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == [{'course_id': 1,
                                'course_name': 'Python',
                                'course_status': True,
                                'students': [],
                                'teachers': [
                                    {'teacher_email': 'sita@example.com',
                                     'teacher_id': 1,
                                     'teacher_name': 'Sita'},
                                    {'teacher_email': 'rita@example.com',
                                     'teacher_id': 2,
                                     'teacher_name': 'Rita'}]
                                }]


# Test cases for DELETE(endpoint: delete_course(soft delete))
# Test case for http response 200
def test_delete_course(client):
    response = client.patch("/course/", params={"course_id": 1})
    assert response.status_code == 200
    assert response.json() == {"Message": "Status changed successfully for course Python", "Status": 200}


def test_delete_course_not_found(client):
    response = client.patch("/course/", params={"course_id": 4})
    assert response.status_code == 404
    assert response.json() == {"Message": "Course with id 4 does not exist", "Status": 404}


# Test cases for DELETE(endpoint: delete_course(hard delete))
# Test case for http response 200
def test_complete_delete_course(client):
    response = client.delete("/course/", params={"course_id": 2})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Successfully deleted Course Python", "Status": 200}


# Test case for http response 404
def test_complete_delete_course_not_exists(client):
    response = client.delete("/course/", params={"course_id": 2})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Course id 2 does not exist", "Status": 404}


# Test cases for UPDATE(endpoint: update_course)

# Test case for http response 200
def test_update_course(client):
    response = client.put("/course", json={"course_id": 2, "course_name": "javascript with reactjs"})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Record of course id 2 updated successfully", "Status": 200}


# Test case for http response 409
def test_update_course_exists(client):
    response = client.put("/course", json={"course_id": 1, "course_name": "Fastapi with pydantic"})
    assert response.status_code == 409
    assert response.json() == {"Message": "Course Name already exist", "Status": 409}


# Test case for http response 404
def test_update_course_not_exists(client):
    response = client.put("/course", json={"course_id": 3, "course_name": "pydantic"})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Course id 3 does not exist", "Status": 404}

