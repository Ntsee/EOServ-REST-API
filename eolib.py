from configparser import ConfigParser
from dataclasses import dataclass
from enum import Enum


class EOReader:
    """A class used to read an Endless Online encoded binary file."""
    ONE_BYTE_MAX = 253
    TWO_BYTE_MAX = int(pow(ONE_BYTE_MAX, 2))
    THREE_BYTE_MAX = int(pow(ONE_BYTE_MAX, 3))

    @staticmethod
    def number(b1: int, b2: int = 254, b3: int = 254, b4: int = 254):
        """
        Decodes a series of bytes into a single value.
        :param b1: the first byte to decode
        :param b2: the second byte to decode (optional)
        :param b3: the third byte to decode (optional)
        :param b4: the fourth byte to decode (optional
        :return: the value represented by the given series of bytes
        """
        b1 = 1 if b1 == 254 else b1
        b2 = 1 if b2 == 254 else b2
        b3 = 1 if b3 == 254 else b3
        b4 = 1 if b4 == 254 else b4

        b1 = 128 if b1 == 0 else b1
        b2 = 128 if b2 == 0 else b2
        b3 = 128 if b3 == 0 else b3
        b4 = 128 if b4 == 0 else b4

        b1 -= 1
        b2 -= 1
        b3 -= 1
        b4 -= 1

        return (b4 * EOReader.THREE_BYTE_MAX) + (b3 * EOReader.TWO_BYTE_MAX) + (b2 * EOReader.ONE_BYTE_MAX) + b1

    def __init__(self, path: str):
        self.file = open(path, "rb")
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read_byte(self) -> int:
        """
        :return: the value of the next byte
        """
        return self.file.read(1)[0]

    def read_char(self) -> int:
        """
        :return: the decoded value of the next byte
        """
        return EOReader.number(self.read_byte())

    def read_short(self) -> int:
        """
        :return: the decoded value of the next 2 bytes
        """
        return EOReader.number(self.read_byte(), self.read_byte())

    def read_three(self) -> int:
        """
        :return: the decoded value of the next 3 bytes
        """
        return EOReader.number(self.read_byte(), self.read_byte(), self.read_byte())

    def read_int(self) -> int:
        """
        :return:  the decoded value of the next 4 bytes
        """
        return EOReader.number(self.read_byte(), self.read_byte(), self.read_byte(), self.read_byte())

    def read_fixed_string(self, length: int) -> str:
        """
        :param length: the length of the string to read
        :return: the ascii representation of length bytes
        """
        return self.file.read(length).decode("ascii")

    def read_break_string(self):
        """
        :return: the ascii representation of the bytes up to 0xFF
        """
        data = []
        b = self.read_byte()
        while b != 0xFF:
            data.append(b)
            b = self.read_byte()
        return bytes(data).decode("ascii")

    def skip(self, amount: int):
        self.file.read(amount)


class EIFType(int, Enum):
    Static = 0
    Money = 2
    Heal = 3
    Teleport = 4
    Spell = 5
    EXPReward = 6
    StatReward = 7
    SkillReward = 8
    Key = 9
    Weapon = 10
    Shield = 11
    Armor = 12
    Hat = 13
    Boots = 14
    Gloves = 15
    Accessory = 16
    Belt = 17
    Necklace = 18
    Ring = 19
    Armlet = 20
    Bracer = 21
    Beer = 22
    EffectPotion = 23
    HairDye = 24
    CureCurse = 25


class EIFSubType(int, Enum):
    Normal = 0
    Range = 1
    Arrows = 2
    Wings = 3
    TwoHanded = 4


class EIFSpecial(int, Enum):
    Common = 0
    Uncommon = 1
    Rare = 2
    Rarest = 3
    Lore = 4
    Cursed = 5
    Unknown1 = 6,
    Unknown2 = 7


