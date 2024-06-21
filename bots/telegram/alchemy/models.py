from datetime import datetime

from sqlalchemy import (
    VARCHAR,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import backref, relationship

from .crud import Base


class BotUserEvent(Base):
    __tablename__ = 'events_botuserevent'

    id = Column(Integer, primary_key=True)
    user_id = Column(VARCHAR(length=64), ForeignKey('botuser_botuser.chat_id'))
    event_id = Column(Integer, ForeignKey('events_event.id'))
    notification_type = Column(Integer, nullable=True)

    def __int__(
            self,
            id: int,
            user_id: str,
            event_id: int,
            notification_type: int | None = None
    ):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.event_id = event_id
        self.notification_type = notification_type


class BotAdmin(Base):
    __tablename__ = 'botuser_botadmin'
    id = Column('chat_id', VARCHAR(length=64), primary_key=True)
    get_preview = Column(Boolean, default=False)
    user_id = Column(
        Integer,
        ForeignKey('auth_user.id')
    )

    def __int__(
            self,
            id: int,
            chat_id: str,
            user_id: int,
            get_preview: bool = False
    ):
        super().__init__()
        self.id = id
        self.chat_id = chat_id
        self.user_id = user_id
        self.get_preview = get_preview


class BotUser(Base):
    __tablename__ = 'botuser_botuser'

    id = Column('chat_id', VARCHAR(length=64), primary_key=True)
    get_articles = Column(Boolean, default=False)
    get_demo_week = Column(Boolean, default=False)
    username = Column(VARCHAR(length=128), nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    first_name = Column(VARCHAR(length=64), nullable=True)
    last_name = Column(VARCHAR(length=64), nullable=True)
    language_code = Column(VARCHAR(length=16), nullable=True)

    def __init__(
            self,
            id: int,
            get_articles: bool = False,
            get_demo_week: bool = False,
            username: str = None,
            email: str = None,
            phone: str = None,
            first_name: str = None,
            last_name: str = None,
            language_code: str = None
    ):
        super().__init__()
        self.id = id
        self.get_articles = get_articles
        self.get_demo_week = get_demo_week
        self.username = username
        self.email = email
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code


class Event(Base):
    __tablename__ = 'events_event'

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(length=255))
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=True)
    stream_link = Column(String, nullable=True)
    is_complete = Column(Boolean, default=False)
    do_broadcast = Column(Boolean, default=False)

    def __init__(
            self,
            id: int,
            title: str,
            description: str | None = None,
            date: datetime | None = None,
            stream_link: str | None = None,
            is_complete: bool = False,
            do_broadcast: bool = False
    ):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.stream_link = stream_link
        self.is_complete = is_complete
        self.do_broadcast = do_broadcast


class Notification(Base):
    __tablename__ = 'notifications_notification'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    preview = Column(Boolean, default=True)
    message_time = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)

    def __int__(
            self,
            id: int,
            text: str,
            preview: bool = False,
            message_time: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        super().__init__()
        self.id = id
        self.text = text
        self.preview = preview
        self.message_time = message_time
        self.created_at = created_at
        self.updated_at = updated_at


class NotificationContent(Base):
    __tablename__ = 'notifications_notificationcontent'

    id = Column(Integer, primary_key=True)
    content_type = Column(VARCHAR(length=128), nullable=True)
    file = Column(Text)
    add_to_group = Column(Boolean, default=False, nullable=True)
    has_spoiler = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now,
                        onupdate=datetime.now)
    notification_id = Column(
        Integer,
        ForeignKey('notifications_notification.id')
    )

    def __int__(
            self,
            id: int,
            file: str,
            notification_id: int,
            content_type: str | None = None,
            add_to_group: bool | None = False,
            has_spoiler: bool | None = False,
            created_at: datetime = datetime.now,
            updated_at: datetime = datetime.now,
    ):
        super().__init__()
        self.id = id
        self.file = file
        self.notification_id = notification_id
        self.content_type = content_type
        self.add_to_group = add_to_group
        self.has_spoiler = has_spoiler
        self.created_at = created_at
        self.updated_at = updated_at


class EventNotification(Base):
    __tablename__ = 'events_eventnotification'

    id = Column(
        'notification_ptr_id',
        Integer,
        ForeignKey('notifications_notification.id'),
        primary_key=True
    )
    event_id = Column(Integer, ForeignKey('events_event.id'))
    notification_type = Column(Integer, nullable=True)

    def __int__(
            self,
            id: int,
            event_id: int,
            notification_type: int | None = None,
    ):
        super().__init__()
        self.id = id
        self.event_id = event_id
        self.notification_type = notification_type


