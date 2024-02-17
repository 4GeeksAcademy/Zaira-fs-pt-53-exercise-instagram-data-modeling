import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Follow(Base):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(20), nullable=False)  
    profile_picture = Column(String(255))  # URL or path to the profile picture
    profile_description = Column(String(240))
    posts = relationship('Post', backref='user', lazy=True) # lazy = will not be loaded from the database until you explicitly request them.
    comments = relationship('Comment', backref='user', lazy=True) # backref is a way to establish a bidirectional relationship between two models. 
    liked_posts = relationship('likes', backref='user', lazy=True)
    followers = relationship('Follow', foreign_keys=[Follow.followed_id], backref='followed_user', lazy='dynamic')
    following = relationship('Follow', foreign_keys=[Follow.follower_id], backref='follower_user', lazy='dynamic')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    caption = Column(String(240))
    image_url = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comments = relationship('Comment', backref='post', lazy=True)
    liked_posts = relationship('likes', backref='post', lazy=True)
    tags = relationship('Tag', secondary='post_tag', backref='posts')

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class PostTag(Base):
    __tablename__ = 'post_tag'
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(String(240), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)



## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
