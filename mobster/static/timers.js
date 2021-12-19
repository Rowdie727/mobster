document.addEventListener('DOMContentLoaded', function() {
    let current_health = document.querySelector('span#current_health');
    let max_health = document.querySelector('span#max_health');
    let user = document.querySelector('#user');
    let time = ((Number(max_health.innerHTML) - Number(current_health.innerHTML)) * 12)
    let clock = document.querySelector('#clock');
    
    if (Number(current_health.innerHTML) < Number(max_health.innerHTML)) {
        const interval = setInterval(() => {
            if (time < 1) {
                clearInterval(interval);
                clock.style.display = 'none';
                current_health.innerHTML = max_health.innerHTML;
                alert('You have been healed!')
            }
            clock.hidden = false;
            clock.innerHTML = time + 's';
            time--;

        }, 1000)
    }
});
