import requests

# The URL of your local server's demo route
url = "http://127.0.0.1:5000/api/contact"

# The fake data we are sending to simulate a user filling out the form
test_data = {
    "name": "Test Student",
    "phone": "+91 98765 43210",
    "course": "JEE Mains + Advanced"
}

print("Sending test request to server...")

# Send the POST request
response = requests.post(url, json=test_data)

# Print the server's response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")