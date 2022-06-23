/**
 * Displays content of the home page
 * @returns {void} Nothing
 */
function Home() {
   // get the root element
   var rootElement = document.getElementById("root");
   // clear the content of the root element if there is any
   if (rootElement.innerHTML !== "") rootElement.innerHTML = "";

   // create title for the page
   var title = setUpTitle("h2", ["text-center"], "Home page");
   // add title to the page
   appendChild(title, rootElement);
}

/**
 * Displays content of the Proteins page
 * @returns {void} Nothing
 */
function Proteins() {
   var rootElement = document.getElementById("root");
   rootElement.innerHTML = "";

   var title = setUpTitle("h2", ["text-center"], "Proteins page");
   appendChild(title, rootElement);
}

/**
 * Displays content of the pfams page
 * @returns {void} Nothing
 */
function Pfams() {
   var rootElement = document.getElementById("root");
   rootElement.innerHTML = "";

   var title = setUpTitle("h2", ["text-center"], "Pfams page");
   appendChild(title, rootElement);
}

/**
 * a function to display the data of the taxonomy
 * @param {Number} taxa_id
 * @param {String} clade
 * @param {String} genus
 * @param {String} species
 */
function ShowTaxonomy(taxa_id, clade, genus, species) {
   // get the root element
   var rootElement = document.getElementById("root");
   // clear the content of the root element if there is any
   if (rootElement.innerHTML !== "") rootElement.innerHTML = "";

   // create title for the page
   var title = setUpTitle("h2", ["text-center"], "Home page");
   // add title to the page
   appendChild(title, rootElement);

   // display taxonomy data through a table
   var taxonomyTable = createTaxonomyTable({ taxa_id, clade, genus, species });
   appendChild(taxonomyTable, rootElement);

   // a div to hold all the buttons
   var buttonDiv = document.createElement("div");
   buttonDiv.classList.add(
      "d-flex",
      "justify-content-center",
      "flex-column",
      "align-items-center"
   );

   // a button to fetch all proteins of the taxonomy
   var proteinButton = document.createElement("button");
   proteinButton.classList.add("btn", "btn-dark", "w-75", "mb-2");
   proteinButton.textContent = "Show all taxonomy proteins";
   proteinButton.onclick = function () {
      TaxonomyProteins({ taxa_id, clade, genus, species });
   };
   appendChild(proteinButton, buttonDiv);

   // a button to fetch all pfams of the taxonomy
   var pfamButton = document.createElement("button");
   pfamButton.classList.add("btn", "btn-dark", "w-75");
   pfamButton.textContent = "Show all taxonomy pfams";
   pfamButton.onclick = function () {
      TaxonomyPfams({ taxa_id, clade, genus, species });
   };
   appendChild(pfamButton, buttonDiv);

   // add the div to the root element
   appendChild(buttonDiv, rootElement);
}

/**
 * A function Proteins related to a taxonomy
 * @param {Object} taxonomy Taxomony of which the data is to be displayed
 */
function TaxonomyProteins(taxonomy) {
   // get the root element
   var rootElement = document.getElementById("root");
   // clear the content of the root element if there is any
   if (rootElement.innerHTML !== "") rootElement.innerHTML = "";

   // create title for the page
   var title = setUpTitle("h2", ["text-center"], "Proteins");
   // add title to the page
   appendChild(title, rootElement);

   // display taxonomy data through a table
   var taxonomyTable = createTaxonomyTable({
      taxa_id: "terst",
      clade: taxonomy.clade,
      genus: taxonomy.genus,
      species: taxonomy.species,
   });
   appendChild(taxonomyTable, rootElement);

   // a div to hold all the buttons
   var buttonDiv = document.createElement("div");
   buttonDiv.classList.add(
      "d-flex",
      "justify-content-center",
      "flex-column",
      "align-items-center",
      "mb-4"
   );

   // a button to fetch all proteins of the taxonomy
   var proteinButton = document.createElement("button");
   proteinButton.classList.add("btn", "btn-dark", "w-75", "mb-2");
   proteinButton.textContent = "Show all taxonomy proteins";
   proteinButton.onclick = function () {
      TaxonomyProteins(taxonomy);
   };
   appendChild(proteinButton, buttonDiv);

   // a button to display a component that displays
   // list of pfams
   var pfamButton = document.createElement("button");
   pfamButton.classList.add("btn", "btn-dark", "w-75");
   pfamButton.textContent = "Show all taxonomy pfams";
   pfamButton.onclick = function () {
      TaxonomyPfams(taxonomy);
   };
   appendChild(pfamButton, buttonDiv);

   // add the div to the root element
   appendChild(buttonDiv, rootElement);

   // create a subtitle for the table of proteins
   var subTitle = setUpTitle("h4", ["text-center"], "Protein List");
   // append the subtitle to the root element
   appendChild(subTitle, rootElement);

   // url from which the proteins list is to be fetched
   var url = "/api/proteins/" + taxonomy.taxa_id;

   // fetch the data from the url and pass to the callback function DisplayProteinList
   fetch_data(url, DisplayProteinList);
}

