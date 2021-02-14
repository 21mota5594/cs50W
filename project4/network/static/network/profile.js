document.addEventListener('DOMContentLoaded', function() {
    // profile page
    document.querySelector('#followButton').addEventListener('click', () => follow());
})

function follow() {
    const username = document.querySelector('#profileUser').innerHTML;
    console.log(username);
    let followAction = ''
    if (document.querySelector('#followButton').innerHTML === "Follow") {
        followAction = 'follow';
    }
    else {
        followAction = 'unfollow';
    }
    console.log(followAction);
    fetch(`/follow/${ username }`, {
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

    if (followAction === 'follow') {
        document.querySelector('#followButton').innerHTML = 'Unfollow';
        console.log(followAction);
    }
    else {
        document.querySelector('#followButton').innerHTML = 'Follow';
        console.log(followAction);
    }
}
