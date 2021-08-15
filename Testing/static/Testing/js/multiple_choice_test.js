function answer_click(answer_container) {
    checkbox = answer_container.getElementsByTagName('input')[0];
    if (!answer_container.classList.contains('selected')) {
        answer_container.classList.add('selected');
        checkbox.checked = true;
    } else {
        answer_container.classList.remove('selected');
        checkbox.checked = false;
    }
}
