register("ChuckNorisJoke", chuckNorisEval());

function chuckNorisEval(url, position, widgetType, context) {
    restCall(url, chuckNorisCallback, position, queryString);
}

function chuckNorisCallback(json, position) {
    const formatedHtml = chuckNorisHtml.format(json.value.joke);
    changeWidget(position, formatedHtml);
}