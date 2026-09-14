function detectCoins() {

    const imageInput = document.getElementById("imageInput");

    if (imageInput.files.length === 0) {
        alert("Please select a coin image first!");
        return;
    }

    const formData = new FormData();

    formData.append("image", imageInput.files[0]);

    fetch("/detect", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("coinCount").textContent = data.count;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong!");
    });
}