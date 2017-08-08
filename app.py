# coding: utf-8
from urllib import quote, unquote
import requests
import conf

cache = conf.CACHE
logger = conf.LOGGER


def get_params(query):
    """
    Try to create dict from GET params that got server
    Args:
        query: server query - str
    Returns:
        dict with params or False if something went wrong
    """
    new_params = {}
    try:
        params = dict([part.split('=') for part in query.split('&')])
        for key in params:
            new_key = unquote(key).decode('utf-8')
            new_params[new_key] = unquote(params[key])
        return new_params
    except ValueError:
        return False


def wait_message(key):
    """Listen channel for `request done` messages """

    logger.info('Start listen channel: ' + 'pending-' + quote(key))
    pubsub = cache.pubsub()
    pubsub.subscribe(['pending-' + quote(key)])
    for item in pubsub.listen():
        value = item['data']
        # Prevent service init message handling
        if value != 1:
            logger.info('Channel message received: %s | %s' % (key, value))
            return value


def from_cache(env, start_response):
    """Caching view function"""

    params = get_params(env['QUERY_STRING'])

    start_response('200', [('Content-type', 'application/json')])

    if not params:
        return ['Wrong query format']

    key = params.get('key')

    if not key:
        return ['Wrong key parameter']

    # Check for executing request with the same key
    value = cache.get(key)

    # If key has a `pending` state we start to listen `done` event for it
    if value == 'pending':
        result = wait_message(key)
    elif value is not None:
        result = value
        logger.info('Got value from cache: ' + value)
    else:
        cache.setex(key, 'pending', 60)
        query = 'https://vast-eyrie-4711.herokuapp.com/?' + env['QUERY_STRING']
        response = requests.get(query)
        # response = requests.get('http://localhost:8080/' + env['QUERY_STRING'])
        logger.info('Got response from server: ' + response.text)
        if response.text != 'error':
            # Cache non-error response
            cache.setex(key, response.text, 24*60*60)
        else:
            # Else remove pending status
            cache.delete(key)
        result = response.text

    # publish `done` message when response received
    cache.publish('pending-' + quote(key), result)
    return [result]  if isinstance(result, str) else result.encode('utf8')


def application(env, start_response):
    """WSGI application entry point"""

    query_path = env['PATH_INFO']

    if query_path == '/from_cache':
        return from_cache(env, start_response)

    start_response('404 Not Found', [('Content-type', 'application/json')])
    return ['']
