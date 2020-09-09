import sqlalchemy
from databases import Database
from starlette.config import Config

class DBWrapper:
    database = None
    table_cards = None
    config = None
    DATABASE_URL = None

    def __init__(self):
        super().__init__()
        self.config = Config('.env')
        self.DATABASE_URL = self.config('DATABASE_URL')
        self.database = Database(self.DATABASE_URL)
        
    async def initDB(self):
        # Database table definitions.
        metadata = sqlalchemy.MetaData()
        self.table_cards = sqlalchemy.Table(
            "cards",
            metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("position", sqlalchemy.Integer),
            sqlalchemy.Column("title", sqlalchemy.String),
            sqlalchemy.Column("thumbnail", sqlalchemy.String),
            sqlalchemy.Column("slug_type", sqlalchemy.String),
            sqlite_autoincrement = True
        )

        self.database = Database(self.DATABASE_URL)
        await self.database.connect()

        print("Database connected")

    async def fetchCards(self):
        query = self.table_cards.select()
        return await self.database.fetch_all(query=query)

    async def fetchCardByPosition(self, position):
        query = "SELECT * FROM cards WHERE position = :position"
        return await self.database.fetch_one(query=query, values={ 'position' : position } )

    async def createCard(self, values):
        query = self.table_cards.insert()
        await self.database.execute(query=query, values=values)

    async def deleteCard(self, position):
        # query = self.table_cards.delete().where('position' == position)
        query = "DELETE FROM cards WHERE position = :position"
        await self.database.execute(query=query, values = { "position" : position})

    async def updateCard(self, id, position, title, thumbnail):
        query = "Update cards set position=:position, title=:title, thumbnail=:thumbnail WHERE id=:id"
        await self.database.execute(query=query, values = { "title" : title, "thumbnail" : thumbnail, "position" : position, "id" : id}) 

    async def disconnect(self):
        await self.database.disconnect()
        print("Database Disconnected")
