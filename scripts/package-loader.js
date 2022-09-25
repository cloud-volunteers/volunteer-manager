packages = ["https://unpkg.com/htmx.org@1.8.0", 
            "https://unpkg.com/hyperscript.org@0.9.7", 
            "./multilang.js"
        ]

packages.forEach(element => {
    var script = document.createElement('script');
    script.src = element;
    if(script.src.includes("multilang.js")){
        script.addEventListener("onload", function(){ globalThis.multilang = new MultiLang('languages.json')})
        //script.setAttribute("_", "on load trigger multilangLoad on .multilang")
        console.log(script)
    }
    document.head.append(script);
});