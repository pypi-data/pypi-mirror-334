from discord.file import File

class MockChannel:
    def __init__(self, name: str):
        self.name = name
    
    async def send(self, content: str = None, file: File = None):
        if content != None:
            print(content)
        if file != None:
            print(file.filename)