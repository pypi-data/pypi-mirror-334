import pymongo
from conexao.config import get_config
from conexao.ssh import start_forward


def create_client(profile_name: str) -> pymongo.MongoClient:
    '''Returns a Mongo Client for a configured profile.'''
    profile = get_config()['profiles'][profile_name]

    if ssh := profile.get('ssh'):
        socket = start_forward(ssh['host'], ssh['forwards'])
        profile['mongo']['host'] = profile['mongo']['host'].format(socket=socket)

    return pymongo.MongoClient(
        **profile['mongo'],
        compressors='zlib',
        zlibCompressionLevel=9,
    )
