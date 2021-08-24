const linkPlaceholder = "12345678901234567890";

function linkToTest(inputList) {
    let link = document.getElementById("id_link");

    let value = "";
    let options = document.getElementById(inputList.getAttribute("list")).getElementsByTagName("option");
    for (let i = 0; i < options.length; ++i) {
        if (inputList.value == options[i].value) {
            value = options[i].getAttribute("data-value");
            break;
        }
    }

    if (value) {
        link.setAttribute("href", link.getAttribute("data-link").replace(
            linkPlaceholder, value
        ));
    } else {
        link.removeAttribute("href");
    }
}
