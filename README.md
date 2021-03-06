# vagrant-catalog-generator

Generate catalog.json files for Vagrant boxes.


## Usage

Put your boxfiles in a directory in the following format:

```
<BOX_NAME>.<PROVIDER>.release-<RELEASE_NUMBER>.box
```

Example:
```
hypernode.vagrant.release-2638.box
hypernode.vagrant.release-2639.box
hypernode.vagrant.release-2640.box
```


Cleaning up old releases (optional)
```
python bin/prune_boxfiles.py --directory /dir/to/your/boxfiles --amount 2
```

Generating a catalog.json file
```
python bin/generate_catalog.py --directory /dir/to/your/boxfiles --base-url https://vagrant.example.com --description "A Hypernode in a box" --name hypernode
```

Result:
```
catalog.json
hypernode.vagrant.release-2641.box
hypernode.vagrant.release-2641.box.sha256
hypernode.vagrant.release-2642.box
hypernode.vagrant.release-2642.box.sha256
```

Catalog:
```
{
  "name": "hypernode",
  "description": "A Hypernode in a box",
  "versions": [
    {
      "version": "2641",
      "providers": [
        {
          "url": "https://vagrant.example.com/hypernode.vagrant.release-2641.box",
          "checksum_type": "sha256",
          "checksum": "00e3261a6e0d79c329445acd540fb2b07187a0dcf6017065c8814010283ac67f",
          "name": "vagrant"
        }
      ]
    },
    {
      "version": "2642",
      "providers": [
        {
          "url": "https://vagrant.example.com/hypernode.vagrant.release-2642.box",
          "checksum_type": "sha256",
          "checksum": "00e3261a6e0d79c329445acd540fb2b07187a0dcf6017065c8814010283ac67f",
          "name": "vagrant"
        }
      ]
    }
  ]
}
```


## Development

```
# Clone repo
git clone git@github.com:ByteInternet/vagrant-catalog-generator.git
cd vagrant-catalog-generator

# Create virtualenv
mkvirtualenv -p python3 -a $(pwd) vagrant-catalog-generator
echo "export PYTHONPATH=$(pwd)" >> $VIRTUAL_ENV/bin/postactivate
workon vagrant-catalog-generator

# Install dependencies
pip install -U pip distribute
pip install -r requirements/development.txt
```

###Running tests
```
./runtests.sh -1
```
