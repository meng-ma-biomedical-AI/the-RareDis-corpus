This folder contain the files of the RareDis corpus. The test dataset is not published yet, because we plan to organise a shared task of information extraction about rare diseases.
- train.zip and dev.zip contains the training and validation files (txt and ann), respectively.
- The files visual.conf and annotation.conf are needed to visualise the annotations with the BRAT annotation tool (https://brat.nlplab.org/).
- bratman.py is a Python script. It contains two functions: i) count_entities, given a path containing ann files, counts their instances of entities and relations; and ii) order_brat that gets a path rewrite all its ann files. In the new ann files, the IDs of the mentions are numbered according to their occurence in the text.
