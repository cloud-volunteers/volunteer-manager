function generateInside(name, placeholder){
    let label = `<label for = \"${name}\" class = \"align-middle\">${placeholder}</label>`
    let input = 
    `<input name = \"${name}\" placeholder = \"${placeholder}\" value = \"{{ user.${name} }}\" class = \"m-1 bg-slate-200 border-2 border-solid border-slate-600 shadow-md shadow-slate-300 dark:text-black\" />`
    let labelDiv = `<div class = \"w-[25%]\">${label}</div>`
    let inputDiv = `<div class = \"w-[25%] text-end\">${input}</div>`
    return labelDiv + inputDiv;
}

function generateOutside(name, placeholder){
    return `<div class = \"flex flex-row place-content-center m-2\">${generateInside(name, placeholder)}</div>`;
}

globalThis.generateOutside = generateOutside;