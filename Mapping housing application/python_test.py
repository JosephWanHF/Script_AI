import requests

API_KEY = 'AIzaSyCAQWvCRWyXj8jmGk3c5aoZ8pKQUkXDvGQ'
location = '52.0907,5.1214'  # Utrecht center
radius = 500
type_ = 'restaurant'

url = (
    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    f"?location={location}&radius={radius}&type={type_}&key={API_KEY}"
)

response = requests.get(url)
data = response.json()

print("Status:", data.get('status'))
print("Results found:", len(data.get('results', [])))
if 'error_message' in data:
    print("Error message:", data['error_message'])