class ArticleNotification(Base):
    __tablename__ = 'article_articlenotification'

    id = Column(
        'notification_ptr_id',
        Integer,
        ForeignKey('notifications_notification.id'),
        primary_key=True,
    )
    notifications = relationship(
        Notification,
        backref=backref('article_articlenotification'),
        lazy='subquery'
    )

    title = Column(VARCHAR(length=255))
    comment = Column(Text, nullable=True)
    notify_immediately = Column(Boolean, default=False)
    is_complete = Column(Boolean, default=True)

    def __int__(
            self,
            id: int,
            title: str,
            comment: str | None = None,
            notify_immediately: bool = False,
            is_complete: bool = True
    ):
        super().__init__()
        self.id = id
        self.title = title
        self.comment = comment
        self.notify_immediately = notify_immediately
        self.is_complete = is_complete


class DemoWeek(Base):
    __tablename__ = 'demoweek_demoday'

    id = Column(
        'notification_ptr_id',
        Integer,
        ForeignKey('notifications_notification.id'),
        primary_key=True
    )
    weekday = Column(Integer, nullable=True)

    def __int__(
            self,
            id: int,
            weekday: int | None = None,
    ):
        super().__init__()
        self.id = id
        self.weekday = weekday


class University(Base):
    __tablename__ = 'data_university'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(length=255))
    created_at = Column(DateTime(), default=datetime.now)

    def __int__(
            self,
            id: int,
            name: str,
            created_at: datetime
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.created_at = datetime.now()


class ProgramName(Base):
    __tablename__ = 'data_programname'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(length=255))

    def __int__(
            self,
            id: int,
            name: str
    ):
        super().__init__()
        self.id = id
        self.name = name


class Program(Base):
    __tablename__ = 'data_program'

    id = Column(Integer, primary_key=True)
    university_id = Column(
        Integer,
        ForeignKey('data_university.id')
    )
    program_name_id = Column(
        Integer,
        ForeignKey('data_programname.id')
    )

    created_at = Column(DateTime(), default=datetime.now)

    def __int__(
            self,
            id: int,
            name: str,
            university_id: int,
            created_at: datetime
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.university_id = university_id
        self.created_at = datetime.now()


class QuestionContent(Base):
    __tablename__ = 'data_questioncontent'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime(), default=datetime.now)

    def __int__(
            self,
            id: int,
            title: str,
            answer: str,
            created_at: datetime
    ):
        super().__init__()
        self.id = id
        self.title = title
        self.answer = answer
        self.created_at = datetime.now()


class Question(Base):
    __tablename__ = 'data_question'

    id = Column(Integer, primary_key=True)
    program_id = Column(
        Integer,
        ForeignKey('data_program.id')
    )
    question_id = Column(
        Integer,
        ForeignKey('data_questioncontent.id')
    )

    def __int__(
            self,
            id: int,
            program_id: int,
            question_id: int,
    ):
        super().__init__()
        self.id = id
        self.program_id = program_id
        self.question_id = question_id


class SubQuestionContent(Base):
    __tablename__ = 'data_subquestioncontent'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    answer = Column(Text)

    def __int__(
            self,
            id: int,
            text: str,
            answer: str,
    ):
        super().__init__()
        self.id = id
        self.text = text
        self.answer = answer


class SubQuestion(Base):
    __tablename__ = 'data_subquestion'

    id = Column(Integer, primary_key=True)
    question_id = Column(
        Integer,
        ForeignKey('data_questioncontent.id')
    )
    content_id = Column(
        Integer,
        ForeignKey('data_suquestioncontent.id')
    )

    def __int__(
            self,
            id: int,
            question_id: int,
            content_id: int,
    ):
        super().__init__()
        self.id = id
        self.question_id = question_id
        self.content_id = content_id


class CuratorAnswer(Base):
    __tablename__ = 'curator_curatoranswer'

    id = Column('message_id', VARCHAR(length=64), primary_key=True)
    chat_id = Column(VARCHAR(length=64))
    text = Column(Text)

    def __int__(
            self,
            id: int,
            chat_id: str,
            text: str,
    ):
        super().__init__()
        self.id = id
        self.chat_id = chat_id
        self.text = text


class CuratorChat(Base):
    __tablename__ = 'curator_curatorchat'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=False)
    chat_id = Column(VARCHAR(length=64))

    def __int__(
            self,
            id: int,
            chat_id: str,
            is_active: bool | None = False,
    ):
        super().__init__()
        self.id = id
        self.chat_id = chat_id
        self.is_active = is_active
