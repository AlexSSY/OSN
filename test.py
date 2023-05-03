import random
from api.db.database import SessionLocal, Base, engine
from api.models.user import User
from api.models.online_status import OnlineStatus
from api.models.message import Message
from faker import Faker


# Create all tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

faker = Faker()

with SessionLocal() as db:

    db.add(OnlineStatus(
        name="offline",
        image_url=f"http://{faker.domain_name()}/{faker.name()}.jpg")
    )

    db.add(OnlineStatus(
        name="online",
        image_url=f"http://{faker.domain_name()}/{faker.name()}.jpg")
    )

    db.add(OnlineStatus(
        name="sleeping",
        image_url=f"http://{faker.domain_name()}/{faker.name()}.jpg")
    )

    db.add(OnlineStatus(
        name="playing",
        image_url=f"http://{faker.domain_name()}/{faker.name()}.jpg")
    )

    db.commit()

    online_status_indexes = [1, 2 ,3, 4]

    for _ in range(0, 100):
        user = User(
            email=faker.email(),
            password=faker.password(),
            online_status=db.query(OnlineStatus).filter(
                OnlineStatus.id == online_status_indexes[random.randint(0, 3)]).first()
        )
        db.add(user)
    db.commit()

    for i in range(0, 7000):

        sender_id = random.randint(1, 100)
        receiver_id = random.randint(1, 100)

        if sender_id == receiver_id:
            continue

        msg = Message(
            message=faker.text(),
            date=faker.date_time(),
            sender=db.query(User).filter(User.id == sender_id).first(),
            receiver=db.query(User).filter(User.id == receiver_id).first()
        )

        db.add(msg)
    db.commit()
