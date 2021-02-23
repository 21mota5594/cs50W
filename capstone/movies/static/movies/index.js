document.addEventListener('DOMContentLoaded', function() {
    // default load
    document.querySelector('#recommendations').style.display = 'none';
    document.querySelector('#recommendButton').style.display = 'block';

    // recommendation button
    document.querySelector('#recommendButton').addEventListener('click', () => recommendations())
})

function recommendations() {
    let cardExists = document.getElementsByClassName('.nullCard');
    if (document.getElementsByClassName('.cardNull') !== null) {
        window.alert("Complete favorite movies before recommendations!");
    }
}