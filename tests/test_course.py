# This file contains test cases for Course

# Test cases for POST (endpoint: add_new_course)

# Test case for http response 200
def test_new_course(client):
    response = client.post("/course", json={"course_name": "python"})
    assert response.status_code == 200
    assert response.json() == {"Message": "Course python added successfully", "Status": 200}


# Test case for http response 406
def test_new_course_special_char(client):
    data = {"course_name": "$#@%^&%"}
    response = client.post("/course", json=data)
    assert response.status_code == 406
    response_data = response.json()
    assert response_data == {"Message": "Course name should be alphanumeric", "Status": 406}


# Test case for http response 409
def test_new_course_existing(client):
    data = {"course_name": "Python"}
    response = client.post("/course", json=data)
    assert response.status_code == 409
    response_data = response.json()
    assert response_data == {"Message": "Course Name already exist", "Status": 409}


# Test cases for GET(endpoint: view_course by course_id)

# Test case for http response 200
def test_view_course(client):
    response = client.get("/course/", params={"course_id": 2})
    assert response.status_code == 200
    assert response.json() == {
                                "course_id": 2,
                                "course_name": "Python",
                                "course_status": True,
                                "students": [],
                                "teachers": []
                            }


# Test case for http response 404
def test_view_course_not_found(client):
    response = client.get("/course/", params={"course_id": 3})
    assert response.status_code == 404
    assert response.json() == {"Message": "Course id does not exist", "Status": 404}


# Test cases for GET(api: view_all_course)
# Test case for http response 200
def test_view_all_course(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == [{'course_id': 1,
                                'course_name': 'Fastapi',
                                'course_status': True,
                                'students': [],
                                'teachers': []},
                               {'course_id': 2,
                                'course_name': 'Python',
                                'course_status': False,
                                'students': [],
                                'teachers': []}]


# Test cases for DELETE(endpoint: delete_course(soft delete))
# Test case for http response 200
def test_delete_course(client):
    response = client.patch("/course/", params={"course_id": 2})
    assert response.status_code == 200
    assert response.json() == {"Message": "Status changed successfully for course Python", "Status": 200}


def test_delete_course_not_found(client):
    response = client.patch("/course/", params={"course_id": "abd"})
    assert response.status_code == 404
    assert response.json() == {"Message": "Course with id 2 does not exist", "Status": 404}


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
    response = client.put("/course", json={"course_id": 1, "course_name": "Fastapi with pydantic"})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Record of course id fastapi with pydantic updated successfully", "Status": 200}


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

