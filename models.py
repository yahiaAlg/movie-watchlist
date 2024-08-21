from dataclasses import dataclass, field
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
    rating: float = 0
    video_link: str = None

    def __post_init__(self):
        if self.date_added is None:
            self.date_added = datetime.datetime.now()