from datetime import date, datetime
from werkzeug.datastructures.file_storage import FileStorage


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class User:
    def __init__(self):
        self.login_credentials = None
        self.expires = date.today()  # the end of subscription plan

    @property
    def active_subscription(self) -> bool:
        """
        Does user have active subscription.
        :return: True if user subscribed, False otherwise
        """
        return date.today() < self.expires

    def login(self) -> None:
        """
        Login user.
        """
        pass

    def activate(self) -> None:
        """
        Purchase subscription.
        """
        pass


class Visitor(User):
    active = {}  # all instances

    def __init__(self):
        super().__init__()
        self.token = self._create_token()
        self.active[self.token] = self

    @staticmethod
    def get(token: str):
        """
        Find a visitor or create one.
        :param token: unique visitor identifier
        :return: Visitor instance
        """
        if token:
            if token in Visitor.active:
                return Visitor.active[token]
        return Visitor()

    def files(self) -> list['File']:
        """
        :return: all files that associated with this visitor
        """
        return [f.filename for f in storage.files if f.owner == self]

    def _create_token(self) -> str:
        """
        Token to store with cookies.
        :return: randomly generated string
        """
        pass


@singleton
class Storage:
    def __init__(self, capacity: int = 1000, hold_for: int = 1):
        self.files = []
        self.capacity = capacity
        self.hold_for = hold_for

    @property
    def size(self) -> float:
        """
        :return: size of all files in MB
        """
        return sum([f.size for f in self.files])

    def save(self, file: FileStorage) -> None:
        """
        Save file.
        :param file: FileStorage object from Flask
        """
        if file.__sizeof__() + self.size > self.capacity:
            raise Exception('Storage is full')
        self.files.append(File(file.filename, file.__sizeof__()))
        # file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))

    def delete_old(self) -> None:
        """
        Delete old files.
        """
        pass


class File:
    def __init__(self, filename: str, size: float, owner_token: str):
        """
        :param filename: ex. name.wav
        :param size: file size in MB
        :param owner_token: token string to identify owner
        """
        assert '.' in filename, 'Wrong filename'
        self.filename = filename
        self.name, self.format = filename.split('.')
        self.size = size
        self.owner = Visitor.get(owner_token)
        self.loaded = datetime.now()
        self.phrases = []

    def extract_phrases(self) -> None:
        """
        Generate phrases from file
        :return:
        """
        pass


class Phrase:
    def __init__(self, start: float, end: float, text: str, conf: float, external_tone: float = 0):
        self.start, self.end, self.text, self.conf, self._external_tone = start, end, text, conf, external_tone

    @property
    def tone(self, weight_internal: float = 1, weight_external: float = 0) -> float:
        """
        General estimation if the phrase needs to be bleeped.
        :param weight_internal:
        :param weight_external:
        :return: float from 0 to 1 probability alike
        """
        return self._internal_tone * weight_internal + self._external_tone * weight_external

    @property
    def _internal_tone(self) -> float:
        """
        Estimate if the phrase needs to be bleeped based only on instance information.
        :return: float from 0 to 1
        """
        pass


storage = Storage()
