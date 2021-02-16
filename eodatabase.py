from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Character(db.Model):
    """
    A class used to represent an EOServ Character database entry
    """
    __tablename__ = 'characters'
    name = db.Column(db.String(16), primary_key=True)
    account = db.Column(db.String(16))
    title = db.Column(db.String(32))
    home = db.Column(db.String(32))
    partner = db.Column(db.String(16))
    admin = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    race = db.Column(db.Integer, nullable=False)
    hairstyle = db.Column(db.Integer, nullable=False)
    haircolor = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.Integer, nullable=False)
    str = db.Column(db.Integer, nullable=False)
    int = db.Column(db.Integer, nullable=False)
    wis = db.Column(db.Integer, nullable=False)
    agi = db.Column(db.Integer, nullable=False)
    con = db.Column(db.Integer, nullable=False)
    cha = db.Column(db.Integer, nullable=False)
    karma = db.Column(db.Integer, nullable=False)
    goldbank = db.Column(db.Integer, nullable=False)
    usage = db.Column(db.Integer, nullable=False)
    inventory = db.Column(db.Text)
    bank = db.Column(db.Text)
    paperdoll = db.Column(db.Text)
    spells = db.Column(db.Text)
    guild = db.Column(db.String(3))
    guild_rank = db.Column(db.Integer)
    guild_rank_string = db.Column(db.String(16))
    slots = [
        "boots",
        "accessory",
        "gloves",
        "belt",
        "armor",
        "necklace",
        "hat",
        "shield",
        "weapon",
        "ring_1",
        "ring_2",
        "armlet_1",
        "armlet_2",
        "bracer_1",
        "bracer_2"
    ]

    def __repr__(self):
        return '<Character %r>' % self.name

    def __unserialize_paperdoll(self) -> dict:
        values = self.paperdoll[:-1].split(',')
        return {name: int(values[slot]) for slot, name in enumerate(self.slots)}

    @staticmethod
    def __unserialize_pairs(text) -> dict:
        values = text[:-1].split(',')
        return {values[i]: int(values[i + 1]) for i in range(0, len(values), 2)} if text else {}

    def serialize(self) -> dict:
        """
        :return: a dictionary representing the Character
        """
        return {
            "name": self.name,
            "title": self.title,
            "home": self.home,
            "partner": self.partner,
            "admin": self.admin,
            "gender": self.gender,
            "race": self.race,
            "hairstyle": self.hairstyle,
            "haircolor": self.haircolor,
            "level": self.level,
            "exp": self.exp,
            "str": self.str,
            "int": self.int,
            "wis": self.wis,
            "agi": self.agi,
            "con": self.con,
            "cha": self.cha,
            "karma": self.karma,
            "goldbank": self.goldbank,
            "usage": self.usage,
            "guild": self.guild,
            "guild_rank": self.guild_rank_string,
            "guild_rank_id": self.guild_rank,
            "paperdoll": self.__unserialize_paperdoll(),
            "inventory": self.__unserialize_pairs(self.inventory),
            "bank": self.__unserialize_pairs(self.bank),
            "spells": self.__unserialize_pairs(self.spells)
        }


class Guild(db.Model):
    """
    A class used to represent an EOServ Guild database entry.
    """
    __tablename__ = 'guilds'
    tag = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(32), unique=True),
    description = db.Column(db.Text)
    created = db.Column(db.Integer)
    ranks = db.Column(db.Text)
    bank = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Guild %r>' % self.tag

    def serialize(self) -> dict:
        """
        :return: a dictionary representing the guild
        """
        return {
            "tag": self.tag,
            "name": self.name,
            "description": self.description,
            "created": self.created,
            "ranks": self.ranks,
            "bank": self.bank,
        }
