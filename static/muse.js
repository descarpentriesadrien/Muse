document.addEventListener('DOMContentLoaded', () => {

    if (document.querySelector('.like-button')) {
        likeArt();
    }
    if (document.querySelector('#viewer-container')) {
        openSeaDragon();
    }
});

// Toggle a like/unlike function with like/unlike buttons in table
function likeArt() {
    // Get all rows
    const artRows = document.querySelectorAll('.art-row');

    // In each row, get the like button and the record ID associated
    artRows.forEach(art => {
        const likeButton = art.querySelector('.like-button');
        const recordId = likeButton.dataset.id;

        // On click, send a POST request
        likeButton.addEventListener('click', () => {
            fetch(`like/${recordId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            })
                .then(response => response.json())
                .then(result => {
                    console.log('Success:', result);

                    // According to response, change from like to unlike
                    if (result.status === 'liked') {
                        likeButton.innerHTML = '<i class="bi bi-heart-fill"></i> Unlike';
                    } else if (result.status === 'unliked') {
                        likeButton.innerHTML = '<i class="bi bi-heart"></i> Like';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
}


// Set up for OpenSeaDragon viewer container
function openSeaDragon() {

    const viewerContainer= document.getElementById('viewer-container');
    const url = viewerContainer.dataset.url;
    const placeholder = viewerContainer.dataset.placeholder;

    // OpenSeadragon Viewer setup
    const viewer = OpenSeadragon({
        id: "openseadragon-viewer",
        prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
        tileSources: {
            type: 'image',
            url: url,
            placeholder: placeholder
        },
        showNavigator: true,
        showLoading: true,
        immediateRender: true,
        visibilityRatio: 1.0,
        constrainDuringPan: true,
    });

    // When tiles finish loading hide the spinner
    viewer.addHandler("open", () => {
        document.getElementById("loading-spinner").style.display = "none";
        document.getElementById("load-message").style.display = "none";
        startTime = Date.now();
    });
}
