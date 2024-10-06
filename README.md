# Chat App

![Pylint](https://github.com/avanine/tsoha-chat-app/actions/workflows/pylint.yml/badge.svg)

A chat application built with Flask and PostgreSQL, featuring categories, threads, and messages. Categories contain discussion threads, which consist of messages. Users must be logged in to view and participate in discussions. The app supports both regular users and administrators, with admins having additional privileges like managing categories and creating private categories.

## Table of Contents

- [Current Progress](#current-progress)
- [Possible Improvements](#possible-improvements)
- [How to Test](#how-to-test)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Structure](#database-structure)

## Current Progress

Visitors are able to register either as an admin or regular user, and log in with the username and password that they created. Possible error messages: username already in use, passwords don't match, incorrect username or password.

![image](https://github.com/user-attachments/assets/0c2bffef-bf06-4913-87fa-fbe505c66a92)

After logging in, there is a dashboard with categories that the user has access to, including the amount of threads and messages, as well as the time of last message for each category. Clicking on the category name opens up the category page. Admins can also see a button for creating a new category.

![image](https://github.com/user-attachments/assets/a45ebad3-cc34-4faf-a152-5773c0509849)

A delete-button will appear by hovering over the category tile (admin feature).

![image](https://github.com/user-attachments/assets/07fc0ef0-dcef-4154-bb94-a916e5420d1b)

All users can see their username and role, and log out using the menu at the top right of the page.

![image](https://github.com/user-attachments/assets/b5712824-102c-4661-bf12-50d4d53a142d)

All users can use the search bar to search for specific messages that they have access to.

![image](https://github.com/user-attachments/assets/187ce0d2-4234-4497-a156-8967589b6605)

Admin users can create a new public or private category.

![image](https://github.com/user-attachments/assets/dce0aa53-2f6f-4fb3-a617-bc61ec24b9be)

If they choose to create a private category, they are able to select the users that they want to give access to.

![image](https://github.com/user-attachments/assets/98220929-79ce-43c4-b16d-40e3291d971e)

Category pages display all threads within a category, with edit and delete options available for threads created by the logged-in user. In the main view, users can see all messages in the selected thread, along with a kebab menu for editing or deleting their own messages. An 'Edited' tag will appear on threads and messages that have been modified.

![image](https://github.com/user-attachments/assets/7a8f3552-6bb3-48de-944c-59831806412d)

## Possible improvements

- nicer footer
- reduce the amount of scroll bars in category page
- after deleting a thread, it still shows in the main view until the user clicks somewhere else
- separate .py-files into folders
- accessibility and style improvements here and there
- better support for smaller screens (threads list)
- highlight message that was found and opened through search

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
