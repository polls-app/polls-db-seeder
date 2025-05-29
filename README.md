# PollsApp Test Data Generator

A test data generation tool for the PollsApp web application database. This utility populates your database with realistic sample data including users, categories, polls, options, hashtags, and votes.

## Requirements

- **Python 3.10.7 or higher**
- Virtual environment (recommended)
- PostgreSQL database

## Setup

### 1. Virtual Environment

Activate your virtual environment:

```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root with your database credentials:

```env
DB_HOST="your-host"
DB_PORT="your-port"
DB_NAME="your-db-name"
DB_USER="your-username"
DB_PASSWORD="your-password"
```

## Usage

To generate test data, run the seed script:

```bash
python seed.py
```

## Generated Data

The data generator creates the following entities:

### 📊 Data Overview

| Entity | Quantity | Description |
|--------|----------|-------------|
| **Users** | 100 | Fake user accounts with realistic data |
| **Profiles** | 100 | Fake user profiles with realistic data |
| **Followings** | Variable | Randomly generated followings, the number is about 25% of all possible followings between 100 users |
| **Categories** | Variable | Poll categories from configuration |
| **Polls** | Variable | Polls loaded from `data/polls.json` |
| **Options** | Variable | Poll answer options |
| **PollInvitedUsers** | Variable | Each poll with `access_mode=“restricted”` can have from 1 to 20 randomly generated invitations |
| **Hashtags** | Variable | Unique hashtags extracted from poll data |
| **Votes** | Variable | Random user votes on poll options |
| **Shares** | Variable | Twice the number of polls |
| **Comments** | Variable | Approximately 30% of the polls have single-level (non-nested) comments; such polls can have anywhere from 1 to 50 comments |

## Output

The script provides real-time feedback during execution:

```
🔄️ Loading sentence transformer model...
✅ Successfully loaded

🚀 Starting database population...

1️⃣ Creating users...
✅ Created 100 users

2️⃣ Creating profiles...
✅ Created 100 profiles

3️⃣ Creating followings...
✅ Created 2481 followings

4️⃣ Creating categories...
✅ Created 41 categories

5️⃣ Loading poll data...
📊 Found 37 polls to process

6️⃣ Creating polls, options, hashtags, and more...
✅ Created 37 polls
✅ Created 182 options
✅ Created 9 invitations
✅ Created 161 hashtags
✅ Created 211 hashtags_to_polls
✅ Created 1844 votes
✅ Created 308 comments

7️⃣ Creating shares...
✅ Created 74 shares

8️⃣ Save changes...

🎉 Database population completed!
```
