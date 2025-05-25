import json
import random
from datetime import datetime

from faker import Faker

from db import session
from recsys_config import CATEGORIES
from factories import (UserFactory,
                       CategoryFactory,
                       HashtagFactory,
                       PollFactory,
                       HashtagToPollFactory,
                       OptionFactory,
                       VoteFactory)


fake = Faker()

print("\n🚀 Starting database population...")
print("\n1️⃣  Creating users...")
users = UserFactory.create_batch(100)
print("✅ Created 100 users")

print("\n2️⃣  Creating categories...")
categories = [CategoryFactory.create(name=cat) for cat in CATEGORIES]
session.flush()
print(f"✅ Created {len(categories)} categories")

print("\n3️⃣  Loading poll data...")
with open("data/polls.json", "r", encoding='utf-8') as file:
    polls_data = json.load(file)
print(f"📊 Found {len(polls_data)} polls to process")

print("\n4️⃣  Creating polls, options, hashtags, hashtags_to_polls and votes...")
unique_tags = {}
counters = {"polls": 0, "options": 0, "hashtags": 0, "hashtags_to_polls": 0, "votes": 0}

for item in polls_data:
    user = random.choice(users)
    category = categories[CATEGORIES.index(item["category"])]

    # Create poll
    poll = PollFactory.create(
        title=item["title"],
        description=item["description"],
        possible_answers_count=item["possible_answers_count"],
        access_mode=item["access_mode"],
        tags=item["tags"],
        category=category,
        user=user
    )
    session.flush()
    counters["polls"] += 1

    # Create poll options
    options = []
    for option in item["options"]:
        options.append(OptionFactory.create(
            content=option["content"],
            position=option["position"],
            is_correct=option["is_correct"],
            poll=poll
        ))
    counters["options"] += len(options)

    # Create and link hashtags
    for tag in item["tags"]:
        if tag not in unique_tags:
            unique_tags[tag] = HashtagFactory.create(name=tag)
            counters["hashtags"] += 1
        
        session.flush()
        HashtagToPollFactory.create(hashtag_id=unique_tags[tag].id,
                                    poll_id=poll.id)
        counters["hashtags_to_polls"] += 1

    users_copy = users.copy()
    
    # Create votes
    for i in range(random.randint(0, len(users))):
        user = random.choice(users_copy)
        users_copy.remove(user)
        voted_at = fake.date_time_between(user.last_login, datetime.now())

        for j in random.sample(list(range(len(options))), poll.possible_answers_count):
            VoteFactory.create(user_id=user.id, option_id=options[j].id, voted_at=voted_at)
            counters["votes"] += 1

print(f"✅ Created {counters['polls']} polls")
print(f"✅ Created {counters['options']} options")
print(f"✅ Created {counters['hashtags']} hashtags")
print(f"✅ Created {counters['hashtags_to_polls']} hashtags_to_polls")
print(f"✅ Created {counters['votes']} votes")

print("\n5️⃣  Save changes...")
session.commit()

print("\n🎉 Database population completed!")
