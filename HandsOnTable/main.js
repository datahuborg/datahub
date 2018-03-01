
      var base_url = "https://datahub.csail.mit.edu";
      // var base_url = "http://datahub-local.mit.edu";
      var client_id = "NXvP3yESbVTbmuN3vuKBGENYTrlRazczwFe4u8XO";
      // var client_id = "A76uzQCu0tVZQpE2YR1NqQPGy3CsqZ3HW1S4h4QW";
      var redirect_uri = "http://web.mit.edu/mkyhuang/www/DataHub_HandsOnTable/";

      // Convenience function to build DataHub URL strings
      // Expects a path starting with a slash. If a params object is present,
      // it encodes and appends that as query parameters.
      function buildURL(path, params) {
          query = "";
          if (params !== undefined && Object.keys(params).length > 0) {
              query = "?" + $.param(params)
          }
          return base_url + path + query;
      }

      // Convenience function to convert a query string into an associative
      // array.
      function paramsFromQuery(query) {
          params = {};
          parts = query.split("&");
          for (var i = parts.length - 1; i >= 0; i--) {
              pieces = parts[i].split("=");
              params[decodeURIComponent(pieces[0])] = decodeURIComponent(pieces[1].replace(/\+/g, " "));
          }
          return params;
      }

      // Convenience function to copy a value to localStorage if it exists in
      // an associate array.
      function saveIfSet(assocArray, key) {
          if (assocArray[key]) {
              console.log("Saving " + key + ": " + assocArray[key]);
              localStorage.setItem(key, assocArray[key]);
          };
      }

      function displayTokenInfo() {
          // Fetch stored info it it's available.
          var access_token = localStorage.getItem('access_token');
          var scope = localStorage.getItem('scope');

          // Populate the page's token info.
          $("#access_token").text(access_token);
          $("#scope").text(scope);
      }

      function buttonWithName(name) {
        return $("<button />", {
                  type: "button",
                  class: "btn btn-default btn-sm pull-right",
                  text: name,
                })
      }

      function refreshRepos() {
        var view = $("#interactive_part");
        view.find("h1 .username").text(localStorage.getItem('username'));
        console.log(localStorage)
        view.show();
        Handsontable_deferred.resolve();
        $.ajax({
          url: buildURL("/api/v1/user/repos/"),
          type: 'GET',
          beforeSend: function(xhr){
              xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('access_token'));
              // xhr.setRequestHeader('Accept-Encoding', 'gzip');
          },
          dataType: 'json',
        })
        .fail(function(xhr, status, error) {
          console.log("refreshRepos failed");
        })
        .done(function(data, status, xhr) {
          console.log(data.repos);
          // Handsontable_deferred.resolve();
          $(document).data('repos', data.repos);
          // displayRepos();
        })
      }


      $(document).ready(function() {

          // Pull the access token from the URL hash if it's available.
          // Overwrite whatever's currently in storage.
          if (window.location.hash.length > 1) {
              params = paramsFromQuery(window.location.hash.substring(1));
              if (params['access_token']) {
                  keys = ['access_token', 'scope'];
                  for (var i = keys.length - 1; i >= 0; i--) {
                      console.log("Trying " + keys[i]);
                      saveIfSet(params, keys[i]);
                  }
                  // Clear the hash after handling the access_token.
                  // Just setting window.location.hash = "" leaves a dangling #.
                  // history.replaceState("", document.title, window.location.pathname + window.location.search);
              }
              console.log(params);
          }

          displayTokenInfo();

          // Set access token for all further calls
          $.ajaxSetup({
              beforeSend: function(xhr) {
                  xhr.setRequestHeader('Authorization', 'Bearer ' +
                      localStorage.getItem('access_token'));
              }
          });

          // Request authorization button
          $("#request").click(function() {
              console.log("requesting auth")
              var params = {
                  "response_type": "token",
                  "scope": "read write",
                  "client_id": client_id,
                  "redirect_uri": redirect_uri
              };
              var authorization_url = buildURL("/oauth2/authorize/", params);
              window.location.href = authorization_url;
          });

          // Clear authorization button
          $("#clear").click(function() {
              console.log("clearing auth")
              keys = ['access_token', 'scope'];
              for (var i = keys.length - 1; i >= 0; i--) {
                  localStorage.removeItem(keys[i]);
              };
              // Show that they've been cleared.
              displayTokenInfo();
          });


          $(".api-link").click(function(event) {
            var link = $(this);
            link.next().html("<pre>...</pre>");
            $.ajax({
              url: buildURL(link.text()),
              type: 'GET',
              beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('access_token'));},
              dataType: 'json',
            })
            .fail(function(xhr, status, error) {
              console.log("failed");
              link.next().html("<pre>" + xhr.status + " " + xhr.statusText + "</pre>");
            })
            .done(function(data, status, xhr) {
              console.log("success");
              link.next().html("<pre>" + JSON.stringify(data, null, 2) + "</pre>");
            })
            
          });


          $.ajax({
            url: buildURL("/api/v1/user/"),
            type: 'GET',
            beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('access_token'));},
            dataType: 'json',
          })
          .fail(function(xhr, status, error) {
            console.log("failed");
          })
          .done(function(data, status, xhr) {
            localStorage.setItem('username', data.username);
            refreshRepos();
          })

      });
 