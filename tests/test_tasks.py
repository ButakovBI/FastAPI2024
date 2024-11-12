from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app


client = TestClient(app)


# def test_get_dashboard_report(create_user_fixture):

#     with patch("tasks.router.current_user") as mock_current_user:
#         mock_current_user.return_value = type(
#             "User", (object,), {
#                 "username": create_user_fixture.username})

#         response = client.post(
#             "/auth/jwt/login",
#             data={
#                 "username": str(create_user_fixture.username),
#                 "password": str(create_user_fixture.password)},
#             headers={
#                 "Content-Type": "application/x-www-form-urlencoded"})

#         assert response.status_code == 204

#         response = client.get("/report/dashboard")

#         assert response.status_code == 401
#         assert response.json() == {'detail': 'Unauthorized'}
