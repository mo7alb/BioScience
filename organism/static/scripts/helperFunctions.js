/**
 * a helper function to fetch data from an external api and return the data
 * @param {String} url url of the api route from which the data is to be fetched
 * @returns {Object} data recieved from the api or an error that occured while fetching the data
 */
function fetch_data(url) {
   return XMLHttpRequest;
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
