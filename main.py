from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


browser = webdriver.Chrome()
browser.get('https://quacs.org/fall2023/#')
time.sleep(1)
f = open('data.json', 'w', encoding='utf-8')
"""
result = {
    "metadata": {
        "Title": "...", 
        "Contributors": ["..."],
        "Source": "...",
        "Date": "...", 
        "Description": "..."
    }
    "data":{
        "Fall_2023": {
            "1": {  # Monday
                "8": {  # 8:00
                    "count": 0,
                    "majors": {
                        "ITWS": {
                            "count": 0,
                            "courses": {}
                        }, 
                        ...
                    }
                },
                ...
            },
            ...
        }, 
        ...
    }
}
"""
result_result = {
    "Fall_2023": {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {}
    }
}
for i in range(6, 24):  # 8:00 - 22:00
    for j in range(1, 6):  # Monday - Friday
        result_result['Fall_2023'][j][i] = {
            "count": 0,
            "majors": {}
        }

majors = browser.find_elements(By.CLASS_NAME, "department-code")
for x, y in enumerate(majors):  # loop through every major
    i = browser.find_elements(By.CLASS_NAME, "department-code")[x]
    text = i.text
    i.click()
    time.sleep(1)
    classes = browser.find_elements(By.CLASS_NAME, "card-header")
    temp = []
    for i, j in enumerate(classes):  # loop through every class, x is index and y is content
        each_text = j.text
        class_title = each_text[:9]
        major_name = class_title[:4]  # e.g. ITWS
        class_name = major_name + class_title[5:]  # e.g. ITWS-1100
        # section part   //*[@id="measuringWrapper-ARCH-2160"]/div/table/tbody/tr[1]/td[1]/span[1]
        j.click()
        time.sleep(1)
        div_class_name = "section-grow-" + class_title
        x_path = "//div[@id='" + div_class_name + "']/div/div/table/tbody/tr"
        sections = browser.find_elements(By.XPATH, x_path)
        for a, b in enumerate(sections):  # loop through every section
            temp_path = x_path + "[" + str(a+1) + "]/"
            for date in range(5):  # loop through every day
                temp = temp_path + "td[" + str(date+2) + "]/span[1]"
                element = browser.find_elements(By.XPATH, temp)
                if not element:  # no time
                    continue
                span_number = 2
                while element[0].text.strip() == "":  # time is not in the first span
                    temp = temp_path + "td[" + str(date+2) + "]/span[" + str(span_number) + "]"
                    element = browser.find_elements(By.XPATH, temp)
                    if not element:
                        break
                    span_number += 1
                if not element:
                    continue
                time_used = element[0].text.strip()
                print(major_name, class_name, "section:", a+1, date+1, time_used)
                if time != "":  # e.g. 10:00a-11:50a
                    time_used = time_used.split('-')
                    start_time = int(time_used[0].split(':')[0])
                    end_time = int(time_used[1].split(':')[0]) + 1
                    if time_used[0][-1] == 'p':
                        start_time += 12 if start_time != 12 and start_time != 13 else 0
                        end_time += 12 if end_time != 12 and end_time != 13 else 0
                    print(date+1, start_time, end_time)
                    for hour in range(start_time, end_time + 1):
                        if major_name not in result_result['Fall_2023'][date+1][hour]["majors"]:
                            result_result['Fall_2023'][date + 1][hour]["count"] += 1
                            result_result['Fall_2023'][date+1][hour]["majors"][major_name] = {
                                "count": 1,
                                "courses": {class_name}
                            }
                        else:
                            if class_name not in result_result['Fall_2023'][date+1][hour]["majors"][major_name]["courses"]:
                                result_result['Fall_2023'][date + 1][hour]["count"] += 1
                                result_result['Fall_2023'][date+1][hour]["majors"][major_name]["count"] += 1
                                result_result['Fall_2023'][date+1][hour]["majors"][major_name]["courses"].add(class_name)
    browser.back()  # finished whole major, go back to main page
    time.sleep(1)
browser.quit()
for i in result_result['Fall_2023']:
    for j in result_result['Fall_2023'][i]:
        if result_result['Fall_2023'][i][j]["count"] != 0:
            for k in result_result['Fall_2023'][i][j]["majors"]:
                result_result['Fall_2023'][i][j]["majors"][k]["courses"] = list(result_result['Fall_2023'][i][j]["majors"][k]["courses"])
json.dump(result_result, f)
f.close()
