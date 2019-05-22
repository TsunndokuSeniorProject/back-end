# Back-end
This back-end web server for Tsunndoku project.
It's using python Flask as a server.
# Models
### Aspect Extraction
Word2Vec for classifying sentences into 3 classes( Story, Writing-Style, Character ).
### Sentiment Analysis
Bidirectional GRU for polarity classification.
# Dependencies
All dependencies was listed in >> requirements.txt
# Start Server
Run file app.py
# Api 
### /api/book/isbn/<string:isbn>
### /api/book/isbn/interpret/<string:isbn>
### /api/book/id/interpret/<string:id>
### /api/testML
### /api/book/id/<string:id>
### /api/book/name/<string:name>
### /api/all_books/list
### /api/book/all_books/genre/<string:genre>/<int:start>:<int:end>
### /api/book/all_books
### /api/book/range_books/<int:start>:<int:end>
### /api/all_genre
# Acknowledgement
A big thank to goodreads.com that provide some useful API and allow us to do high frequency web scraping by not ban our IP.
