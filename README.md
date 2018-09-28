# Back-end
This back-end web server for Tsunndoku project.
It's using python Flask as a server.
# Dependencies
To install, this should be done by using command pip install < module >
* Python < 2.7.* >
* Flask
* NumPy
* SciPy
* Pandas
* scikit-learn
# Start Server
* $ cd <inside the directory>
* $ python server.py
# Api 
### /api/1.0/test
This endpoint is using just for test. It provide a simple example of RestAPI concept.
Inside the code there is a temporary database which allow to [POST] or [GET] by sending a request.
### /api/1.0/predict
This end point is allow to post { height, weight }, the server will predict a gender of the given information.
# Upcoming
#### ...