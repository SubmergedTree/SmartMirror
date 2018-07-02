register("catFacts", catFactsEval);

function catFactsEval(url, position, widgetType, context) {
    restCall('https://cors-anywhere.herokuapp.com/' + url, catFactsCallback, position, context);
}

function catFactsCallback(json, position) {
    const formatedHtml = catFactsHtml.format(json.fact);
    changeWidget(position, formatedHtml);
}