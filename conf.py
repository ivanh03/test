# coding: utf-8

import logging
import redis as rds


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger('app')


CACHE = rds.Redis('localhost', db=0)
