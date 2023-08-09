# messenger-backend

#### A fully working backend of messenger, websockets are in development yet, you can see the progress here: https://github.com/mrsupertop/fastsockets

# How to run?
## Step 1, installing dependencies

#### You can use [poetry](https://python-poetry.org/docs/) to automatically create virtual environment for this project:
#### Install poetry with your python
###### pip install poetry
#### Create virtual environment
###### poetry install

## Step 2, configure databases in the config file
#### For testing you can juse use docker:
###### docker compose up

## Step 3, starting
#### The first time you run the project, you will need to create databases, to do that follow next steps
###### Go to package/db/__init__.py and replace generate_schemas=False with generate_schemas=True
#### Then just run package/__main__.py file
###### python package/__main__.py

# Endpoints

### Overall structure of endpoints
![image](https://github.com/batreller/messenger-backend/assets/120225698/7072b84d-2063-43ef-abae-350d6ffd522d)

## More detailed description

### POST - {{address}}/register
Body:
```
{
    "username": "username",
    "email": "email@example.com",
    "password": "password"
}
```

Response:
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNjkxNTUxMDY2fQ.pYdSZN0SAVFyqMJJ3xCnQ3cpgZrRSrY9uldENnAdGYw",
    "token_type": "bearer"
}
```

### POST - {{address}}/login
Body:
```
{
    "usernameOrEmail": "username",
    "password": "password"
}
```

Response:
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNjkxNTUxMTIzfQ.6l1SStyCrBoPtLht1oiSvOQ7sPgU4A_byJv0a7o1Mdg",
    "token_type": "bearer"
}
```

### GET - {{address}}/user/me
#### returns information about current user
authorization via bearer token from response of register/login endpoints required

Response:
```
{
    "id": 5,
    "created_at": "2023-08-09T01:17:46.419120+00:00",
    "updated_at": "2023-08-09T01:17:46.425569+00:00",
    "username": "username",
    "email": "email@example.com",
    "bio": null,
    "email_confirmed": false
}
```

### GET - {{address}}/user/chats
#### retunrs list of user's chats
authorization via bearer token from response of register/login endpoints required

Response:
```
{
    "next": "2023-08-09T01:20:36.545682+00:00",
    "count": 1,
    "chats": [
        {
            "id": 4,
            "created_at": "2023-08-09T01:20:36.545682+00:00",
            "updated_at": "2023-08-09T01:20:36.545682+00:00",
            "name": null,
            "type": "private",
            "last_message": null
        }
    ]
}
```

### PATCH - {{address}}/user/bio
#### returns if request was successfull
authorization via bearer token from response of register/login endpoints required

Body:
```
{
    "bio": "Hi there!"
}
```

Response:
```
{
    "success": true
}
```

### POST - {{address}}/chat/private/create
#### returns information about just created chat
authorization via bearer token from response of register/login endpoints required

Body:
```
{"with_user_id": 6}
```

Response:
```
{
    "id": 5,
    "created_at": "2023-08-09T01:25:11.886035+00:00",
    "updated_at": "2023-08-09T01:25:11.886035+00:00",
    "name": null,
    "type": "private",
    "last_message": null,
    "participants": [
        {
            "id": 5,
            "username": "username"
        },
        {
            "id": 2,
            "username": "user2"
        }
    ]
}
```

### POST - {{address}}/chat/group/create
#### returns information about just created group
authorization via bearer token from response of register/login endpoints required

Data:
```
{
    "with_ids": [2, 3],
    "name": "Best friends!"
}
```

Response:
```
{
    "id": 6,
    "created_at": "2023-08-09T01:26:00.361578+00:00",
    "updated_at": "2023-08-09T01:26:00.361578+00:00",
    "name": "Best friends!",
    "type": "group",
    "last_message": null,
    "participants": [
        {
            "id": 5,
            "username": "username"
        },
        {
            "id": 2,
            "username": "user2"
        },
        {
            "id": 3,
            "username": "user3"
        }
    ]
}
```

### POST - {{address}}/chat/{{chat_id}}/message
#### returns information about just sent message
authorization via bearer token from response of register/login endpoints required

Data:
```
{"contents": "hello to group"}
```

Response:
```
{
    "id": 8,
    "created_at": "2023-08-09T01:26:57.621299+00:00",
    "updated_at": "2023-08-09T01:26:57.621299+00:00",
    "contents": "hello to group",
    "author_id": 5
}
```

### GET - {{address}}/chat/{{chat_id}}/messages?cursor=1&limit=2
#### returns messages from the chat
authorization via bearer token from response of register/login endpoints required

Response:
```
{
    "count": 1,
    "authors": [
        {
            "id": 5,
            "username": "username"
        }
    ],
    "messages": [
        {
            "id": 8,
            "created_at": "2023-08-09T01:26:57.621299+00:00",
            "updated_at": "2023-08-09T01:26:57.621299+00:00",
            "contents": "hello to group",
            "author_id": 5
        }
    ]
}
```

### GET - {{address}}/chat/{{chat_id}}
#### returns participants of the chat
authorization via bearer token from response of register/login endpoints required

Response:
```
{
    "id": 6,
    "created_at": "2023-08-09T01:26:00.361578+00:00",
    "updated_at": "2023-08-09T01:26:00.361578+00:00",
    "name": "Best friends!",
    "type": "group",
    "last_message": {
        "id": 8,
        "created_at": "2023-08-09T01:26:57.621299+00:00",
        "updated_at": "2023-08-09T01:26:57.621299+00:00",
        "contents": "hello to group",
        "author_id": 5
    },
    "participants": [
        {
            "id": 5,
            "username": "username"
        },
        {
            "id": 2,
            "username": "user2"
        },
        {
            "id": 3,
            "username": "user3"
        }
    ]
}
```
