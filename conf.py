# coding: utf-8

import os
import logging
import redis as rds


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger('app')


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

CACHE = rds.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