/**
 * A function called after requesting for protein data
 * this data is in the form of a list
 * @param {Object} data protein data to be displayed
 * @param {Object} error error occured while fetching data
 */
function DisplayProteinList(data, error) {
   // root element to which every thing is to be rendered
   var rootElement = document.getElementById("root");

   // handle error if any occur
   if (error !== null) {
      appendChild(handleError(error), rootElement);
      return;
   }

   // create a table to display list of proteins
   var dataTable = document.createElement("table");

   // create a table header
   var tableHeader = document.createElement("thead");
   // specify the content of the header row
   var row = createTableRow(true, [{ content: "Protein id" }, { content: "" }]);

   // append the row to the header element and the header element to the table
   appendChild(row, tableHeader);
   appendChild(tableHeader, dataTable);

   // create a table body element to contain all the protein rows
   var tableBody = document.createElement("tbody");

   // iterate over proteins list and display the protein id and a button
   data.forEach(protein => {
      // create a row element with the protein id
      var row = createTableRow(false, [{ content: protein.protein_id }]);

      // create the detail button
      var button = document.createElement("button");
      // add bootstrap4 classes to style the button
      button.classList.add("btn", "btn-light", "w-75", "mb-2");
      // add the text content of the button
      button.textContent = "detials";
      // handle button click
      button.onclick = function () {
         Protein(protein.protein_id);
      };

      // add the button to the second column of the row
      appendChild(button, row);
      // add the row to the table body
      appendChild(row, tableBody);
   });

   // add table body to the table
   appendChild(tableBody, dataTable);

   // style the protein list table with bootstrap4 classes
   dataTable.classList.add(
      "table",
      "table-dark",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm"
   );

   // append the protein list table to the root div
   appendChild(dataTable, rootElement);
}

/**
 * Displays details of pfams on the screen based on the taxonomy passed
 * @param {Object} taxonomy taxonomy to which the pfams are related to
 */
function TaxonomyPfams(taxonomy) {
   // get the root element
   var rootElement = document.getElementById("root");
   // clear the content of the root element if there is any
   if (rootElement.innerHTML !== "") rootElement.innerHTML = "";

   // create title for the page
   var title = setUpTitle("h2", ["text-center"], "Pfams");
   // add title to the page
   appendChild(title, rootElement);

   // display taxonomy data through a table
   var taxonomyTable = createTaxonomyTable(taxonomy);
   appendChild(taxonomyTable, rootElement);

   // a div to hold all the buttons
   var buttonDiv = document.createElement("div");
   // style the div with bootstrap4 classes
   buttonDiv.classList.add(
      "d-flex",
      "justify-content-center",
      "flex-column",
      "align-items-center"
   );

   // a button to fetch all proteins of the taxonomy
   var proteinButton = document.createElement("button");
   proteinButton.classList.add("btn", "btn-dark", "w-75", "mb-2");
   proteinButton.textContent = "Show all taxonomy proteins";
   proteinButton.onclick = function () {
      TaxonomyProteins(taxonomy);
   };
   appendChild(proteinButton, buttonDiv);

   // a button to fetch all pfams of the taxonomy
   var pfamButton = document.createElement("button");
   pfamButton.classList.add("btn", "btn-dark", "w-75");
   pfamButton.textContent = "Show all taxonomy pfams";
   pfamButton.onclick = function () {
      TaxonomyPfams(taxonomy);
   };
   appendChild(pfamButton, buttonDiv);

   // add the div to the root element
   appendChild(buttonDiv, rootElement);

   // url from which the pfams are to be fetched
   var url = "/api/pfams/" + taxonomy.taxa_id;

   // make a html request to the api to get all pfams
   fetch_data(url, PfamsList);
}

/**
 * A function that requests details from the api for a single protein
 * @param {String} id protein id string
 */
function Protein(id) {
   // get the root element
   var rootElement = document.getElementById("root");
   // clear the content of the root element if there is any
   if (rootElement.innerHTML !== "") rootElement.innerHTML = "";

   // create title for the page
   var title = setUpTitle("h2", ["text-center"], "Protein Details");
   // add title to the page
   appendChild(title, rootElement);

   // url to fetch protein details from
   var url = "/api/protein/" + id;
   // fetch details
   fetch_data(url, DisplayProteinDetails);
}

/**
 * A function to display a Protein Details in a table
 * @param {Object} data Protein data to be displayed on the screen
 */
