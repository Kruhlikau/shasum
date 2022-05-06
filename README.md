# Python script for calculating hash sum
____
**First of all, need to create a virtual environment. 
In general, the command will look like this:**

`$ python3 -m venv env`

Here `env` - name of `virtualenv`

**The next step is to activate the virtual environment:**

`$ source env/bin/activate`

**And update the `pip` package manager:**

`-m pip install --upgrade pip`

**The last step is to install `requirements.txt`:**

`pip install -r requirements.txt`

**To start using the script, enter the following command in the console:**
**`python3 main.py [-h] [-f FILES] [-a ALGORITHM] [-s] [-c]`**

**where**:
* ###  -h, --help: show this help message and exit
* ###  -f FILES, --files FILES(With no FILE, or when FILE is -, read standard input.): files for hash calculation
* ### -a ALGORITHM, --algorithm ALGORITHM - hashing algorithms for a files:
    **md4, sha512, sha512_224, sha224, shake_128, sha384, md5, sha3_256, md5-sha1, sha3_224, sha512_256, sm3, sha3_384, blake2s,sha3_512, sha1, sha256, ripemd160, whirlpool, blake2b, shake_256**
* ### -s, --save: safe result to db
* ### -c, --check: hash diff comparison