class EIFSize(int, Enum):
    Size1x1 = 0
    Size1x2 = 1
    Size1x3 = 2
    Size1x4 = 3
    Size2x1 = 4
    Size2x2 = 5
    Size2x3 = 6
    Size2x4 = 7


@dataclass
class EIF:
    """A class used to represent a single entry in an Endless Online items pub file."""
    id: int
    name: str
    graphic: int
    type: EIFType
    subtype: EIFSubType
    special: EIFSpecial
    health: int
    mana: int
    min_damage: int
    max_damage: int
    accuracy: int
    evade: int
    armor: int
    strength: int
    intelligence: int
    wisdom: int
    agility: int
    constitution: int
    charisma: int
    spec1: int
    spec2: int
    spec3: int
    level_requirement: int
    class_requirement: int
    strength_requirement: int
    intelligence_requirement: int
    wisdom_requirement: int
    agility_requirement: int
    constitution_requirement: int
    charisma_requirement: int
    element: int
    element_power: int
    weight: int
    size: EIFSize

    def __init__(self, reader: EOReader = None):
        if reader:
            self.name = reader.read_fixed_string(reader.read_char())
            self.graphic = reader.read_short()
            self.type = EIFType(reader.read_char())
            self.subtype = EIFSubType(reader.read_char())
            self.special = EIFSpecial(reader.read_char())
            self.health = reader.read_short()
            self.mana = reader.read_short()
            self.min_damage = reader.read_short()
            self.max_damage = reader.read_short()
            self.accuracy = reader.read_short()
            self.evade = reader.read_short()
            self.armor = reader.read_short()
            reader.skip(1)
            self.strength = reader.read_char()
            self.intelligence = reader.read_char()
            self.wisdom = reader.read_char()
            self.agility = reader.read_char()
            self.constitution = reader.read_char()
            self.charisma = reader.read_char()
            reader.skip(6)
            self.spec1 = reader.read_three()
            self.spec2 = reader.read_char()
            self.spec3 = reader.read_char()
            self.level_requirement = reader.read_short()
            self.class_requirement = reader.read_short()
            self.strength_requirement = reader.read_short()
            self.intelligence_requirement = reader.read_short()
            self.wisdom_requirement = reader.read_short()
            self.agility_requirement = reader.read_short()
            self.constitution_requirement = reader.read_short()
            self.charisma_requirement = reader.read_short()
            self.element = reader.read_char()
            self.element_power = reader.read_char()
            self.weight = reader.read_char()
            reader.skip(1)
            self.size = EIFSize(reader.read_char())


class ENFType(int, Enum):
    NPC = 0
    Passive = 1
    Aggressive = 2
    Pet = 3
    Unknown1 = 4
    Unknown2 = 5
    Shop = 6
    Inn = 7
    Unknown3 = 8
    Bank = 9
    Barber = 10
    Guild = 11
    Priest = 12
    Law = 13
    Skills = 14
    Quest = 15
    Unknown4 = 16
    Unknown5 = 17
    Unknown6 = 18
    Unknown7 = 19
    Unknown8 = 20


@dataclass
class ENF:
    """A class used to represent a single entry in an Endless Online NPC pub file."""
    id: int
    name: str
    graphic: int
    boss: bool
    child: bool
    type: ENFType
    vendor: int
    health: int
    min_damage: int
    max_damage: int
    accuracy: int
    evade: int
    armor: int
    element_weak: int
    element_weak_power: int
    experience: int

    def __init__(self, reader: EOReader = None):
        if reader:
            self.name = reader.read_fixed_string(reader.read_char())
            self.graphic = reader.read_short()
            reader.skip(1)
            self.boss = reader.read_short() > 0
            self.child = reader.read_short() > 0
            self.type = ENFType(reader.read_short())
            self.vendor = reader.read_short()
            self.health = reader.read_three()
            reader.skip(2)
            self.min_damage = reader.read_short()
            self.max_damage = reader.read_short()
            self.accuracy = reader.read_short()
            self.evade = reader.read_short()
            self.armor = reader.read_short()
            reader.skip(5)
            self.element_weak = reader.read_short()
            self.element_weak_power = reader.read_short()
            reader.skip(1)
            self.experience = reader.read_three()


