var inline_form_template = null
var inline_form_conteiner = null
var prefixes = null
var inline_form_max_index = 0

function set_inline_form_template(container_class, prefix) {
    prefixes = [prefix, "id_" + prefix];
    let form = document.getElementsByClassName(container_class)[0];
    inline_form_conteiner = form.parentNode;
    inline_form_template = form.cloneNode(true);
    inline_form_max_index = document.getElementsByClassName(inline_form_template.className).length - 1;
}

function change_attributes(nodes, index) {
    for (let n = 0; n < nodes.length; n++) {
        let node = nodes[n];
        if (node.childNodes)
            change_attributes(node.childNodes, index);
        if (node.attributes) {
            for (let i = 0; i < node.attributes.length; i++) {
                let attrib = node.attributes[i];
                if (attrib.specified) {
                    for (let p = 0; p < prefixes.length; p++) {
                        let pref = prefixes[p];
                        if (attrib.value.substring(0, pref.length) === pref) {
                            attrib.value = pref + String(index) +
                                attrib.value.substring(pref.length + 1, attrib.value.length);
                            break;
                        }
                    }
                }
            }
        }
    }
}

function add_inline_form() {
    let new_form = inline_form_template.cloneNode(true);
    inline_form_conteiner.appendChild(new_form);
    change_attributes(new_form.childNodes, ++inline_form_max_index);
    document.getElementById(prefixes[1] + "TOTAL_FORMS").setAttribute("value", inline_form_max_index + 1);
}
