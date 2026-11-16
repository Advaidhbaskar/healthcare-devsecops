
const form = document.getElementById("appointment-form");
const result = document.getElementById("result");
const dateInput = document.getElementById("date");

// Prevent booking dates in the past.
dateInput.min = new Date().toISOString().split("T")[0];

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    result.textContent = "Processing appointment...";

    try {
        const response = await fetch("/book", {
            method: "POST",
            body: new FormData(form)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Booking failed");
        }

        result.textContent = data.message;
        form.reset();
        dateInput.min = new Date().toISOString().split("T")[0];

    } catch (error) {
        result.textContent = error.message;
    }
});
