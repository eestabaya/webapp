let infoCardShown = false;

document.addEventListener("DOMContentLoaded", function () {
    let image = imageInfo['image'],
        originalCreator = imageInfo['original_creator'],
        sourceType = imageInfo['source_type']

    document.getElementById("modal-image").src = image;
    document.getElementById("image-link").href = image;
    document.getElementById("image-link-info").innerText = image;
    document.getElementById("original-creator-info").innerText = originalCreator;
    document.getElementById("source-type-info").innerText = sourceType;
})


function revealInfoCard() {
    infoCardShown = !infoCardShown;
    let infoCard = document.getElementById("info-card");

    if (infoCardShown) {
        infoCard.style.display = "block"
    } else {
        infoCard.style.display = "none"
    };
}