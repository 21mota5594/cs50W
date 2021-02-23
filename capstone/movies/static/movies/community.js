document.addEventListener('DOMContentLoaded', function() {
    // default load
    defaultLoad();

    // tabs
    document.querySelectorAll('.profileTab').forEach(input => input.addEventListener('click', event => {
        console.log(event.id);
        return false;
    }));
})

function defaultLoad() {
    document.querySelectorAll('profileTab').forEach(a=>a.classList.add('active'));
    document.querySelectorAll('userProfile').forEach(a=>a.style.display('block'));

    document.querySelectorAll('favoritesTab').forEach(a=>a.classList.remove('active'));
    document.querySelectorAll('userFavorites').forEach(a=>a.style.display('none'));

    document.querySelectorAll('recommendedTab').forEach(a=>a.classList.remove('active'));
    document.querySelectorAll('userRecommended').forEach(a=>a.style.display('none'));
}

