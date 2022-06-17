// div element in which the contents of all the pages are to rendered
var rootElement = document.getElementById("root");

/**
 * Displays content of the home page
 * @returns {void} Nothing
 */
function Home() {
   rootElement.innerHTML = "";

   var heading = setUpElement("h2", ["text-center"], "Home page");
   appendChild(heading, rootElement);
}

/**
 * Displays content of the Proteins page
 * @returns {void} Nothing
 */
function Proteins() {
   rootElement.innerHTML = "";

   var heading = setUpElement("h2", ["text-center"], "Proteins page");
   appendChild(heading, rootElement);
}

/**
 * Displays content of the pfams page
 * @returns {void} Nothing
 */
function Pfams() {
   rootElement.innerHTML = "";

   var heading = setUpElement("h2", ["text-center"], "Pfams page");
   appendChild(heading, rootElement);
}
