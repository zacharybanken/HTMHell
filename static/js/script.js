document.addEventListener("click", function (event) {
    console.log("Click detected on:", event.target);  // Log the clicked element
    // Check if the clicked element is a link (A tag)
    if (event.target.tagName === "A") {
        event.preventDefault();  // Prevent default link behavior

        let clickedId = event.target.id;
        let currentHTML = document.documentElement.outerHTML;  // Capture full page HTML
        console.log("Sending request to server...");  // Log before sending the request

        // Send POST request to the FastAPI server
        fetch("http://localhost:8000/generate_html/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ html: currentHTML, clicked_id: clickedId })  // Send data as JSON
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            // Ensure the response contains generated HTML
            if (data.html) {
                document.open();  // Clears the current page
                document.write(data.html);  // Writes the AI-generated HTML
                document.close();  // Closes the document to render the new HTML
            } else {
                console.error("Error: No HTML returned from the server.");
            }
        })
        .catch(error => {
            console.error("Error during fetch:", error);  // Catch and log any fetch errors
        });
    }
});
