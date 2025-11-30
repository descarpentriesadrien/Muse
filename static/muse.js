document.addEventListener('DOMContentLoaded', () => {

        if (document.querySelector('.like-button')) {
            likeArt();
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


function seaDragon
