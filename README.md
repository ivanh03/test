Required steps for the service deploy

```bash
git clone https://github.com/ivanh03/test.git && cd test
mkvirtualenv test
pip install -r requirements.txt
export ROOT_DIR=`pwd`
# needs to setup redis server
export REDIS_HOST='HOST' # optional, default value is localhost
export REDIS_PORT='PORT' # optional, default value is 6379
uwsgi app.ini
```

Tested on Ubuntu 16.04, Redis 3.2.1
