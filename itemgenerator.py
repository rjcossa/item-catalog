from db.database_connection import session
from db.database import User, Category, Item
"""
This script is meant to populate the database with sample data in order to get
a better experience while running the code and not have to start everything
from scratch
"""

# ------------------------
# POPULATE CATEGORIES
# ------------------------

cat = Category(name="Snow Bikes",
               user_id=1)
session.add(cat)
session.commit()
cat = Category(name="Football",
               user_id=1)
session.add(cat)
session.commit()

cat = Category(name="Break Dance",
               user_id=3)
session.add(cat)
session.commit()

cat = Category(name="Sports",
               user_id=4)
session.add(cat)
session.commit()

cat = Category(name="Finance",
               user_id=1)
session.add(cat)
session.commit()

# ------------------------
# POPULATE ITEMS
# ------------------------

item = Item(
            name="YFZ Killaton",
            category_id=1,
            description="Crazy Snow Bike with 200hp",
            picture=("https://pixabay.com/get/"
                     "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                     "4b0144095f9c571a2eab7_640.png"),
            user_id=1)
session.add(item)
session.commit()

item = Item(
            name="Yamaha Breakpads",
            category_id=1,
            description="Crazy Ice breaking ting that goes skraaah",
            ppicture=("https://pixabay.com/get/"
                      "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                      "4b0144095f9c571a2eab7_640.png"),
            user_id=4)
session.add(item)
session.commit()

item = Item(
            name="Front Flip",
            category_id=3,
            description="Magestic flip to the front with no fear",
            picture=("https://pixabay.com/get/"
                     "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                     "4b0144095f9c571a2eab7_640.png"),
            user_id=1)
session.add(item)
session.commit()

item = Item(
            name="Back Flip",
            category_id=3,
            description="Magestic flip to the back with no fear",
            picture=("https://pixabay.com/get/"
                     "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                     "4b0144095f9c571a2eab7_640.png"),
            user_id=3)
session.add(item)
session.commit()


item = Item(
            name="Suicides",
            category_id=3,
            description="Amazing New Trick",
            picture=("https://pixabay.com/get/"
                     "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                     "4b0144095f9c571a2eab7_640.png"),
            user_id=1)
session.add(item)
session.commit()


item = Item(
            name="Football",
            category_id=4,
            description="Best sport of all time and also the most viewed",
            picture=("https://pixabay.com/get/"
                     "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                     "4b0144095f9c571a2eab7_640.png"),
            user_id=1)
session.add(item)
session.commit()


item = Item(
            name="Basketball",
            category_id=4,
            description="Lebron James's sport",
            picture=("https://pixabay.com/get/"
                     "eb3cb50e20fc043ed95c4518b74b469ee07fe1d20"
                     "4b0144095f9c571a2eab7_640.png"),
            user_id=1)
session.add(item)
session.commit()

print "Finished adding items"
