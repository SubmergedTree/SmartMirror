register("ChuckNorisJoke", chuckNorisEval);

function chuckNorisEval(url, position, widgetType, context) {
    alert(url);
    alert(position);
    alert(widgetType);
    alert(context);
    restCall(url, chuckNorisCallback, position, context);
}

function chuckNorisCallback(json, position) {
    const formatedHtml = chuckNorisHtml.format(json.value.joke);
    changeWidget(position, formatedHtml);
}