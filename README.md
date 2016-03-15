# hypernode-boxfile-manager

Tool to generate catalog.json files for the hypernode-vagrant box and the intermediate development box we use internally.

## Development

```
# Clone repo
git clone git@github.com:ByteInternet/hypernode-boxfile-manager.git
cd hypernode-boxfile-manager

# Create virtualenv
mkvirtualenv -a $(pwd) hypernode-boxfile-manager
echo "export PYTHONPATH=$(pwd)" >> $VIRTUAL_ENV/bin/postactivate
workon hypernode-boxfile-manager

# Install dependencies
pip install -U pip distribute
pip install -r requirements/development.txt
```

###Running tests
```
./runtests.sh -1
```
