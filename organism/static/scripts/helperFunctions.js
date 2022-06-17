/**
 * a helper function to fetch data from an external api and return the data
 * @param {String} url url of the api route from which the data is to be fetched
 * @returns {Object} data recieved from the api or an error that occured while fetching the data
 */
function fetch_data(url) {
   var request = new XMLHttpRequest();
   var data = [];
   var error = null;

   // handle change in request status
   request.onreadystatechange = function () {
      // handling a successfull request
      if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
         data = JSON.parse(this.responseText);
         mainContentToGeneDetail(data);
      }

      // handling a failed request
      else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
         error = {
            status: this.status,
            error: "Failed to fetch data",
         };
      }
   };

   // opening and sending a new request to the server
   request.open("GET", url, true);
   request.send();

   if (error != null) {
      return error;
   }

   return data;
}

function appendChild(child, parent) {
   parent.append(child);
}

function setUpElement(type, classes, content) {
   const element = document.createElement(type);
   classes.forEach(c => {
      element.classList.add(c);
   });
   element.textContent = content;

   return element;
}
