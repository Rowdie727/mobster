
// This controlls the page being displayed on made_men

function showPage(page) {
    document.querySelectorAll('.page-section').forEach(div => {
        div.style.display = 'none';
    })
    document.querySelector(`#${page}`).style.display = 'block';
}


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.made-men-btn').forEach(button => {
        button.onclick = function() {
            showPage(this.dataset.page);
        }
    });
});
