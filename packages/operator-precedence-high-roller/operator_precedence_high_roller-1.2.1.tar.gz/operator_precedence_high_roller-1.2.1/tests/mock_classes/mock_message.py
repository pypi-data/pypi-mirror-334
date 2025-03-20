from tests.mock_classes.mock_message_attributes.mock_author import MockAuthor
from tests.mock_classes.mock_message_attributes.mock_channel import MockChannel

class MockMessage:
    def __init__(self, author: MockAuthor, channel: MockChannel, content: str):
        self.author = author
        self.channel = channel
        self.content = content