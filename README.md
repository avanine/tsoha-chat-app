# Chat App

![Pylint](https://github.com/avanine/tsoha-chat-app/actions/workflows/pylint.yml/badge.svg)

A chat application built with Flask and PostgreSQL, featuring categories, threads, and messages. Categories contain discussion threads, which consist of messages. Users must be logged in to view and participate in discussions. The app supports both regular users and administrators, with admins having additional privileges like managing categories and creating private categories.

## Table of Contents

- [How to Test](#how-to-test)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Structure](#database-structure)

## How to Test

_The app was originally deployed to Fly.io, but due to very unclear pricing, I have taken it down. This means that the app will have to be tested locally._

1. Clone the repository and navigate to the root directory

2. Create a ``.env`` file with the following variables, changing the values to your own

```
DATABASE_URL=postgresql:///yourlocaldatabaseaddress
SECRET_KEY=supersecret
```

3. Activate Python's virtual environment and install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

4. Specify database schema

```
psql < schema.sql
```

5. Run the app 🦄

```
flask run
```

## Features

### General User Features
- Create a new account.
- Log in and log out.
- When logged in, view a list of categories, including the number of threads and messages, and the timestamp of the most recent message.
- Create new threads within a category, with a title and initial message content.
- Post messages in existing threads.
- Edit the title of threads they created, the content of their messages, and delete their threads and messages.
- Search for messages containing a given word.

### Admin Features
- Add and delete categories.
- Create private categories and specify which users can access them.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap
- **Other Tools:** SQLAlchemy for database ORM, Jinja2 for templating

## Database Structure


![database-structure](https://github.com/user-attachments/assets/8dd78b49-ef99-46eb-9ca7-c64886879815)
