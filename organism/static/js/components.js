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

   // create a div for displaying proteins
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
   buttonDiv.classList.add("d-flex", "justify-content-center", "flex-column");

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
      taxa_id: taxonomy.taxa_id,
      clade: taxonomy.clade,
      genus: taxonomy.genus,
      species: taxonomy.species,
   });
   appendChild(taxonomyTable, rootElement);

   // create a subtitle for the table of proteins
   var subTitle = setUpTitle("h4", ["text-center"], "Protein List");
   // append the subtitle to the root element
   appendChild(subTitle, rootElement);

   // url from which the proteins list is to be fetched
   var url = "/api/proteins/" + taxonomy.taxa_id;
   // fetch data from the url
   var request = new XMLHttpRequest();
   // handle change in request status
   request.onreadystatechange = function () {
      // handling a successfull request
      if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
         DisplayProteinList(JSON.parse(this.responseText));
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
}

function DisplayProteinList(data) {
   var rootElement = document.getElementById("root");
   var dataTable = document.createElement("table");

   var tableHeader = document.createElement("thead");
   var row = createTableRow(true, [{ content: "Protein id" }, { content: "" }]);

   appendChild(row, tableHeader);
   appendChild(tableHeader, dataTable);

   data.forEach(protein => {
      var tableBody = document.createElement("tbody");
      var row = createTableRow(false, [{ content: protein.protein_id }]);

      var button = document.createElement("button");
      button.classList.add("btn", "btn-light", "w-75", "mb-2");
      button.textContent = "detials";
      button.onclick = function () {
         Protein(protein.protein_id);
      };

      appendChild(button, row);

      appendChild(row, tableBody);
      appendChild(tableBody, dataTable);
   });

   dataTable.classList.add(
      "table",
      "table-dark",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm"
   );
   appendChild(dataTable, rootElement);
}

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
   var taxonomyTable = createTaxonomyTable({ taxa_id, clade, genus, species });
   appendChild(taxonomyTable, rootElement);
}

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
   var request = new XMLHttpRequest();

   request.onreadystatechange = function () {
      // handling a successfull request
      if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
         DisplayProteinDetails(JSON.parse(this.responseText));
      }

      // handling a failed request
      else if (this.status > 400 || (this.status > 0 && this.status < 200)) {
         error = {
            status: this.status,
            error: "Failed to fetch data",
         };
      }
   };

   request.open("GET", url, true);
   request.send();
}

/**
 * A function to display a Protein Details in a table
 * @param {Object} data Protein data to be displayed on the screen
 */
function DisplayProteinDetails(data) {
   console.log(data);
   var table = document.createElement("table");

   var tableBody = document.createElement("tbody");

   var row = createTableRow(false, [
      { content: "Protein id" },
      { content: data.protein_id },
   ]);
   appendChild(row, tableBody);

   row = createTableRow(false, [
      { content: "Lenght" },
      { content: data.length },
   ]);
   appendChild(row, tableBody);

   data.domains.forEach(domain => {
      row = createTableRow(true, [{ content: "Domain" }]);
      appendChild(row, tableBody);

      row = createTableRow(false, [
         { content: "description" },
         { content: domain.description },
      ]);
      appendChild(row, tableBody);

      row = createTableRow(false, [
         { content: "start coordinate" },
         { content: domain.start_coordinate },
      ]);
      appendChild(row, tableBody);

      row = createTableRow(false, [
         { content: "end coordinate" },
         { content: domain.end_coordinate },
      ]);
      appendChild(row, tableBody);
   });

   data.taxonomy.forEach(domain => {
      row = createTableRow(true, [{ content: "taxonomy" }]);
      appendChild(row, tableBody);

      row = createTableRow(false, [
         { content: "id" },
         { content: domain.taxa_id },
      ]);
      appendChild(row, tableBody);
   });

   appendChild(tableBody, table);

   table.classList.add(
      "table",
      "table-light",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm",
      "mt-2"
   );

   var root = document.getElementById("root");
   appendChild(table, root);

   var sequenceDiv = document.createElement("div");
   var sequenceLabel = document.createElement("h5");
   sequenceLabel.textContent = "Protein sequence";
   appendChild(sequenceLabel, sequenceDiv);

   var sequence = document.createElement("p");
   sequence.textContent = data.sequence;
   sequence.classList.add("text-break");

   appendChild(sequence, sequenceDiv);
   appendChild(sequenceDiv, root);
}
