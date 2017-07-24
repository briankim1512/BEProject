# WARNING--> Execute this code ONLY ONCE, else there will be duplicate entries.
# Imports for the necessary modules to run SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, ItemCat

# Make an engine to run SQL sessions and commit entries
engine = create_engine('sqlite:///itemcat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

item1 = ItemCat(name="Monitor", category="Screens",
                description="A standard 24 inch, 1920 by 1080 resolution " +
                "monitor. It has a 60hz refresh rate and the panel is IPS")
session.add(item1)
session.commit()

item2 = ItemCat(name="Desktop", category="Computers",
                description="A computer with a 4 core CPU and integrated " +
                "graphics. Also contains 1 TB of storage and 8 GB of ram " +
                "memory.")
session.add(item2)
session.commit()

item3 = ItemCat(name="Keyboard", category="Computer Accessory",
                description="A mechanical swith keyboard. The switches " +
                "feature a clicky acoustic and tactile feedback.")
session.add(item3)
session.commit()

item4 = ItemCat(name="Mouse", category="Computer Accessory",
                description="A wireless mouse that uses a small dongle for " +
                "connection. The mouse is also 'ergonomic' and fits nicely " +
                "to the hand.")
session.add(item4)
session.commit()

item5 = ItemCat(name="Laptop", category="Computers",
                description="A laptop with a 2 core CPU and integrated " +
                "graphics. Contains 500 GB of storage and 4 GB of ram. " +
                "Extremely portable form and weighs 2 kg.")
session.add(item5)
session.commit()

item6 = ItemCat(name="Earphones", category="Audio Equipment",
                description="An earphone with 3 drivers on each channel. " +
                "Made with precise German engineering.")
session.add(item6)
session.commit()

item7 = ItemCat(name="Microphone", category="Audio Equipment",
                description="A omni-directional microphone that allows " +
                "recordings from any direction.")
session.add(item7)
session.commit()

item8 = ItemCat(name="External Harddrive", category="Computer Accessory",
                description="An external harddrive that holds around 2 TB " +
                "of data.")
session.add(item8)
session.commit()

item9 = ItemCat(name="Battery Backup", category="Electronics Accessories",
                description="A massive 50,000 mAh battery to charge almost " +
                "anything you can throw at it.")
session.add(item9)
session.commit()

item10 = ItemCat(name="Micro SD card", category="Electronics Accessories",
                 description="A small data storage device that can be " +
                 "converted to fit any device IO.")
session.add(item10)
session.commit()
