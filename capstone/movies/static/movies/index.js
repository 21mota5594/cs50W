document.addEventListener('DOMContentLoaded', function() {
    // recommendation button
    document.querySelector('#recommendForm').addEventListener('submit', () => recommendations())
})

function recommendations() {
    let cardExists = document.getElementsByClassName('.nullCard');
    console.log(cardExists);
    if (document.getElementsByClassName('.nullCard').length !== 0) {
        window.alert("Complete favorite movies before recommendations!");
        console.log(cardExists);
        return false;
    }
}