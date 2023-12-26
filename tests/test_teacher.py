# This file contains test cases for Student

# Test cases for POST (endpoint: new_teacher)

# Test case for http response 200
def test_new_teacher(client):
    response = client.post("/teacher", json={"teacher_name": "rita",
                                             "teacher_email": "rita@example.com",
                                             "assign_course": [1]})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Teacher Rita added successfully for courses [1]", "Status": 200}


# Test case for http response 406
def test_new_teacher_special_char(client):
    response = client.post("/teacher", json={"teacher_name": "$#@%^&$",
                                             "teacher_email": "gita@example.com",
                                             "assign_course": [1]})
    assert response.status_code == 406
    assert response.json() == {"Message": "Teacher name field should have characters", "Status": 406}


def test_new_teacher_email_exists(client):
    response = client.post("/teacher", json={"teacher_name": "sita",
                                             "teacher_email": "sita@example.com",
                                             "assign_course": [1]})
    assert response.status_code == 406
    assert response.json() == {"Message": f"Email sita@example.com already exists", "Status": 406}


def test_view_teacher(client):
    response = client.get("/teacher/", params={"teacher_id": 1})
    assert response.status_code == 200


# Test cases for GET (endpoint: view_all_student)
def test_view_all_teachers(client):
    response = client.get("/teachers")
    assert response.status_code == 200
    assert response.json() == [{'teacher_id': 1,
                                'teacher_name': 'Sita',
                                'teacher_email': 'sita@example.com',
                                'assigned_courses': []}]


# Test cases for DELETE (endpoint: complete_delete_student)

# Test case for http response 200
def test_complete_delete_teacher(client):
    response = client.delete("/teacher/", params={"teacher_id": 2})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Teacher id 2 deleted successfully", "Status": 200}


# Test case for http response 404
def test_complete_delete_teacher_not_found(client):
    response = client.delete("/teacher/", params={"teacher_id": 2})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Teacher id 2 does not exist", "Status": 404}


# Test cases for PATCH (endpoint: delete_student)

# Test case for http response 200
def test_delete_teacher(client):
    response = client.patch("/teacher/", params={"teacher_id": 1})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Status of teacher id 1 changed successfully", "Status": 200}


# Test case for http response 404
def test_delete_teacher_not_found(client):
    response = client.patch("/teacher/", params={"teacher_id": 2})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Teacher with id 2 does not exist", "Status": 404}


# Test cases for PUT (endpoint: update_student)
# Test case for http response 200
def test_update_teacher(client):
    response = client.put("/teacher", json={"teacher_id": 1,
                                            "teacher_name": "gita",
                                            "teacher_email": "gitaa@exam-ple.com",})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Record of teacher id 1 updated successfully", "Status": 200}


def test_update_teacher_not_exists(client):
    response = client.put("/teacher", json={"teacher_id": 2,
                                            "teacher_name": "gita",
                                            "teacher_email": "gitaa@exam-ple.com",})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Teacher id 2 does not exist", "Status": 404}
