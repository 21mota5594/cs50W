document.addEventListener('DOMContentLoaded', function() {
    // default load
    hideView();

    // new post
    document.querySelector('#newPostButton').addEventListener('click', () => newPost());
    document.querySelector('#hideNew').addEventListener('click', () => hideView());
    document.querySelector('#postForm').onsubmit = postForm;
    
    // edit post
    document.querySelector('#editButton').addEventListener('click', () => editPost());
    document.querySelector('#editForm').onsubmit = saveEdit;

})

function newPost() {
    document.querySelector('#newPost').style.display = 'block';
    document.querySelector('#newPostButton').style.display = 'none';
    document.querySelector('#postMessage').style.display = 'none';
}

function hideView() {
    document.querySelector('#newPost').style.display = 'none';
    document.querySelector('#newPostButton').style.display = 'block';
    document.querySelector('#postMessage').style.display = 'none';
}

function postForm() {
    const post = document.querySelector('#post').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(post);
    const request = new Request(
        '/post',
        {
            headers: {'X-CSRFToken': csrftoken},
            method: "POST"
        }
    );
    console.log(request);
    fetch(request, {
        body: JSON.stringify({
            post: post
        }),
        mode: 'same-origin'
      })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    
    document.querySelector('#post').value = '';
    hideView();
    document.querySelector('#postMessage').style.display = 'block';
    return false;
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
    const previousText = document.querySelector('#postText').innerHTML;

    document.querySelector('#postText').style.display = 'block';
    document.querySelector('#editButton').style.display = 'inline-block';
    document.querySelector('#editForm').style.display = 'none';
    document.querySelector('#saveButton').style.display = 'none';
    
    document.querySelector('#postText').innerHTML = text;

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/edit',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    console.log(request);
    fetch(request, {
        method: 'PUT',
        method: 'same-origin',
        body: JSON.stringify({
            oldText: previousText,
            newText: text
        })
      })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    return false;
}