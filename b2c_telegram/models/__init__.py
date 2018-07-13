# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from threading import Thread

import psycopg2
from odoo import sql_db
from odoo.service import db, server
from odoo.tools import config
from telegram.ext import *

from . import res_partner
from . import b2c_base, b2c_bot
from .b2c_bot import B2CBotTelegram

_logger = logging.getLogger(__name__)


class B2CBotTelegramThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.start_bots()

    def _has_b2c_base(self, cr):
        cr.execute("SELECT 1 FROM pg_tables WHERE tablename=%s",
                   ('ir_module_module',))
        if not cr.fetchone():
            return False
        cr.execute(
            "SELECT 1 FROM ir_module_module WHERE name=%s AND state=%s",
            ('b2c_base', 'installed')
        )
        return cr.fetchone()

    def get_db_names(self):
        if config['db_name']:
            db_names = config['db_name'].split(',')
        else:
            db_names = db.exp_list(True)
        return db_names

    def get_active_bots(self, cr):
        cr.execute(
               """SELECT token
                  FROM b2c_base
                  WHERE active = 't' AND provider = 'telegram';"""
            )
        return cr.fetchall()

    def start_bots(self):
        for db_name in self.get_db_names():
            connection_info = sql_db.connection_info_for(db_name)[1]
            conn = psycopg2.connect(**connection_info)
            cr = conn.cursor()
            if not self._has_b2c_base(cr):
                return False
            for bot_raw in self.get_active_bots(cr):
                bot = B2CBotTelegram(bot_raw[0])
                bot.start_polling()
            cr.close()
            conn.close()

    def stop(self):
        for db_name in self.get_db_names():
            connection_info = sql_db.connection_info_for(db_name)[1]
            conn = psycopg2.connect(**connection_info)
            cr = conn.cursor()
            for bot_raw in self.get_active_bots(cr):
                bot = B2CBotTelegram(bot_raw[0])
                bot.stop_polling()
            cr.close()
            conn.close()


b2c_telegram_thread = None

orig_prefork_start = server.PreforkServer.start
orig_prefork_stop = server.PreforkServer.stop
orig_threaded_start = server.ThreadedServer.start
orig_threaded_stop = server.ThreadedServer.stop


def prefork_start(server, *args, **kwargs):
    global b2c_telegram_thread
    res = orig_prefork_start(server, *args, **kwargs)
    if not config['stop_after_init']:
        _logger.info("Starting Telegram Bot of B2C (in prefork server)")
        b2c_telegram_thread = B2CBotTelegramThread()
        b2c_telegram_thread.start()
    return res


def prefork_stop(server, graceful=True):
    global b2c_telegram_thread
    if b2c_telegram_thread:
        b2c_telegram_thread.stop()
    res = orig_prefork_stop(server, graceful)
    if b2c_telegram_thread:
        b2c_telegram_thread.join()
        b2c_telegram_thread = None
    return res


def threaded_start(server, *args, **kwargs):
    global b2c_telegram_thread
    res = orig_threaded_start(server, *args, **kwargs)
    if not config['stop_after_init']:
        _logger.info("starting Telegram of B2C (in threaded server)")
        b2c_telegram_thread = B2CBotTelegramThread()
        b2c_telegram_thread
        b2c_telegram_thread.start()
    return res


def threaded_stop(server):
    global b2c_telegram_thread
    if b2c_telegram_thread:
        b2c_telegram_thread.stop()
    res = orig_threaded_stop(server)
    if b2c_telegram_thread:
        b2c_telegram_thread.join()
        b2c_telegram_thread = None
    return res


server.PreforkServer.start = prefork_start
server.PreforkServer.stop = prefork_stop
server.ThreadedServer.start = threaded_start
server.ThreadedServer.stop = threaded_stop
