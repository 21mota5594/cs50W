document.addEventListener('DOMContentLoaded', function() {
    // favorite button
    document.querySelector('#addButton').addEventListener('click', () => favMovie());
})

function favMovie() {
    const title = document.querySelector('#movieTitle').innerHTML;
    const img = document.querySelector('#movieImg');
    const url = img.src;
    const id = document.querySelector('#hiddenID').value.split('/')[2];
    console.log(`${title} ${id}`);
    console.log(id)
    let action = ''
    if(document.querySelector('#addButton').innerHTML === 'Add to favorites') {
        action = 'favorite'
    }
    else {
        action = 'unfavorite'
    }
    console.log(action)
    fetch('/favorite', {
        method: 'PUT',
        body: JSON.stringify({
            action: action,
            title: title,
            url: url,
            id: id
        })
    })
    .then(response => response.json())
    .then(result => {
        // print result
        console.log(result);
    });

    if(document.querySelector('#addButton').innerHTML === 'Add to favorites') {
        document.querySelector('#addButton').innerHTML = 'Remove from favorites'
    }
    else {
        document.querySelector('#addButton').innerHTML = 'Add to favorites'
    }
}