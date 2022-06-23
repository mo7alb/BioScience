/**
 * Displays content of the home page
 * @returns {void} Nothing
 */
function Home() {
   // clear the content of the root element if there is any
   clearRoot();

   // create title for the page
   var title = setUpTitle("h2", "Home page");
   // add title to the page
   appendToRoot(title);
}

/**
 * a function to display the data of the taxonomy
 * @param {Number} taxa_id
 * @param {String} clade
 * @param {String} genus
 * @param {String} species
 */
function ShowTaxonomy(taxa_id, clade, genus, species) {
   // clear the content of the root element if there is any
   clearRoot();

   // create title for the page
   var title = setUpTitle("h2", "Home page");
   // add title to the page
   appendToRoot(title);

   // display taxonomy data through a table
   var taxonomyTable = createTaxonomyTable({ taxa_id, clade, genus, species });
   appendToRoot(taxonomyTable);

   // a div to hold all the buttons
   var buttonDiv = document.createElement("div");
   buttonDiv.classList.add(
      "d-flex",
      "justify-content-center",
      "flex-column",
      "align-items-center"
   );

   // a button to fetch all proteins of the taxonomy
   var proteinButton = Button("Show all taxonomy proteins", false, function () {
      TaxonomyProteins({ taxa_id, clade, genus, species });
   });
   appendChild(proteinButton, buttonDiv);

   // a button to fetch all pfams of the taxonomy
   var pfamButton = Button("Show all taxonomy pfams", false, function () {
      TaxonomyPfams({ taxa_id, clade, genus, species });
   });
   appendChild(pfamButton, buttonDiv);

   // add the div to the root element
   appendToRoot(buttonDiv);
}

/**
 * A function Proteins related to a taxonomy
 * @param {Object} taxonomy Taxomony of which the data is to be displayed
 */
function TaxonomyProteins(taxonomy) {
   // clear the content of the root element if there is any
   clearRoot();

   // create title for the page
   var title = setUpTitle("h2", "Proteins");
   // add title to the page
   appendToRoot(title);

   // display taxonomy data through a table
   var taxonomyTable = createTaxonomyTable({
      taxa_id: "terst",
      clade: taxonomy.clade,
      genus: taxonomy.genus,
      species: taxonomy.species,
   });
   appendToRoot(taxonomyTable);

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
   var proteinButton = Button("Show all taxonomy proteins", false, function () {
      TaxonomyProteins(taxonomy);
   });
   appendChild(proteinButton, buttonDiv);

   // a button to display a component that displays
   // list of pfams
   var pfamButton = Button("Show all taxonomy pfams", false, function () {
      TaxonomyPfams(taxonomy);
   });
   appendChild(pfamButton, buttonDiv);

   // add the div to the root element
   appendToRoot(buttonDiv);

   // create a subtitle for the table of proteins
   var subTitle = setUpTitle("h4", "Protein List");
   // append the subtitle to the root element
   appendToRoot(subTitle);

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
   // handle error if any occur
   if (error !== null) {
      appendToRoot(handleError(error));
      return;
   }

   // create a table header
   var tableHeader = document.createElement("thead");
   // specify the content of the header row
   var row = createTableRow(true, [{ content: "Protein id" }, { content: "" }]);
   // append the row to the header element and the header element to the table
   appendChild(row, tableHeader);

   // create a table body element to contain all the protein rows
   var tableBody = document.createElement("tbody");
   // iterate over proteins list and display the protein id and a button
   data.forEach(protein => {
      // create a row element with the protein id
      var row = createTableRow(false, [{ content: protein.protein_id }]);

      var tableData = document.createElement("td");

      // create the detail button
      var detailButton = Button("details", true, function () {
         Protein(protein.protein_id);
      });

      appendChild(detailButton, tableData);
      // add the button to the second column of the row
      appendChild(tableData, row);
      // add the row to the table body
      appendChild(row, tableBody);
   });

   var proteinList = createTable(tableHeader, tableBody);

   // append the protein list table to the root div
   appendToRoot(proteinList);
}

/**
 * Displays details of pfams on the screen based on the taxonomy passed
 * @param {Object} taxonomy taxonomy to which the pfams are related to
 */
