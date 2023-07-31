
data = {
  "email": "asa@gmail.com",
  "first_name": "Eyal",
  "last_name": "Tz",
  "phone_number": "0551112231",
  "location": {"x": 9, "y": 10},
  "gender": "male",
  "relationship_status": "single",
  "interested_in": "female",
  "hobbies": ["filming", "programming"]

}


def create_user(client):
    response = client.post("http://localhost:8000/api/user/register", json=data)
    return response.json()


def delete_user(client, user_id):
    response = client.delete(f"http://localhost:8000/api/user/user?user={user_id}")
    return response.json()
