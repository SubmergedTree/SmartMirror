register("weatherForecast", weatherForecastEval);

function weatherForecastEval(url, position, widgetType, context) {
    restCall(url + context, weatherForecastCallback, position, context);
}

function weatherForecastCallback(json, position) {
    const formatedHtml = weatherForecastHtml.format(json.list[0].dt_txt, json.list[0].clouds.all, json.list[0].main.humidity,
                                                    json.list[1].dt_txt, json.list[1].clouds.all, json.list[1].main.humidit);
    changeWidget(position, formatedHtml);
}