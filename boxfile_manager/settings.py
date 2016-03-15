from re import compile

RECENT_BOX_AMOUNT = 3

BOX_NAME = 'hypernode'
BASE_URL = 'http://vagrant.hypernode.com/'
BOX_METADATA = {'name': BOX_NAME, 'description': 'A Hypernode in a box', 'versions': list()}

PROVIDER_AND_VERSION_PATTERN = compile(r'^hypernode\.([^.]*)\.release-(.*)\.box$')
