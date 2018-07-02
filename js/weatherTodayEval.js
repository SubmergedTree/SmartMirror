register("weatherToday", weatherTodayEval);

function weatherTodayEval(url, position, widgetType, context) {
    restCall(url + context, weatherTodayCallback, position, context);
}

function weatherTodayCallback(json, position) {
    const formatedHtml = weatherTodayHtml.format(json.name, json.main.humidity, json.main.temp);
    changeWidget(position, formatedHtml);
}