function TaxonomyPfams(taxonomy) {
   // clear the content of the root element if there is any
   clearRoot();

   // create title for the page
   var title = setUpTitle("h2", "Pfams");
   // add title to the page
   appendToRoot(title);

   // display taxonomy data through a table
   var taxonomyTable = createTaxonomyTable(taxonomy);
   appendToRoot(taxonomyTable);

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
   var proteinButton = Button("Show all taxonomy proteins", false, function () {
      TaxonomyProteins(taxonomy);
   });
   appendChild(proteinButton, buttonDiv);

   // a button to fetch all pfams of the taxonomy
   var pfamButton = Button("Show all taxonomy pfams", false, function () {
      TaxonomyPfams(taxonomy);
   });
   appendChild(pfamButton, buttonDiv);

   // add the div to the root element
   appendToRoot(buttonDiv);

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
   // clear the content of the root element if there is any
   clearRoot();

   // create title for the page
   var title = setUpTitle("h2", "Protein Details");
   // add title to the page
   appendToRoot(title);

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
   // handle an error if any occured
   if (error !== null) {
      appendToRoot(handleError(error));
      return;
   }

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

   var proteinDetails = createTable(null, tableBody);

   // append the protein details table to the root div
   appendToRoot(proteinDetails);

   // create a div as a container for the protein sequence
   var sequenceDiv = document.createElement("div");

   // add bootstrap4 class to the container div
   sequenceDiv.classList.add("container");

   // create a title to describe the content of the div
   // and add this is the container div
   var sequenceLabel = setUpTitle("h2", "Protein sequence");
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
   appendToRoot(sequenceDiv);

   // url to fetch protein coverage from
   var url = "/api/coverage/" + data.protein_id;
   // fetch details
   fetch_data(url, DisplayProteinCoverage);
}

/**
 * A function to display list of pfams as a table
 * @param {Array} data array of data recieved from the api
 * @param {Object} error object of error in case an error occurs, null otherwise
 * @returns Nothing
 */
function PfamsList(data, error) {
   // handle an error if any occured
   if (error !== null) {
      appendToRoot(handleError(error));
      return;
   }

   // header for pfam list table
   var pfamHeader = document.createElement("thead");

   // header row for pfam list table
   var row = createTableRow(true, [{ content: "domain id" }, { content: "" }]);

   // append the row to the header and the header to the table
   appendChild(row, pfamHeader);

   // body for the pfam list table
   var pfamBody = document.createElement("tbody");

   // iterate over each pfam and add its domain id to the pfam list table
   data.forEach(obj => {
      // create a pfam row
      var pfamRow = createTableRow(false, [{ content: obj.pfam.domain_id }]);

      // a pfam detail button
      var detailButton = Button("pfam details", true, function () {
         getPfamDetails(obj.pfam.domain_id);
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

   // create a table to display pfam data
   var pfamTable = createTable(pfamHeader, pfamBody);

   // append the table to the root element
   appendToRoot(pfamTable);
}

/**
 * function that makes a request to the api to fetch details about a pfam
 * @param {String} id domain id of the pfam
 * @returns Nothing
 */
function getPfamDetails(id) {
   // clear all the elements of the root element
   clearRoot();

   // set a title to show what page is it
   var title = setUpTitle("h2", "Pfam details");
   // append the child to the root element
   appendToRoot(title, root);

   // url to fetch the data from api
   var url = "/api/pfam/" + id;
   // fetch data and display them
   fetch_data(url, showPfamDetails);
}

/**
 * function that displays details of a pfam as a table
 * @param {Object} data data recieved from the api
 * @param {Object} error error occured while fetching data
 * @returns Nothing
 */
function showPfamDetails(data, error) {
   // handle error if any occurs
   if (error !== null) {
      appendToRoot(handleError(error));
      return;
   }

   // create a header for the pfam detail table
   var tableHeader = document.createElement("thead");
   // create a header row for the pfam detail table header
   var headerRow = createTableRow(true, [
      { content: "domain id" },
      { content: "domain description" },
   ]);
   // add header row to the pfam detail table header
   appendChild(headerRow, tableHeader);

   // create a body for the pfam detail table
   var tableBody = document.createElement("tbody");

   // create a row for the data
   var dataRow = createTableRow(false, [
      { content: data.domain_id },
      { content: data.domain_description },
   ]);
   // add data row to the details table
   appendChild(dataRow, tableBody);

   // create a table to display pfam details
   var pfamDetailsTable = createTable(tableHeader, tableBody);

   // append the pfam detail table to the root element
   appendToRoot(pfamDetailsTable);
}

/**
 * function that displays the coverage of the protein
 * @param {Object} data data retreived from the api
 * @param {Object} error error occured during the retreival of data
 * @returns Nothing
 */
function DisplayProteinCoverage(data, error) {
   // handle errors if any occues
   if (error !== null) {
      appendToRoot(handleError(error));
      return;
   }

   // create div that contains the coverage of the protein and details
   var coverageDiv = document.createElement("div");
   // set up a title and add it to the coverage div
   appendChild(setUpTitle("h2", "Protein coverage"), coverageDiv);
   // style coverage div with bootstrap4 class
   coverageDiv.classList.add("container");

   // create a paragraph element containing the coverage details
   var coverage = document.createElement("p");
   // set the paragraph content to the coverage details
   coverage.textContent = "Protein Coverage = " + data.coverage;
   // style paragraph with bootstrap4 class names
   coverage.classList.add("text-center");

   // add the coverage paragraph to the coverage container
   appendChild(coverage, coverageDiv);
   // add coverage container div to the root
   appendToRoot(coverageDiv);
}
