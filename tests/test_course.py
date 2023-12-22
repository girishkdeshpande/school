
# Test data for add_new_course
data1 = {"course_name": "FastAPI"}
data2 = {"course_name": "$#@%^&%"}
data3 = {"course_name": "python"}


def test_new_course(client):
    response = client.post("/course", json=data1)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"Message": "Course FastAPI added successfully", "Status": 200}


def test_new_course_special_char(client):
    response = client.post("/course", json=data2)
    assert response.status_code == 406
    response_data = response.json()
    assert response_data == {"Message": "Course name should be alphanumeric", "Status": 406}


def test_new_course_existing(client):
    response = client.post("/course", json=data3)
    assert response.status_code == 409
    response_data = response.json()
    assert response_data == {"Message": "Course Name already exist", "Status": 409}
