

假定allure生成的数据与core处于同级目录，
测试完毕之后，allure数据存放在report/html目录下

```
E:\MIRROR\TUTORIAL\SOURCECODE\SOFTWARETEST\自动化接口\PYTEST-AUTO-API2\REPORT\HTML
│   app.js
│   favicon.ico
│   index.html
│   styles.css
│
├───data
│   │   behaviors.csv
│   │   behaviors.json
│   │   categories.csv
│   │   categories.json
│   │   packages.json
│   │   suites.csv
│   │   suites.json
│   │   timeline.json
│   │
│   ├───attachments
│   │       13bfb57703e7690e.json
        ...
│   │       fcca81305c6a23d5.txt
│   │
│   └───test-cases                      # 存放所有的测试详细数据
│           485224bd0dd174a5.json
        ...
│           f242095ef3856bd9.json
│
├───export
│       influxDbData.txt
│       mail.html
│       prometheusData.txt
│
├───history
│       categories-trend.json
│       duration-trend.json
│       history-trend.json
│       history.json
│       retry-trend.json
│
├───plugins
│   ├───behaviors
│   │       index.js
│   │
│   ├───packages
│   │       index.js
│   │
│   └───screen-diff
│           index.js
│           styles.css
│
└───widgets
        behaviors.json
        categories-trend.json
        categories.json
        duration-trend.json
        duration.json
        environment.json
        executors.json
        history-trend.json
        launch.json
        retry-trend.json
        severity.json
        status-chart.json
        suites.json
        summary.json                # 存放测试统计数据，如pass数量，fail数量，良率等数据
```