class ESFType(int, Enum):
    Heal = 0
    Damage = 1
    Bard = 2


class ESFTargetRestrict(int, Enum):
    NPC = 0
    Friendly = 1
    Opponent = 2


class ESFTargetType(int, Enum):
    Normal = 0
    Self = 1
    Unknown = 2
    Group = 3


@dataclass
class ESF:
    """A class used to represent a single entry in an Endless Online spells pub file."""
    id: int
    name: str
    shout: str
    icon: int
    graphic: int
    mana: int
    stamina: int
    cast_time: int
    type: ESFType
    element: int
    element_power: int
    target_restrict: ESFTargetRestrict
    target_type: ESFTargetType
    min_damage: int
    max_damage: int
    heal: int

    def __init__(self, reader: EOReader = None):
        if reader:
            name_length = reader.read_char()
            shout_length = reader.read_char()
            self.name = reader.read_fixed_string(name_length)
            self.shout = reader.read_fixed_string(shout_length)
            self.icon = reader.read_short()
            self.graphic = reader.read_short()
            self.mana = reader.read_short()
            self.stamina = reader.read_short()
            self.cast_time = reader.read_char()
            reader.skip(2)
            self.type = ESFType(reader.read_three())
            self.element = reader.read_char()
            self.element_power = reader.read_short()
            self.target_restrict = ESFTargetRestrict(reader.read_char())
            self.target_type = ESFTargetType(reader.read_char())
            reader.skip(4)
            self.min_damage = reader.read_short()
            self.max_damage = reader.read_short()
            self.accuracy = reader.read_short()
            reader.skip(5)
            self.heal = reader.read_short()
            reader.skip(15)


@dataclass
class ECF:
    """A class used to represent a single entry in an Endless Online class pub file."""
    id: int
    name: str
    parent: int
    stat_table: int
    strength: int
    intelligence: int
    wisdom: int
    agility: int
    constitution: int
    charisma: int

    def __init__(self, reader: EOReader = None):
        if reader:
            self.name = reader.read_fixed_string(reader.read_char())
            self.parent = reader.read_char()
            self.stat_table = reader.read_char()
            self.strength = reader.read_short()
            self.intelligence = reader.read_short()
            self.wisdom = reader.read_short()
            self.agility = reader.read_short()
            self.constitution = reader.read_short()
            self.charisma = reader.read_short()


def __read_pub(pub: type, extension: str, file: str) -> list:
    """
    Read an Endless Online pub file.
    :param pub: a class representing a single entry in a pub file
    :param extension: the file magic used to validated the pub file type
    :param file: the path to the pub file
    :return: a list of pub entries
    """
    with EOReader(file) as reader:
        magic = reader.read_fixed_string(3)
        if extension != magic:
            raise ValueError(magic, "is not valid", extension, "file")
        reader.read_int()  # rid
        total = reader.read_short()
        reader.skip(1)
        entries = []
        for i in range(total - 1):
            entry = pub(reader)
            entry.id = i + 1
            entries.append(entry)
        return entries


def read_eif(file: str):
    """
    Reads an Endless Online items file
    :param file: the path to the eif file
    :return: a list of EIF entries
    """
    return __read_pub(EIF, "EIF", file)


def read_enf(file: str) -> list[ENF]:
    """
    Reads an Endless Online NPCs file
    :param file: the path to the enf file
    :return: a list of ENF entries
    """
    return __read_pub(ENF, "ENF", file)


def read_esf(file: str) -> list[ESF]:
    """
    Reads an Endless Online spells file
    :param file: the path to the esf file
    :return: a list of ESF entries
    """
    return __read_pub(ESF, "ESF", file)


