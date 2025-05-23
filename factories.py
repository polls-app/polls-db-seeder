import random
from uuid import uuid4
from datetime import datetime

import factory
from faker import Faker

from db import session
from vectorizer import PollVectorizer
from models import (User,
                    Category,
                    Poll,
                    Hashtag,
                    HashtagToPoll,
                    Option,
                    Vote)


fake = Faker()
vectorizer = PollVectorizer()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    id = factory.LazyFunction(lambda: str(uuid4()))
    email = factory.Sequence(lambda n: f"user{n + 1}@example.com")
    password = factory.Faker('password', length=97)
    role = factory.LazyAttribute(
        lambda self: random.choices(
            ["admin", "pollee"],
            weights=self.user_role_weights,
            k=1
        )[0]
    )
    is_verified = factory.LazyAttribute(
        lambda self: random.random() > self.verified_percent
    )
    joined_at = factory.LazyAttribute(
        lambda self: fake.date_time_between(self.min_joined_date, self.max_joined_date)
    )
    last_login = factory.LazyAttribute(
        lambda self: fake.date_time_between(self.joined_at, datetime.now())
    )

    class Params:
        user_role_weights = [0.1, 0.9]  # for admins and pollees
        verified_percent = 0.5
        min_joined_date = datetime(2010, 1, 1)
        max_joined_date = datetime.now()
    

class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = session

    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Sequence(lambda n: f"Category {n + 1}")


class HashtagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Hashtag
        sqlalchemy_session = session

    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Faker("word")


class PollFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Poll
        sqlalchemy_session = session

    id = factory.LazyFunction(lambda: str(uuid4()))
    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("text")
    color_hex = factory.Faker("color")
    lang_code = "en"
    access_mode = factory.LazyAttribute(
        lambda self: random.choices(
                ["restricted", "public"],
                weights=self.poll_access_modes,
                k=1
            )[0]
    )
    possible_answers_count = factory.LazyFunction(
        lambda: random.randint(1, 5)
    )
    created_at = factory.LazyAttribute(
        lambda self: fake.date_time_between(self.user.last_login, datetime.now())
    )

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        self.embedding = vectorizer.vectorize_poll(
        {
            "title": self.title,
            "description": self.description,
            "lang_code": self.lang_code,
            "category": self.category.name,
            "tags": extracted or [fake.word() for _ in range(random.randint(1, 10))]
        }

    )
        
    class Params:
        poll_access_modes = [0.1, 0.9]  # for restricted and public polls
        

class HashtagToPollFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HashtagToPoll
        sqlalchemy_session = session


class OptionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Option
        sqlalchemy_session = session

    id = factory.LazyFunction(lambda: str(uuid4()))
    content = factory.Faker("sentence", nb_words=3)
    position = 1
    is_correct = factory.LazyFunction(lambda: random.random() > 0.5)
    
    poll = factory.SubFactory(PollFactory)


class VoteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Vote
        sqlalchemy_session = session
