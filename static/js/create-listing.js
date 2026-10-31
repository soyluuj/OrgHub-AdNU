console.log("Create Listing JS Loaded!");

const imageInput = document.getElementById("imageInput");
const previewGrid = document.getElementById("previewGrid");
const imageCount = document.getElementById("imageCount");
const dropArea = document.getElementById("dropArea");

let selectedFiles = [];

const MAX_IMAGES = 5;

function syncFileInput() {

    const dataTransfer = new DataTransfer();

    selectedFiles.forEach(file => {
        dataTransfer.items.add(file);
    });

    imageInput.files = dataTransfer.files;

}

function refreshPreview() {

    previewGrid.innerHTML = "";

    imageCount.textContent =
        `${selectedFiles.length} / ${MAX_IMAGES} image(s) selected`;

    selectedFiles.forEach((file, index) => {

        const reader = new FileReader();

        reader.onload = function (e) {

            const card = document.createElement("div");

            card.className = "preview-item";

            card.innerHTML = `
                <img src="${e.target.result}" alt="Preview">

                <button
                    type="button"
                    class="remove-image"
                    data-index="${index}">
                    ×
                </button>
            `;

            previewGrid.appendChild(card);

        };

        reader.readAsDataURL(file);

    });

}

/* -----------------------------
   File Picker
----------------------------- */

imageInput.addEventListener("change", (event) => 
{

    const files = [...event.target.files];

    files.forEach(file => 
    {

        if (selectedFiles.length >= MAX_IMAGES) 
        {

            alert("Maximum of 5 images.");

            return;
        }

        if (!file.type.startsWith("image/")) {

            alert(`${file.name} is not an image.`);

            return;
        }

        if (file.size > 5 * 1024 * 1024) {

            alert(`${file.name} exceeds the 5 MB limit.`);

            return;
        }
        const exists = selectedFiles.some(f =>
            f.name === file.name &&
            f.size === file.size
        );

        if (!exists) {
            selectedFiles.push(file);
        }
    });
    
    syncFileInput();
    refreshPreview();


});

previewGrid.addEventListener("click", (event) => {

    if (!event.target.classList.contains("remove-image"))
        return;

    const index = Number(event.target.dataset.index);

    selectedFiles.splice(index, 1);

    syncFileInput();
    refreshPreview();

});

dropArea.addEventListener("dragover", (event) => {

    event.preventDefault();

    dropArea.style.borderColor = "#ffffff";
    dropArea.style.background = "rgba(255,255,255,.10)";

});

dropArea.addEventListener("dragleave", () => {

    dropArea.style.borderColor = "rgba(255,255,255,.45)";
    dropArea.style.background = "transparent";

});

dropArea.addEventListener("drop", (event) => {

    event.preventDefault();

    dropArea.style.borderColor = "rgba(255,255,255,.45)";
    dropArea.style.background = "transparent";

    const files = [...event.dataTransfer.files];

    files.forEach(file => {

        if (selectedFiles.length >= MAX_IMAGES)
            return;

        if (!file.type.startsWith("image/"))
            return;

        if (file.size > 5 * 1024 * 1024)
            return;

        const exists = selectedFiles.some(f =>
            f.name === file.name &&
            f.size === file.size
        );

        if (!exists) {
            selectedFiles.push(file);
        }

    });

    syncFileInput();
    refreshPreview();

});