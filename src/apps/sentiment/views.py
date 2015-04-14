import json
from django.shortcuts import render
from django.http import HttpResponse

from core.db.manager import DataHubManager
from account.auth import *

from textblob import TextBlob

'''
Returns a successful JSON response.

@param json_dict - A dictionary representing the JSON to be sent to the user. It will be augmented
                    with the property, json_dict.success = true

@return An HttpResponse representing the json_dict (augmented with the "success" property).
'''
def json_response(json_dict):
    json_dict["success"] = True
    return HttpResponse(json.dumps(json_dict), content_type="application/json")

'''
Returns a failure JSON response.

@return An HttpResponse representing the JSON object
{
    "success": false
}
'''
def error_response(message):
    return HttpResponse(json.dumps({"success": False, "message": message}), content_type="application/json")

'''
Return the list of repos associated with the current user. If successful, the response is JSON of 
the form:

{
    "success": true,
    "repos": [String]
}

If there was a failure, the response is JSON of the form:

{
    "success": false
}
'''
@login_required
def sentiment(request):
    sentences = request.GET.getlist("sentences[]", []);
    if len(sentences) == 0:
        return error_response("No sentences provided")
    sentiments = []
    for sentence in sentences:
        sentiment = TextBlob(sentence).sentiment
        sentiments.append({"sentence": sentence, "polarity": sentiment.polarity, "subjectivity": sentiment.subjectivity})
    return json_response({"sentiments": sentiments})
