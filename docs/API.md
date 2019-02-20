# URL Shortener API

In addition to the website, you can use these APIs to create, delete and get URLs.

Types
```
URL {
  id {string} Unique ID of the URL
  clicks {number} The amount of visits to this URL
  created_on {string} ISO timestamp of when the URL was created
  target {string} Where the URL will redirect to
  short_url {string} The shortened link (Usually https://cour.fun/id)
}
```
In order to use these APIs you need to generate an API key from settings. Never put this key in the client side of your app or anywhere that is exposed to others.

All API requests and responses are in JSON format.

Include the API key as ```X-API-Key``` in the header of all below requests. Available API endpoints with body parameters:

Get shortened URLs list:
```
GET /api/url/list
```
Returns:
```
Array<URL>
```
Create a shortened link:
```
POST /api/url/create
```
Body:
```
target: Original long URL to be shortened.
```
Returns:
```
URL object
```
Delete a shortened URL and Get stats for a shortened URL:
```
POST /api/url/delete/id
```
Returns:
```json
{}
```
