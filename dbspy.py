from db.database_connection import session
from db.database import User, Category, Item
"""
This script is intended for your to get a peek of the information that is
in the database at any given time you can add property names to the print
statements if you would like to display more properties
"""
categories = session.query(Category).all()
print 'Categories\n\n'
for c in categories:
    print c.name

print '\n\nUsers\n\n'
users = session.query(User).all()

for u in users:
    print u.username + " id: " + str(u.id)

print '\n\nItems\n\n'

items = session.query(Item).all()
for i in items:
    print i.name
