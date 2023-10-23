Location -based recommendation based on single user preference

User Data: userid, username, password, email
Locations: locationId, name, description, imageUrl, city, province, openTime, closeTime, latitude, longitude,
accessibility, historical_context, hands_on_activities
interaction: userId, locationId, action, timestamp

food_id,orderedBy(user_id),food_name,description,feedback,cuisine,age

TODO : Create pre_processed.csv with all the data for recommendation system

Authentication: true
Username: nilupa
Password: nilupa123
Latitude: 6.828828828828828
Longitude: 79.86386702251839
Nearest Landmark: Okada Temple
Distance Radius Value: 303.5087719298246
Updated Data:
Time Restrictions: 7.00AM - 7.00PM
Accessibility: Choose an option
Historical Contexts: Rock Information
Hands-On Activities: Choose an option

Initially Data  
user_id ->
imageDataList: [ImageData(imageUrl: 'https://picsum.photos/${imageResolution}/${imageResolution}?random=8', name: 'Photographer 8', dateTime: 'Daytime photography', description: 'Description for photo 8',), ImageData(imageUrl: 'https://picsum.photos/${imageResolution}/${imageResolution}?random=9', name: 'Photographer 9', dateTime: 'Daytime photography', description: 'Description for photo 9')]

Card ekk click kalama
user_id, filters, current location, location id -> Shortest path eka (lat, long)

user_id, latitude, longitude, radius, time restrictions, accessibility, historical contexts, hands-on activities,
location id ->
->
["latitude": 6.828828828828828, "longitude" : 79.86386702251839, "name" : "Okada Temple"]

login eka
username, password -> verify -> authenticate : true, false

sign up ela
username, password, email -> create new user -> user_id

TODO:

In recommadation -> Add unexpected once (Find a list of least visited places and recommend them)
Chatbot -> Train Chatbot with corpus



