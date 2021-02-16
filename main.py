import eolib

from argparse import ArgumentParser
from eodatabase import Character, Guild, db

from flask_api import FlaskAPI, exceptions

app = FlaskAPI(__name__)


@app.route('/api/classes', methods=['GET'])
def classes():
    try:
        return {"results": eolib.read_ecf(app.config['ECF'])}
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/items', methods=['GET'])
def items():
    try:
        return {"results": eolib.read_eif(app.config['EIF'])}
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/spells', methods=['GET'])
def spells():
    try:
        return {"results": eolib.read_esf(app.config['ESF'])}
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/npcs', methods=['GET'])
def npcs():
    try:
        return {"results": eolib.read_enf(app.config['ENF'])}
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/drops', methods=['GET'])
def drops():
    try:
        return eolib.read_drops(app.config['DROPS'])
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/skills', methods=['GET'])
def skills():
    try:
        return eolib.read_skills(app.config['SKILLS'])
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/shops', methods=['GET'])
def shops():
    try:
        return eolib.read_shops(app.config['SHOPS'])
    except FileNotFoundError:
        raise exceptions.NotFound


@app.route('/api/characters/<name>', methods=['GET'])
def character(name):
    result = Character.query.filter(Character.name == name.lower()).one_or_none()
    if result is None:
        raise exceptions.NotFound
    return result.serialize()


@app.route('/api/guilds/<tag>', methods=['GET'])
def guild(tag):
    result = Guild.query.filter(Guild.name == tag).one_or_none()
    if result is None:
        raise exceptions.NotFound
    return result.serialize()


@app.route('/api/guilds/<tag>/characters', methods=['GET'])
def guild_members(tag):
    result = Guild.query.filter(Guild.tag == tag).one_or_none()
    if result is None:
        raise exceptions.NotFound
    result = Character.query.filter(Character.guild == result.guild)
    return {"members": [i.serialize for i in result]}


if __name__ == '__main__':
    parser = ArgumentParser(description="EOServ REST API")
    parser.add_argument("--ecf", help="path to EIF pub")
    parser.add_argument("--eif", help="path to EIF pub")
    parser.add_argument("--esf", help="path to ESF pub")
    parser.add_argument("--enf", help="path to ENF pub")
    parser.add_argument("--drops", help="path to shops config")
    parser.add_argument("--skills", help="path to skills config")
    parser.add_argument("--shops", help="path to shops config")
    parser.add_argument("--database", help="database location")
    args = parser.parse_args()

    app.config['ECF'] = args.ecf if args.ecf else "data/pub/dat001.ecf"
    app.config['EIF'] = args.eif if args.eif else "data/pub/dat001.eif"
    app.config['ESF'] = args.esf if args.esf else "data/pub/dsl001.esf"
    app.config['ENF'] = args.enf if args.enf else "data/pub/dtn001.enf"
    app.config['DROPS'] = args.drops if args.drops else "data/drops.ini"
    app.config['SKILLS'] = args.skills if args.skills else "data/skills.ini"
    app.config['SHOPS'] = args.shops if args.shops else "data/shops.ini"
    app.config['SQLALCHEMY_DATABASE_URI'] = args.database if args.database else 'sqlite:///database.sdb'

    db.init_app(app)
    app.run(debug=True)
