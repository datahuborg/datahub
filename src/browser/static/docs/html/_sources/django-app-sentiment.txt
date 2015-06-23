.. _django-app-sentiment:

Sentiment
**********
| primary(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintainer(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| location: ``src/apps/sentiment``

A backend and JavaScript library for sentiment analysis using NLTK.

--------------------
Build Client Library
--------------------
* Navigate to the ``src/apps/sentiment`` directory
* Run ``source build.sh``, this will produce the output client file in ``src/browser/static/sentiment/sentiment.js``

--------------------
Using Client Library
--------------------
* Include ``sentiment.js`` (the build instructions are above) in your HTML file
* In your JavaScript code, call

``Sentiment(sentences, callback)``

where ``sentences`` is an array of strings (each is a sentence) and ``callback`` is a ``function(err, sentiments)``. ``err`` is ``null`` if there is no error (or a ``string`` if there is an error). ``sentiments`` is an array of objects of the form ``{"sentence": String, "polarity": Number, "subjectivity": Number}``.