document.addEventListener('DOMContentLoaded', function() {
    let current_health = document.querySelector('span#current_health');
    let max_health = document.querySelector('span#max_health');
    let time = ((Number(max_health.innerHTML) - Number(current_health.innerHTML)) * 20)
    let clock = document.querySelector('#clock');
    
    if (Number(current_health.innerHTML) < Number(max_health.innerHTML)) {
        const interval = setInterval(() => {
            if (time < 1) {
                clearInterval(interval);
                clock.style.display = 'none';
            }
            clock.hidden = false;
            clock.innerHTML = time + 's';
            time--;

        }, 1000)
    }
});


setInterval(function() {
    fetch('/user_json').then(
        response => response.json()
    ).then(
        data => 
            data.forEach(match => 
                updateElement(match)    
            )
    )
}, 1000

);

function updateElement(match) {
    Object.entries(match).forEach(([k,v]) => {
        element = document.getElementById(k);
        previousValue = element.innerHTML;
        if (previousValue !== v.toString()) {
            element.innerHTML = v.toString();
        }
    })
}