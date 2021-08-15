function changeSelectedValue(inputList) {
    let hiddenInput = getHiddenInput(inputList);
    let value = "";
    let options = getDataList(inputList).getElementsByTagName("option");
    for (let i = 0; i < options.length; ++i) {
        if (inputList.value == options[i].value) {
            value = options[i].getAttribute("data-value");
            break;
        }
    }
    hiddenInput.value = value;
}

function setSelected(inputList, selectedValue) {
    console.log(selectedValue)
    let options = getDataList(inputList).getElementsByTagName("option");
    for (let i = 0; i < options.length; ++i) {
        if (selectedValue == options[i].getAttribute("data-value")) {
            inputList.value = options[i].value;
            break;
        }
    }
    inputList.onchange();
}

function getHiddenInput(inputList) {
    return document.getElementById(
        "id_" + inputList.getAttribute("list").substring(5)
    )
}

function getDataList(inputList) {
    return document.getElementById(inputList.getAttribute("list"))
}
