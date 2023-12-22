const loadLimit = 32;
let infoCardShown = false,
    curCol = 0,
    loading = false,
    columns = document.getElementsByClassName('column')

document.addEventListener("DOMContentLoaded", () => {
    loadImages(); // initial image load

})

function changePage(n) {
    if (pageNumber == 1 && n == -1) {return};
    if (n == -1) {pageNumber -= 1} else {pageNumber++}

    window.location.replace(redirectUrl + "?limit=" + loadLimit + "&page=" + pageNumber)
}

function loadImages() {
    url = images_api_url + "?limit=" + loadLimit + "&page=" + pageNumber

    fetchJSONData(url)
        .then(data => {
            data.result.forEach(image => {
                addImageToGallery(image)
            })
        });

    loading = false;
}

function handleScroll() {
    let grid = document.getElementById("image-grid");
    let isScrollAtBottom = ((grid.scrollTop + grid.clientHeight) / grid.scrollHeight >= 0.7);

    if (isScrollAtBottom && !loading) {
        loadImages();
        loading = true;
    }
}

function getColumnIndex() {
    let columnHeights = [];
    for (let i = 0; i < columns.length; i++) {
        columnHeights.push(getColHeight(columns[i]))
    }

    const min = Math.min.apply(null, columnHeights)
    return columnHeights.indexOf(min);
}

function getColHeight(col) {
    var totalHeight = 0;
    for (let i = 0; i < col.children.length; i++) {
        totalHeight = totalHeight + col.children[i].clientHeight;
    }
    return totalHeight
}

function addImageToGallery(imageInfo) {
    column = columns[getColumnIndex()]
    
    let image = imageInfo['image'],
        cw = imageInfo['cw'];

    let newImage = document.createElement("img");

    newImage.src = image;
    newImage.className = "gallery_img";
    newImage.setAttribute("draggable", "false");
    if (cw > 2) {newImage.classList.add("blur")};

    newImage.addEventListener("click", () => {
        // open thing in new tab, EX:
        let imageWindow = 'https://litdab.xyz/idfktheendpoint?hash=iforgothowiwassupposedtoaccesstheimage'
        window.open(imageWindow, "_blank")
    })

    column.appendChild(newImage);
}

function fetchJSONData(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not OK");
            }
            return response.json();
        })
        .catch(error => {
            console.error("Error fetching JSON data:", error);
        });
}
