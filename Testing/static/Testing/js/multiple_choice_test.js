function answer_click(answer_container) {
    let checkbox = answer_container.getElementsByTagName('input')[0];
    if (!answer_container.classList.contains('selected')) {
        answer_container.classList.add('selected');
        checkbox.checked = true;
    } else {
        answer_container.classList.remove('selected');
        checkbox.checked = false;
    }
}


function solution_check(e, form) {
    let inputs = form.getElementsByTagName("input");
    for (let i = 0; i < inputs.length; ++i) {
        if (inputs[i].getAttribute("type") === "checkbox" && inputs[i].checked) {
            return;
        }
    }
    e.preventDefault();
    let answers_container = form.children[2];
    if (!answers_container.classList.contains("error_answers")) {
        answers_container.classList.add("error_answers");
        let paragraph = document.createElement("p");
        paragraph.innerText = "Оберіть варіант відповіді";
        paragraph.className = "error";
        answers_container.insertBefore(paragraph, answers_container.firstChild);
    }
}
