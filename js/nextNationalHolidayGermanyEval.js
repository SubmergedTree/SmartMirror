register("nextNationalHolidayGermany", nextNationalHolidayGermanyEval);

function nextNationalHolidayGermanyEval(url, position, widgetType, context) {
    const splittedContext = context.split(';');
    const finalUrl = url + '?jahr={0}&nur_land={1}'.format(splittedContext[0], splittedContext[1]);
    restCall(finalUrl, nextNationalHolidayGermanyCallback, position, "");
}

function nextNationalHolidayGermanyCallback(json, position) {
    const holidayList = getHolidayProperties_nextNationalHolidayGermany(json);
    const nextHoliday = getNextHoliday_nextNationalHolidayGermany(holidayList);

    const formatedHtml = nextNationalHolidayGermanyHtml.format(nextHoliday.name, nextHoliday.date);
    changeWidget(position, formatedHtml);
}

function getHolidayProperties_nextNationalHolidayGermany(json) {
    let holidayList = [];
    for (let day in json) {
        if(json.hasOwnProperty(day) ) {
          holidayList.push({
              name: day,
              date: json[day].datum
          })
        }
    }
    return holidayList;
}

function getNextHoliday_nextNationalHolidayGermany(holidayList) {
    const unixTimeNow = Date.now();
    for (let i = 0; i < holidayList.length; i++) {
        let unixTime = Date.parse(holidayList[i].date);
        if (unixTime >= unixTimeNow) {
            return holidayList[i];
        }
    }
}