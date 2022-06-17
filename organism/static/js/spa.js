/**
 * A function that allows navigations between different pages
 * @param {String} component the component to be displayed
 */
function navigate(component) {
   if (component == "home") {
      Home();
   }
   if (component == "proteins") {
      Proteins();
   }
   if (component == "pfams") {
      Pfams();
   }
}
