# This file contains test cases for Student

# Test cases for POST (endpoint: new_student)

# Test case for http response 200
def test_new_student(client):
    response = client.post("/student", json={"student_name": "girish",
                                             "student_email": "girish1@example.com",
                                             "year_enrolled": "2023-12-16",
                                             "course_enrolled": [2]})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Student girish added successfully with courses [2]", "Status": 200}


# Test case for http response 406
def test_new_student_special_char(client):
    response = client.post("/student", json={"student_name": "$#@%^&$",
                                             "student_email": "gita@example.com",
                                             "year_enrolled": "2023-12-16",
                                             "course_enrolled": [1]})
    assert response.status_code == 406
    assert response.json() == {"Message": "Student name field should have characters", "Status": 406}


def test_new_student_email_exists(client):
    response = client.post("/student", json={"student_name": "gita",
                                             "student_email": "gita@example.com",
                                             "year_enrolled": "2023-12-16",
                                             "course_enrolled": [1]})
    assert response.status_code == 406
    assert response.json() == {"Message": f"Email address gita@example.com already exists", "Status": 406}


def test_view_student(client):
    response = client.get("/student/", params={"student_id": 1})
    assert response.status_code == 200


# Test cases for GET (endpoint: view_all_student)
def test_view_all_students(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json() == [{'student_id': 1,
                                'student_name': 'Gagan@Example.Com',
                                'student_email': 'gagan@example.com',
                                'year_enrolled': '2023-12-16',
                                'courses': []},
                               {'student_id': 2,
                                'student_name': 'Girish@Example.Com',
                                'student_email': 'girish@example.com',
                                'year_enrolled': '2023-12-16',
                                'courses': []}]


# Test cases for DELETE (endpoint: complete_delete_student)

# Test case for http response 200
def test_complete_delete_student(client):
    response = client.delete("/student/", params={"student_id": 1})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Student id 1 deleted successfully", "Status": 200}


# Test case for http response 404
def test_complete_delete_student_not_found(client):
    response = client.delete("/student/", params={"student_id": 4})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Student id {4} does not exist", "Status": 404}


# Test cases for PATCH (endpoint: delete_student)

# Test case for http response 200
def test_delete_student(client):
    response = client.patch("/student/", params={"student_id": 1})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Status of student id {1} changed successfully", "Status": 200}


# Test case for http response 404
def test_delete_student_not_found(client):
    response = client.patch("/student/", params={"student_id": 2})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Student id {2} does not exist", "Status": 404}


# Test cases for PUT (endpoint: update_student)
# Test case for http response 200
def test_update_student(client):
    response = client.put("/student", json={"student_id": 1,
                                            "student_name": "gita",
                                            "student_email": "gitaa@exam-ple.com",
                                            "year_enrolled": "2023-09-09"})
    assert response.status_code == 200
    assert response.json() == {"Message": f"Record of student id {1} updated successfully", "Status": 200}


def test_update_student_not_exists(client):
    response = client.put("/student", json={"student_id": 2,
                                            "student_name": "gita",
                                            "student_email": "gitaa@exam-ple.com",
                                            "year_enrolled": "2023-09-09"})
    assert response.status_code == 404
    assert response.json() == {"Message": f"Student with id {2} does not exist", "Status": 404}
