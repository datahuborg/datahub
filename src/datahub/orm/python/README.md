DataHub Python ORM Spec
=======

Status update: 30th Oct, 2013

DONE: 
implemented basic version of orm 
can convert simple queries to create statements in table
class preserved - foregin key might be easier

TODO:
general
add more features - can only do new() right now, and that too, partially

models.py
Support more Field types
Support more params such as primary key, foreign key, check (?), default
Fix inheritance issue

sample_models.py (testing code)

parse_models.py
make code cleaner 
fix io hardcoding
helper functions! 
