document.addEventListener('DOMContentLoaded', function() {
    // default load
    hideView();

    // new post
    document.querySelector('#newPostButton').addEventListener('click', () => newPost());
    document.querySelector('#hideNew').addEventListener('click', () => hideView());
    document.querySelector('#postForm').onsubmit = hideView;
    
    // edit post
    document.querySelector('#editButton').addEventListener('click', () => editPost());
    document.querySelector('#editForm').onsubmit = saveEdit;

})

function newPost() {
    document.querySelector('#newPost').style.display = 'block';
    document.querySelector('#newPostButton').style.display = 'none';
    document.querySelector('#post').value = '';
}

function hideView() {
    document.querySelector('#newPost').style.display = 'none';
    document.querySelector('#newPostButton').style.display = 'block';
}


function follow() {
    const username = document.querySelector('#profileUser');
    console.log(username);
    if (document.querySelector('#followButton').value = 'Follow') {
        const followAction = 'unfollow';
    }
    else {
        const followAction = 'follow';
    }

    fetch(`profile/${ username }`, {
        method: 'PUT',
        body: JSON.stringify({
            followAction: followAction,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
}

function editPost() {
    const text = document.querySelector('#postText').innerHTML;

    document.querySelector('#postText').style.display = 'none';
    document.querySelector('#editButton').style.display = 'none';
    document.querySelector('#editForm').style.display = 'block';
    document.querySelector('#saveButton').style.display = 'inline-block';
    document.querySelector('#postTextArea').value = text;
}

function saveEdit() {
    const text = document.querySelector('#postTextArea').value;

    document.querySelector('#postText').style.display = 'block';
    document.querySelector('#editButton').style.display = 'inline-block';
    document.querySelector('#editForm').style.display = 'none';
    document.querySelector('#saveButton').style.display = 'none';
    
    document.querySelector('#postText').innerHTML = text;
}