function DisplayProteinDetails(data, error) {
   // root element where everything is to be rendered
   var root = document.getElementById("root");

   // handle an error if any occured
   if (error !== null) {
      appendChild(handleError(error), rootElement);
      return;
   }

   // create table to display protein data
   var table = document.createElement("table");
   // create table body to append the data
   var tableBody = document.createElement("tbody");

   // create row for the protein id
   var row = createTableRow(false, [
      { content: "Protein id" },
      { content: data.protein_id },
   ]);
   // add the row to the table body
   appendChild(row, tableBody);

   // create row for the protein length
   row = createTableRow(false, [
      { content: "Lenght" },
      { content: data.length },
   ]);
   // add the row to the table body
   appendChild(row, tableBody);

   // display domain data as a rows
   data.domains.forEach(domain => {
      // create a title row showing underneath it would be domain data
      row = createTableRow(true, [{ content: "Domain" }, { content: "" }]);
      // add the title to the table body
      appendChild(row, tableBody);

      // create a row for the domain description
      row = createTableRow(false, [
         { content: "description" },
         { content: domain.description },
      ]);

      // add the domain description to the table body
      appendChild(row, tableBody);

      // create a row for the start coordinate
      row = createTableRow(false, [
         { content: "start coordinate" },
         { content: domain.start_coordinate },
      ]);

      // add the start coordinate to the table body
      appendChild(row, tableBody);

      // create a row for the end coordinate
      row = createTableRow(false, [
         { content: "end coordinate" },
         { content: domain.end_coordinate },
      ]);
      // add the end coordinate to the table body
      appendChild(row, tableBody);
   });

   // iterate over taxonomy data and display them to the user
   data.taxonomy.forEach(tax => {
      // create a title row
      row = createTableRow(true, [{ content: "taxonomy" }, { content: "" }]);
      // add title row to table body
      appendChild(row, tableBody);

      // create a row the taxa_id and append it to the table data
      row = createTableRow(false, [
         { content: "id" },
         { content: tax.taxa_id },
      ]);
      appendChild(row, tableBody);
   });

   // append the table body to the table
   appendChild(tableBody, table);

   // add list of bootstap4 classes to the table
   table.classList.add(
      "table",
      "table-light",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm",
      "mt-2"
   );

   // append the protein details table to the root div
   appendChild(table, root);

   // create a div as a container for the protein sequence
   var sequenceDiv = document.createElement("div");

   // add bootstrap4 class to the container div
   sequenceDiv.classList.add("container");

   // create a title to describe the content of the div
   // and add this is the container div
   var sequenceLabel = document.createElement("h5");
   sequenceLabel.textContent = "Protein sequence";
   appendChild(sequenceLabel, sequenceDiv);

   // create an paragraph element to contain the
   // protein sequnece
   var sequence = document.createElement("p");
   sequence.textContent = data.sequence;

   // add bootstrap4 class to it to style it
   sequence.classList.add("text-break");
   // add the sequence to the container div
   appendChild(sequence, sequenceDiv);

   // add the container div to the root div
   appendChild(sequenceDiv, root);
}

/**
 * A function to display list of pfams as a table
 * @param {Array} data array of data recieved from the api
 * @param {Object} error object of error in case an error occurs, null otherwise
 * @returns Nothing
 */
function PfamsList(data, error) {
   console.log(data);
   // root element where everything is to be rendered
   var root = document.getElementById("root");

   // handle an error if any occured
   if (error !== null) {
      appendChild(handleError(error), root);
      return;
   }

   // table to display list of pfams
   var pfamTable = document.createElement("table");

   // header for pfam list table
   var pfamHeader = document.createElement("thead");

   // header row for pfam list table
   var row = createTableRow(true, [{ content: "domain id" }, { content: "" }]);

   // append the row to the header and the header to the table
   appendChild(row, pfamHeader);
   appendChild(pfamHeader, pfamTable);

   // body for the pfam list table
   var pfamBody = document.createElement("tbody");

   // iterate over each pfam and add its domain id to the pfam list table
   data.forEach(obj => {
      // create a pfam row
      var pfamRow = createTableRow(false, [{ content: obj.pfam.domain_id }]);

      // a pfam detail button
      var detailButton = document.createElement("button");
      // styling detail button with bootstrap4 classew
      detailButton.classList.add("btn", "btn-secondary");
      // adding content to the detail button
      detailButton.textContent = "pfam details";
      // handle detail button click event
      detailButton.onclick(function () {
         pfamDetails(obj.id);
      });

      // create a table data to store the detail button
      var tableData = document.createElement("td");

      // append the button to the table data
      appendChild(detailButton, tableData);
      // adding the table data to the row
      appendChild(tableData, pfamRow);
      // add pfam to the table body
      appendChild(pfamRow, pfamBody);
   });

   // append the body to the pfam list table
   appendChild(pfamBody, pfamTable);

   // style the table with bootstrap4 classes
   pfamTable.classList.add(
      "table",
      "table-light",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm",
      "mt-2"
   );

   // append the table to the root element
   appendChild(pfamTable, root);
}
