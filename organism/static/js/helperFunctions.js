/**
 * A function that appends a child to its parent
 * @param {Element} child the child to be appended in the parent element
 * @param {Element} parent the parent element
 */
function appendChild(child, parent) {
   parent.append(child);
}

/**
 * A function that simplifies creating a title
 * @param {String} type Type of html element
 * @param {Array} classes Array of string with each string representing a list to be added to html element
 * @param {String} content Content of the title element
 * @returns the HTML element created
 */
function setUpTitle(type, classes, content) {
   // create a new element
   const element = document.createElement(type);
   // add all element relaed class
   classes.forEach(c => {
      element.classList.add(c);
   });
   // add the content to the element
   element.textContent = content;

   return element;
}

/**
 * A function to simpify create a row within a HTML table
 * @param {boolean} header determines if the row is a header row or not
 * @param {Array} content List of contents
 * @returns Table row element (tr)
 */
function createTableRow(header, content) {
   // create a row element
   var tableRow = document.createElement("tr");
   // add some classes
   tableRow.classList.add("text-center");

   // iterate over the row content and add
   // them to the raw
   content.forEach(data => {
      var tableData;
      if (header) {
         tableData = document.createElement("th");
      } else {
         tableData = document.createElement("td");
      }

      tableData.textContent = data.content;

      appendChild(tableData, tableRow);
   });

   // return the row
   return tableRow;
}

function createTaxonomyTable(taxonomy) {
   // display taxonomy data through a table
   var taxonomyTable = document.createElement("table");

   // add classes to the HTML element
   taxonomyTable.classList.add(
      "table",
      "table-light",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm",
      "mt-2"
   );

   // create a body element for the table
   var tableBody = document.createElement("tbody");

   // create a row for displaying the taxaonomy id
   var row = createTableRow(false, [
      { content: "taxa id" },
      { content: taxonomy.taxa_id },
   ]);
   // append the row to the table body
   appendChild(row, tableBody);

   // create a row for displaying the taxaonomy clade
   var row = createTableRow(false, [
      { content: "clade" },
      { content: taxonomy.clade },
   ]);
   // append the row to the table body
   appendChild(row, tableBody);

   // create a row for displaying the taxaonomy genus
   var row = createTableRow(false, [
      { content: "genus" },
      { content: taxonomy.genus },
   ]);
   // append the row to the table body
   appendChild(row, tableBody);

   // create a row for displaying the taxaonomy species
   var row = createTableRow(false, [
      { content: "species" },
      { content: taxonomy.species },
   ]);
   // append the row to the table body
   appendChild(row, tableBody);

   // append the body to the table element
   appendChild(tableBody, taxonomyTable);

   // return the HTML table
   return taxonomyTable;
}

/**
 * Function to make a request and call a callback
 * function to dipslay retrieved data
 *
 * sends two arguements to the callback function
 * one containing data
 * one containing errors
 *
 * @param {String} url url to fetch the data from
 * @param {function} callback a callback function called to display the data retrived
 * @returns {void} Nothing
 */
function fetch_data(url, callback) {
   // create new instance of XML HTTP Request
   var request = new XMLHttpRequest();

   // handle change in request state
   request.onreadystatechange = function () {
      if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
         callback(JSON.parse(this.responseText), null);
      } else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
         callback(null, { status: this.status, error: "failed to fetch data" });
      }
   };

   // open the request and send it
   request.open("GET", url);
   request.send();
}

/**
 * A function that notifies the user about an occured error
 * @param {Object} error contains a error message and status code
 * @returns HTML div element containing the error details
 */
function handleError(error) {
   // create a div element to wrap all of the error related data
   var errorElement = document.createElement("div");

   // create a title showing that an error occured
   var errorTitle = setUpTitle("h2", [], "Opps, seems like an error occured");
   // add the title to the wrapper div
   appendChild(errorTitle, errorElement);

   // create paragrap elements for the error status and message
   var errorStatus = document.createElement("p");
   var errorMessage = document.createElement("p");

   // set the content of the paragraph elements to the status
   // and message of the error
   errorStatus.textContent = error.status;
   errorMessage.textContent = error.message;

   // add the error message and status to the wrapper div
   appendChild(errorStatus, errorElement);
   appendChild(errorMessage, errorElement);

   // return the wrapper div element
   return errorElement;
}