def read_ecf(file: str) -> list[ECF]:
    """
    Reads an Endless Online classes file
    :param file: the path to the ecf file
    :return: a list of ECF entries
    """
    return __read_pub(ECF, "ECF", file)


def __read_ini(file: str) -> list[tuple[str, str]]:
    """
    Reads an EOServ ini file.
    :param file: the path to the ini file
    :return: the key value pairs of the file
    """
    with open(file, 'r') as f:
        config_string = '[default]\n' + f.read()
        config = ConfigParser()
        config.read_string(config_string)
        return config.items('default')


def read_drops(file: str) -> dict:
    """
    Reads an EOServ drops.ini file
    :param file: the path to the drops.ini file
    :return: a dictionary of the drops.ini file where the keys are the NPC ids and the values are a list of drops
    """
    table = {}
    entries = __read_ini(file)
    for key, value in entries:
        drops = value.split(',')
        table[key] = []
        for i in range(0, len(drops), 4):
            item_id, min_amount, max_amount, chance = tuple(drops[i:i + 4])
            table[key].append({
                'id': int(item_id),
                'min_amount': int(min_amount),
                'max_amount': int(max_amount),
                'chance': float(chance)
            })
    return table


def read_shops(file: str) -> dict:
    """
    Reads an EOServ shops.ini file
    :param file: the path to the shops.ini file
    :return: a dictionary of the shops.ini file where the keys are npc/vendor ids and the values are the associated shop
    """
    def parse_name(data: str) -> str:
        return data

    def parse_trade(data: str) -> list[dict]:
        trades = []
        data = data.split(',')
        for i in range(0, len(data), 3):
            item_id, buy_price, sell_price = tuple(data[i:i+3])
            trades.append({
                'id': int(item_id),
                'buy': int(buy_price),
                'sell': int(sell_price),
            })
        return trades

    def parse_craft(data: str) -> list[dict]:
        crafts = []
        data = data.split(',')
        for i in range(0, len(data), 9):
            item_id = data[i]
            crafts.append({
                'id': int(item_id),
                'ingredients': [{
                    'id': int(data[i+j]),
                    'amount': int(data[i+j+1])} for j in range(1, 9, 2) if int(data[i+j]) > 0]
            })
        return crafts

    read_shops.parsers = {'name': parse_name, 'trade': parse_trade, 'craft': parse_craft}

    table = {}
    entries = __read_ini(file)
    for key, info in entries:
        if key == 'version':
            continue
        npc_id, group = key.split('.')
        if npc_id not in table:
            table[npc_id] = {}
        table[npc_id][group] = read_shops.parsers[group](info)
    return table


def read_skills(file: str) -> dict:
    """
    Reads an EOServ skills.ini file
    :param file: the path to the skills.ini file
    :return: a dictionary of the skills.ini file where keys are npc ids and the values are the skills offered
    """
    def _parse_name(data: str) -> str:
        return data

    def parse_learn(data: str) -> list[dict]:
        skills = []
        data = data.split(',')
        for i in range(0, len(data), 14):
            spell_id, cost, level, clas = data[i:i+4]
            stren, intl, wis, agi, con, cha = data[i+8:i+14]
            skills.append({
                'id': int(spell_id),
                'cost': int(cost),
                'level': int(level),
                'class': int(clas),
                'str_req': int(stren),
                'int_req': int(intl),
                'wis_req': int(wis),
                'agi_req': int(agi),
                'con_req': int(con),
                'cha_req': int(cha),
                'spell_req': [int(data[i+j]) for j in range(4, 4, 1) if int(data[i+j]) > 0]

            })
        return skills

    read_skills.parsers = {'name': _parse_name, 'learn': parse_learn}

    table = {}
    entries = __read_ini(file)
    for key, info in entries:
        if key == 'version':
            continue
        npc_id, group = key.split('.')
        if npc_id not in table:
            table[npc_id] = {}
        table[npc_id][group] = read_skills.parsers[group](info)
    return table
