const inline_form_attr = "data-inline-prefix";
const inline_form_wrapper_attr = "data-inline-form";

class InlineFormset {
    constructor(formset_wrapper) {
        let form_wrappers = formset_wrapper.querySelectorAll('[' + inline_form_wrapper_attr + ']');
        let template_element = form_wrappers[form_wrappers.length - 1];
        let prefix = template_element.getAttribute(inline_form_wrapper_attr);
        this.prefixes = [prefix, "id_" + prefix];
        this.container = template_element.parentNode;
        this.form = template_element.cloneNode(true);
        this.max_index = this.container.querySelectorAll('[' + inline_form_wrapper_attr + ']').length - 1;
    }

    change_attributes(nodes) {
        for (let n = 0; n < nodes.length; n++) {
            let node = nodes[n];
            if (node.childNodes)
                this.change_attributes(node.childNodes);
            if (node.attributes) {
                for (let i = 0; i < node.attributes.length; i++) {
                    let attrib = node.attributes[i];
                    if (attrib.specified) {
                        for (let p = 0; p < this.prefixes.length; p++) {
                            let pref = this.prefixes[p];
                            if (attrib.value.substring(0, pref.length) === pref && attrib.name != inline_form_attr) {
                                attrib.value = pref + String(this.max_index) +
                                    attrib.value.substring(pref.length + 1, attrib.value.length);
                                break;
                            }
                        }
                    }
                }
            }
        }
    }

    add_inline_form() {
        let new_form = this.form.cloneNode(true);
        this.container.appendChild(new_form);
        this.max_index += 1;
        this.change_attributes(new_form.childNodes);
        document.getElementById(this.prefixes[1] + "TOTAL_FORMS").setAttribute("value", this.max_index + 1);
    }
}

var inline_formsets = new Map();

function add_inline_formset() {
    let formsets = document.querySelectorAll('[' + inline_form_attr + ']');
    for (let i = 0; i < formsets.length; ++i) {
        inline_formsets.set(formsets[i].getAttribute(inline_form_attr), new InlineFormset(formsets[i]));
    }
}
