registrationsAfterRestCall.push(new Registration("ChuckNorisJoke", chuckNorisEval()));

function chuckNorisEval(url, position, widgetType, queryString) {
    //changeWidget(position, chuckNorisHtml);
    restCall(url, chuckNorisCallback, position, queryString)
}

function chuckNorisCallback(json, position) {

}