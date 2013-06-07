Installation and usage
======================

1. ```pip install git+git://github.com/vladignatyev/python-iprewrite.git```
2. Generate ranges from text file with RewriteCond directives: ```iprewrite testfile.txt ranges.txt```
3. Run ```python example.py``` 
4. Look at the source code of ```example.py``` for usage example of obtained IP ranges table.
 
TODO
====

1. Test coverage, pep8
2. Replace bruteforce with euristical algorithm
3. Add IP masks generation
4. Add Nginx configs generation from Apache configs.
