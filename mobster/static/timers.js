document.addEventListener('DOMContentLoaded', function() {
    let current_health = document.querySelector('span#current_health');
    let max_health = document.querySelector('span#max_health');
    let health_time = ((Number(max_health.innerHTML) - Number(current_health.innerHTML)) * 20)
    let health_clock = document.querySelector('#health_clock');
    let energy_time = ((Number(max_energy.innerHTML) - Number(current_energy.innerHTML)) * 20)
    let energy_clock = document.querySelector('#energy_clock');
    
    if (Number(current_health.innerHTML) < Number(max_health.innerHTML)) {
        const interval = setInterval(() => {
            if (health_time < 1) {
                clearInterval(interval);
                health_clock.style.display = 'none';
            }
            health_clock.hidden = false;
            health_clock.innerHTML = health_time + 's';
            health_time--;

        }, 1000)
    }

    if (Number(current_energy.innerHTML) < Number(max_energy.innerHTML)) {
        const interval = setInterval(() => {
            if (energy_time < 1) {
                clearInterval(interval);
                energy_clock.style.display = 'none';
            }
            energy_clock.hidden = false;
            energy_clock.innerHTML = energy_time + 's';
            energy_time--;

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

function test() {
    alert('Testing!')
}