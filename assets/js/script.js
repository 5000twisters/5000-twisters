document.addEventListener("DOMContentLoaded", function() {
    var allInCounter = 0;
  
    function updateCounter() {
      allInCounter++;
      document.getElementById("all-in-counter").textContent = allInCounter;
  
      var progress = (allInCounter / 5000) * 100;
      document.getElementById("all-in-progress").style.width = progress + "%";
    }
  
    var form = document.getElementById("registration-form");
    form.addEventListener("submit", function(event) {
      var commitment = form.elements["commitment"].value;
      if (commitment === "in") {
        updateCounter();
      }
      // Additional form submission handling, e.g., sending data to Formspree
      // ...
  
      event.preventDefault(); // Prevent the form from submitting normally
      form.reset(); // Reset the form fields
      // Show the thank you message or redirect to a success page
      // ...
    });
  });