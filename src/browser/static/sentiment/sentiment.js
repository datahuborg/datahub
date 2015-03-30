Sentiment = function(sentences, callback) {
  var sentence_arr = sentences;
  if (sentences.length === undefined) {
    sentence_arr = [sentences];
  }
  $.get("/apps/sentiment/api/", {"sentences": sentence_arr}, function(data) {
    if (data.success) {
      callback(null, data.sentiments);
    } else {
      callback(data.message);
    }
  });
};
