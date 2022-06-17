function appendChild(child, parent) {
   parent.append(child);
}

function setUpTitle(type, classes, content) {
   const element = document.createElement(type);
   classes.forEach(c => {
      element.classList.add(c);
   });
   element.textContent = content;

   return element;
}

function createTableRow(header, content) {
   var tableRow = document.createElement("tr");
   tableRow.classList.add("text-center");

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

   return tableRow;
}

function createTaxonomyTable(taxonomy) {
   // display taxonomy data through a table
   var taxonomyTable = document.createElement("table");

   taxonomyTable.classList.add(
      "table",
      "table-light",
      "table-striped",
      "table-bordered",
      "table-hover",
      "table-responsive-sm",
      "mt-2"
   );

   var tableBody = document.createElement("tbody");

   var row = createTableRow(false, [
      { content: "taxa id" },
      { content: taxonomy.taxa_id },
   ]);
   appendChild(row, tableBody);

   var row = createTableRow(false, [
      { content: "clade" },
      { content: taxonomy.clade },
   ]);
   appendChild(row, tableBody);

   var row = createTableRow(false, [
      { content: "genus" },
      { content: taxonomy.genus },
   ]);
   appendChild(row, tableBody);

   var row = createTableRow(false, [
      { content: "species" },
      { content: taxonomy.species },
   ]);

   appendChild(row, tableBody);

   appendChild(tableBody, taxonomyTable);

   return taxonomyTable;
}
