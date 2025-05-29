import json
import random
import itertools
from datetime import datetime

from faker import Faker

from db import session
from recsys_config import CATEGORIES
from factories import (UserFactory,
                       ProfileFactory,
                       CategoryFactory,
                       HashtagFactory,
                       PollFactory,
                       HashtagToPollFactory,
                       OptionFactory,
                       VoteFactory,
                       ShareFactory,
                       FollowingFactory,
                       PollInvitedUserFactory,
                       CommentFactory)


fake = Faker()

print("\n🚀 Starting database population...")
print("\n1️⃣  Creating users...")
users = UserFactory.create_batch(100)
print("✅ Created 100 users")

print("\n2️⃣  Creating profiles...")
profiles = [ProfileFactory.create(user=user) for user in users]
print("✅ Created 100 profiles")

print("\n3️⃣  Creating followings...")
followings = [FollowingFactory.create(follower=follower, user=user)
                          for follower, user in itertools.product(users, users)
                          if follower != user and random.random() > 0.75]
print(f"✅ Created {len(followings)} followings")

print("\n4️⃣  Creating categories...")
categories = [CategoryFactory.create(name=cat) for cat in CATEGORIES]
session.flush()
print(f"✅ Created {len(categories)} categories")

print("\n5️⃣  Loading poll data...")
with open("data/polls.json", "r", encoding='utf-8') as file:
    polls_data = json.load(file)
print(f"📊 Found {len(polls_data)} polls to process")

print("\n6️⃣  Creating polls, options, hashtags, and more...")
unique_tags = {}
counters = {"polls": 0, "options": 0, "invitations": 0, "hashtags": 0,
            "hashtags_to_polls": 0, "votes": 0, "comments": 0}
polls = []

for item in polls_data:
    user = random.choice(users)
    category = categories[CATEGORIES.index(item["category"])]

    # Update contribution count in profile
    profiles[users.index(user)].contribution_count += 1

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
    polls.append(poll) 
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

    # Create invitations
    if poll.access_mode == "restricted":
        invited_users = random.sample(users, k=random.randint(0, 20))
        invitations = [PollInvitedUserFactory(poll_id=poll.id, user_id=user.id)
                       for user in invited_users]
        counters["invitations"] += len(invitations)

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

    # Create comments for 30% of polls
    if random.random() > 0.7:
        comments = [CommentFactory.create(poll=poll, user=user)
                    for user in random.sample(users, k=random.randint(1, len(users) // 2))]
        counters["comments"] += len(comments)
        

print(f"✅ Created {counters['polls']} polls")
print(f"✅ Created {counters['options']} options")
print(f"✅ Created {counters['invitations']} invitations")
print(f"✅ Created {counters['hashtags']} hashtags")
print(f"✅ Created {counters['hashtags_to_polls']} hashtags_to_polls")
print(f"✅ Created {counters['votes']} votes")
print(f"✅ Created {counters['comments']} comments")

print("\n7️⃣  Creating shares...")
share_combinations = list(itertools.product(users, polls))
selected_share_combinations = random.sample(share_combinations, k=len(polls)*2)
shares = [ShareFactory.create(user_id=user.id, poll_id=poll.id) for user, poll in selected_share_combinations]
print(f"✅ Created {len(shares)} shares")

print("\n8️⃣  Save changes...")
session.commit()

print("\n🎉 Database population completed!")
