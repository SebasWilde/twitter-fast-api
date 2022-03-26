import json
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from fastapi import FastAPI, status, Body
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


# Models


class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64)


class User(UserBase):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    birthday: Optional[date] = Field(None)


class UserRegister(User):
    password: str = Field(..., min_length=8, max_length=64)


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., min_length=1, max_length=256)
    created_at: datetime = Field(datetime.now())
    updated_at: Optional[datetime] = Field(None)
    by: User = Field(...)


# Users
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register a user',
    tags=['Users'],
)
def signup(user: UserRegister = Body(...)):
    """
    Register a new user

    Parameters:
        - Request body parameter:
            - user: UserRegister

    Returns a json with user information
        - user_id: UUID
        - email: EmailStr
        - first_name: First name
        - last_name: Last name
        - birthday: date
    """
    with open('users.json', 'r+', encoding='utf-8') as f:
        db = json.loads(f.read())
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birthday'] = str(user_dict['birthday'])
        db.append(user_dict)
        f.seek(0)
        f.write(json.dumps(db, indent=2))

        return user


@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login a user',
    tags=['Users'],
)
def login():
    ...


@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Get all users',
    tags=['Users'],
)
def get_users():
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Get specific user',
    tags=['Users'],
)
def get_user():
    ...


@app.delete(
    path='/users/{user_id}/delete',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a user',
    tags=['Users'],
)
def delete_user():
    ...


@app.put(
    path='/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update a user',
    tags=['Users'],
)
def update_user():
    ...


# Tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Get all tweets',
    tags=['Tweets'],
)
def home():
    with open('tweets.json', 'r') as f:
        return json.loads(f.read())


@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Create a tweet',
    tags=['Tweets'],
)
def create_tweet(tweet: Tweet = Body(...)):
    with open('tweets.json', 'r+') as f:
        db = json.loads(f.read())
        tweet_data = tweet.dict()
        tweet_data['tweet_id'] = str(tweet_data['tweet_id'])
        tweet_data['created_at'] = str(tweet_data['created_at'])
        tweet_data['updated_at'] = str(tweet_data['updated_at'])
        tweet_data['by']['user_id'] = str(tweet_data['by']['user_id'])
        tweet_data['by']['birthday'] = str(tweet_data['by']['birthday'])
        db.append(tweet_data)
        f.seek(0)
        f.write(json.dumps(db, indent=2))

        return tweet


@app.get(
    path='/get/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Get a tweet',
    tags=['Tweets'],
)
def get_tweet():
    ...


@app.delete(
    path='/get/{tweet_id}/delete',
    status_code=status.HTTP_201_CREATED,
    summary='Delete a tweet',
    tags=['Tweets'],
)
def delete_tweet():
    ...


@app.put(
    path='/get/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Update a tweet',
    tags=['Tweets'],
)
def update_tweet():
    ...
