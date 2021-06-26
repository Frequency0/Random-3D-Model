# Random 3D Model Downloader


## Requirements

This requires that you have at least Python 3.7 installed to your machine before running it.

It similarly requires that you have `requests-html` and `requests` installed, which can be installed by running
`pip install -r requirements.txt`

The first time you run it it will also install a chromium shell, this is done through the `requests-html` and will only happen on first run.

## Info

This can pull models from either Thingiverse or PrusaPrinters, and does so by directly loading the HTML.

There may be support for more later, but for the time these were the easiest to introduce.

## Use

The script can be run from command line by changing into the `Random-3D-Model` directory and running `py download.py`, after which it will begin running.

The script also accepts arguments as follows:

`-i` or `--independant` - Runs the script without asking for input from the user

`-u` or `--unlimited`   - Runs the script over and over again to download many random prints

`-f` or `--filter`      - Filters the results based on the input

`-s` or `--service`     - Specifies which service to use, accepts either 'prusa' or 'thingiverse'

`-o` or `--output`      - Specifies a location to save the files to

## Examples

`py download.py --unlimited --independant`

`py download.py --independant --service prusa`

`py download.py --independant --service thingiverse --output Random/Files`

`py download.py --independant --filter "Super Cow" --service thingiverse`

`py download.py --filter Awesome`


## Me

This is the first script I have every publicly released, so please bare with me. If there are errors, please let me know and I will do my best to get them fixed.
