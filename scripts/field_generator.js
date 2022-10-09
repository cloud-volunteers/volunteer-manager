function generateInside(name, placeholder, jinja){
    var readonly = ""
    var type = "text"
    var required = ""

    if(jinja == "None")
        jinja = ""

    if("id" == name){
        readonly = "readonly"
        type = "number"
        required = "required"
    }
    else if("email" == name){
        type = "email"
        required = "required"
    }
    else if(("online" == name) || ("offline" == name) || ("active" == name))
        type = "checkbox"
        
    else if("age" == name)
        type = "number"

    let label = `<label for = \"${name}\" class = \"align-middle\">${placeholder}</label>`
    let input = 
    `<input name = \"${name}\" type = \"${type}\" placeholder = \"${placeholder}\" value = \"${jinja}\" ${readonly} ${required} class = \"m-1 bg-slate-200 border-2 border-solid border-slate-600 shadow-md shadow-slate-300 dark:text-black\" />`
    let labelDiv = `<div class = \"w-[25%]\">${label}</div>`
    let inputDiv = `<div class = \"w-[25%] text-end\">${input}</div>`
    return labelDiv + inputDiv;
}

function generateOutside(name, placeholder, jinja){
    return `<div class = \"flex flex-row place-content-center m-2\">${generateInside(name, placeholder, jinja)}</div>`;
}

globalThis.generateOutside = generateOutside;