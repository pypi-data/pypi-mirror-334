This package is designed for internal use only. Should you have any questions, please contact Zachary Yang via Teams or zachary.yang@tradeup.com

Release note 0.0.2   2023/10/18 13:55
Added Previous_BDay(), return previous business day
Added db_insert(), insert dataframes into database
Added data_pull, pull data from MySQL DB including original column names


Release note 0.0.3   2023/10/30 15:18
Added clear_table(), clear records based on customized conditions
Added last_business_day()

Release note 0.0.4   2023/11/09 15:37
Added to_float(), used mainly in BR parsing, e.g. change string '9,000,154.91-' to float -9000154.91

Release note 0.0.5   2023/11/29 16:43
Created function create_partition(), automatically create partition of next month for each table, with hard coded user name and password

Release note 0.1.1   2024/05/02 10:59
Defined all functions under class Amazon as static method, no need to include argument 'self' when calling functions

Release note 0.1.2   2024/05/02 15:20
Excluded all 'self' under class amazon

## Release note 0.1.3   2024/05/09 11:32
Minor bug fix, correct typos in check_holiday()

## Release note 0.1.4   2024/05/24 14:46
Based on use cases, assign individual connection to check_holiday()

## Release note 0.1.6   2024/07/22 17:35
Automated check_holidays calendars; Discarded the manual update; Adopted the pandas_market_calendars package
Added CobolNumericConverter, CustomUSFederalHolidayCalendar Classes
Tony Yuan

## Release note 0.1.7   2024/12/20 16:51
- Fixed the variable passing issue that check_holiday() only applies to current year
- Refactored data_pull() function for improved connection handling and query execution
- Explicitly imported CobolNumericConverter

## Release note 0.1.8   2024/12/30 17:25
- check holiday function support both datetime.datetime and datetime.date inputs
- calling bank holiday requires inputting """which='Bank_Holiday'"""

## Release note 0.1.9   2025/01/27 14:34
- Brand new onError function delivering teams alert in adaptation of Microsoft retiring Office 365 connectors. The new function directly posts JSON to Logic App endpoints that correspnds to 3 of channels: alert, info and testing, where channel urls are stored in AWS Secrets Manager in consideration of security.

## Release note 0.1.10   2025/03/17 10:50
- Micosoft workflow adaptive card only support json-like inputs, created function safe_for_json() with onError to escape as much special characters/expressions as possible 