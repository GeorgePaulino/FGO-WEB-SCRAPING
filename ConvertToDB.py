from email.encoders import encode_noop
import sqlite3
from sqlite3 import Error
import json
import os

comm_create = ''
with open('Command_Create.sql', encoding='utf8') as file:
    comm_create = file.read()
comm = ''
with open('Command_Add.sql', encoding='utf8') as file:
    comm = file.read()

def create_connection(db_file):
    conn = None
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute(comm_create)
        for f in os.listdir('./datas'):
            card = json.load(open('./datas/{}'.format(f), encoding='utf-8'))
            card_comm = tuple(card.values())
            c = conn.cursor()
            c.execute(comm, card_comm)
            print('{} {}'.format(card['Id'], card["Name"]))
        #conn.commit()
        

if __name__ == '__main__':
    create_connection(r"cards.db")