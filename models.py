from dataclasses import dataclass, field
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid


@dataclass
class Movie:
    title: str
    director: str
    year: datetime.date
    _id: str = uuid.uuid4().hex
    description: str = None
    tags: list[str] = field(default_factory=list)
    casts: list[str] = field(default_factory=list)
    series: list[str] = field(default_factory=list)
    date_added: datetime.datetime = field(default_factory=datetime.datetime.now)
    last_seen: datetime.datetime = field(default_factory=datetime.datetime.now)
    rating: float = 0
    video_link: str = None

    def __post_init__(self):
        if self.date_added is None:
            self.date_added = datetime.datetime.now()
            


@dataclass
class User:
    email: str
    name: str
    password: str = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    password_hash: str = field(default_factory=str)
    movie_ids: List[str] = field(default_factory=list)

    
    def __post_init__(self):
        self.password_hash = generate_password_hash(self.password)
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
