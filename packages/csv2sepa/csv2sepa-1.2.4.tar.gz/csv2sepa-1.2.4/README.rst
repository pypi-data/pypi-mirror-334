CSV to SEPA Convertor
=====================

This is a python implementation to generate SEPA XML files from a CSV file.

Limitations
-----------

Supported standards:

* SEPA PAIN.001.001.03 (v2009, not authorized after november 2025)
* SEPA PAIN.001.001.09 (v2019, last version)
* SEPA PAIN.008.001.02 (v2009, not authorized after november 2025)
* SEPA PAIN.008.001.08 (v2019, last version)

Usage
-----
1. Configure the `csv2sepa.ini` file with your informations.
2. Create a CSV file with data based on the example file corresponding to the desired SEPA format (provided in the ./csv directory).
3. Run `py csv2json.py` and answer to the questions (which SEPA format? Which CSV file?).
4. The generated XML file will be saved in the ./xml directory.

Credits and License
-------------------

Maintainer: Philippe-Alexandre PIERRE <pap@httpap.dev>

The source code is released under MIT license.
