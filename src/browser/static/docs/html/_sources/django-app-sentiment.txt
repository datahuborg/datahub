.. _django-app-sentiment:

Sentiment
**********
| primary(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`__
| maintainer(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`__, `Gina Yuan <https://github.com/ygina>`__
| location: ``src/apps/sentiment``

A backend and JavaScript library for sentiment analysis using NLTK.

==========
How to Use
==========
* Create a Repo and a Table. The table must include at least one text field
* Insert data into the table. Data must include some sentences or sentence fragments
* Navigate to the table
* Click "Run Sentiment Analysis" and select the column with sentences
* Sentences with negative sentiments will be in red font. Positive sentiments will be in green.


=================
Technical Details
=================

---------------------------
Building the Client Library
---------------------------
* Navigate to the ``src/apps/sentiment`` directory
* Run ``source build.sh``, this will produce the output client file in ``src/browser/static/sentiment/sentiment.js``

------------------------
Using the Client Library
------------------------
* Include ``sentiment.js`` (the build instructions are above) in your HTML file
* In your JavaScript code, call

``Sentiment(sentences, callback)``

where ``sentences`` is an array of strings (each is a sentence) and ``callback`` is a ``function(err, sentiments)``. ``err`` is ``null`` if there is no error (or a ``string`` if there is an error). ``sentiments`` is an array of objects of the form ``{"sentence": String, "polarity": Number, "subjectivity": Number}``.

.. note:: Sentiment is closely tied to DataTables. DataTables is disabled when viewing collaborators' repos, and so sentiment is too.