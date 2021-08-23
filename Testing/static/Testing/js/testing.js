function setTimeDelta() {
    let element = document.getElementById("testing_time");
    let endDateTime = new Date(element.getAttribute("data-end"));
    let difference = new Date(endDateTime - Date.now());
    if (difference < 30000) {
        let parent = element.parentNode;
        if (!parent.classList.contains("testing_time_warninig")) {
            parent.classList.add("testing_time_warninig");
        }
    }
    if (difference < 0) {
        window.location.replace(element.getAttribute("data-timeout-url"));
        clearInterval(SetTimeDeltaIntervalId);
    } else {
        let diff_years = difference.getUTCFullYear() - 1970;
        let diff_months = difference.getUTCMonth();
        let diff_days = difference.getUTCDate() - 1;
        let diff_hourse = difference.getUTCHours();
        let diff_minutes = difference.getUTCMinutes();
        let diff_seconds = difference.getUTCSeconds();

        let timeDeltaStr = "";
        if (diff_years > 0) { 
            timeDeltaStr += diff_years + " років "; 
        }
        if (diff_months > 0) { 
            timeDeltaStr += diff_months + " місяців "; 
        }
        if (diff_days > 0) {
            timeDeltaStr += diff_days + " діб "; 
        }
        if (diff_hourse > 0) {
            timeDeltaStr += diff_hourse + " год. "; 
        }
        if (diff_minutes > 0) { 
            timeDeltaStr += diff_minutes + " хв. "; 
        }
        if (diff_seconds > 0) { 
            timeDeltaStr += diff_seconds + " с. "; 
        }
        
        element.innerText = timeDeltaStr;
    }
}

window.onload = setTimeDelta;

var SetTimeDeltaIntervalId = setInterval(setTimeDelta, 1000);
