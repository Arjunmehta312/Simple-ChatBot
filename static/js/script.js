document.getElementById("chatForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent form submission

    // Get user input
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const message = document.getElementById("message").value;

    // Validate input
    if (!firstName || !lastName || !message) {
        alert("Please fill out all fields!");
        return;
    }

    // Send data to the backend
    try {
        const response = await fetch("/generate-response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                message: message,
            }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Display AI response
        document.getElementById("responseText").textContent = data.response;

    } catch (error) {
        console.error("Error fetching response:", error);
        document.getElementById("responseText").textContent =
            "An error occurred. Please try again.";
    }
});
