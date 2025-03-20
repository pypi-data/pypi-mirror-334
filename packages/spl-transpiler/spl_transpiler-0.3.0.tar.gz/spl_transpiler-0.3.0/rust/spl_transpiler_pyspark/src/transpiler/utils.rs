use crate::ast::*;
use anyhow::{bail, Context, Result};

pub fn join_as_binaries(op: impl ToString, exprs: Vec<ColumnLike>) -> Option<ColumnLike> {
    match exprs.len() {
        0 => None,
        1 => Some(exprs[0].clone()),
        2 => Some(ColumnLike::BinaryOp {
            op: op.to_string(),
            left: Box::new(exprs[0].clone().into()),
            right: Box::new(exprs[1].clone().into()),
        }),
        _ => {
            let mut left = exprs[0].clone();
            for check in &exprs[1..] {
                left = ColumnLike::BinaryOp {
                    left: Box::new(left.into()),
                    op: op.to_string(),
                    right: Box::new(check.clone().into()),
                };
            }
            Some(left)
        }
    }
}

/* SPL format arguments:
Date and time variables
Variable 	 Description
%c       	 The date and time in the current locale's format as defined by the server's operating system. For example, Thu Jul 18 09:30:00 2019 for US English on Linux.
%+       	 The date and time with time zone in the current locale's format as defined by the server's operating system. For example, Thu Jul 18 09:30:00 PDT 2019 for US English on Linux.
Time variables
Variable 	 Description
%Ez      	 Splunk-specific, timezone in minutes.
%f       	 Microseconds as a decimal number.
%H       	 Hour (24-hour clock) as a decimal number. Hours are represented by the values 00 to 23. Leading zeros are accepted but not required.
%I       	 Uppercase "i". Hour (12-hour clock) with the hours represented by the values 01 to 12. Leading zeros are accepted but not required. Use with %p to specify AM or PM for the 12-hour clock.
%k       	 Like %H, the hour (24-hour clock) as a decimal number. Leading zeros are replaced by a space, for example 0 to 23.
%M       	 Minute as a decimal number. Minutes are represented by the values 00 to 59. Leading zeros are accepted but not required.
%N       	 The number of subsecond digits. The default is %9N. You can specify %3N = milliseconds, %6N = microseconds, %9N = nanoseconds.
%p       	 AM or PM. Use with %I to specify the 12-hour clock for AM or PM. Do not use with %H.
%Q       	 The subsecond component of a UTC timestamp. The default is milliseconds, %3Q. Some valid values are:
              %3Q = milliseconds, with values of 000-999
              %6Q = microseconds, with values of 000000-999999
              %9Q = nanoseconds, with values of 000000000-999999999
%S       	 Second as a decimal number, for example 00 to 59.
%s       	 The UNIX Epoch Time timestamp, or the number of seconds since the Epoch: 1970-01-01 00:00:00 +0000 (UTC). For example the UNIX epoch time 1484993700 is equal to Tue Jan 21 10:15:00 2020.
%T       	 The time in 24-hour notation (%H:%M:%S). For example 23:59:59.
%X       	 The time in the format for the current locale. For US English the format for 9:30 AM is 9:30:00.
%Z       	 The timezone abbreviation. For example EST for US Eastern Standard Time.
%z       	 The timezone offset from UTC, in hour and minute: +hhmm or -hhmm. For example, for 5 hours before UTC the values is -0500 which is US Eastern Standard Time.
Examples:

Use %z to specify hour and minute, for example -0500
Use %:z to specify hour and minute separated by a colon, for example -05:00
Use %::z to specify hour minute and second separated with colons, for example -05:00:00
Use %:::z to specify hour only, for example -05
%%	A literal "%" character.
To parse timestamps with GMT and an offset in data that you upload using Add Data, such as Fri Apr 29 2022 23:45:22 GMT-0700, you might need to use %:Z to capture both the timestamp and the offset.

Date variables
Variable	Description
%F 	 Equivalent to %Y-%m-%d (the ISO 8601 date format).
%x 	 The date in the format of the current locale. For example, 7/13/2019 for US English.
Specifying days and weeks
Variable   	 Description
%A         	 Full weekday name. (Sunday, ..., Saturday)
%a         	 Abbreviated weekday name. (Sun, ... ,Sat)
%d         	 Day of the month as a decimal number, includes a leading zero. (01 to 31)
%e         	 Like %d, the day of the month as a decimal number, but a leading zero is replaced by a space. (1 to 31)
%j         	 Day of year as a decimal number, includes a leading zero. (001 to 366)
%V (or %U) 	 Week of the year. The %V variable starts the count at 1, which is the most common start number. The %U variable starts the count at 0.
%w         	 Weekday as a decimal number. (0 = Sunday, ..., 6 = Saturday)
Specifying months
Variable 	 Description
%b       	 Abbreviated month name. (Jan, Feb, etc.)
%B       	 Full month name. (January, February, etc.)
%m       	 Month as a decimal number. (01 to 12). Leading zeros are accepted but not required.
Specifying year
Variable 	 Description
%y       	 Year as a decimal number, without the century. (00 to 99). Leading zeros are accepted but not required.
%Y       	 Year as a decimal number with century. For example, 2020.
 */

/* Spark time format arguments:
Symbol 	 Meaning                      	 Presentation 	 Examples
G      	 era                          	 text         	 AD; Anno Domini
y      	 year                         	 year         	 2020; 20
D      	 day-of-year                  	 number(3)    	 189
M/L    	 month-of-year                	 month        	 7; 07; Jul; July
d      	 day-of-month                 	 number(2)    	 28
Q/q    	 quarter-of-year              	 number/text  	 3; 03; Q3; 3rd quarter
E      	 day-of-week                  	 text         	 Tue; Tuesday
F      	 aligned day of week in month 	 number(1)    	 3
a      	 am-pm-of-day                 	 am-pm        	 PM
h      	 clock-hour-of-am-pm (1-12)   	 number(2)    	 12
K      	 hour-of-am-pm (0-11)         	 number(2)    	 0
k      	 clock-hour-of-day (1-24)     	 number(2)    	 1
H      	 hour-of-day (0-23)           	 number(2)    	 0
m      	 minute-of-hour               	 number(2)    	 30
s      	 second-of-minute             	 number(2)    	 55
S      	 fraction-of-second           	 fraction     	 978
V      	 time-zone ID                 	 zone-id      	 America/Los_Angeles; Z; -08:30
z      	 time-zone name               	 zone-name    	 Pacific Standard Time; PST
O      	 localized zone-offset        	 offset-O     	 GMT+8; GMT+08:00; UTC-08:00;
X      	 zone-offset ‘Z’ for zero     	 offset-X     	 Z; -08; -0830; -08:30; -083015; -08:30:15;
x      	 zone-offset                  	 offset-x     	 +0000; -08; -0830; -08:30; -083015; -08:30:15;
Z      	 zone-offset                  	 offset-Z     	 +0000; -0800; -08:00;
‘      	 escape for text              	 delimiter
’‘     	 single quote                 	 literal      	 ’
[      	 optional section start
]      	 optional section end
 */

const CONVERSIONS: [(&str, Option<&str>); 37] = [
    // Date and time variables
    ("%c", None), // No direct equivalent
    ("%+", None), // No direct equivalent
    // Time variables
    ("%Ez", None),              // No direct equivalent
    ("%f", Some("SSS")),        // Microseconds as a decimal number
    ("%H", Some("HH")),         // Hour (24-hour clock)
    ("%I", Some("hh")),         // Hour (12-hour clock)
    ("%k", Some("H")),          // Hour (24-hour clock, leading space)
    ("%M", Some("mm")),         // Minute
    ("%N", Some("SSS")),        // Subsecond digits (default to milliseconds)
    ("%p", Some("a")),          // AM or PM
    ("%Q", Some("SSS")),        // Subsecond component of a UTC timestamp (default to milliseconds)
    ("%3Q", Some("SSS")),       // Subsecond component of a UTC timestamp (milliseconds)
    ("%6Q", Some("SSSSSS")),    // Subsecond component of a UTC timestamp (microseconds)
    ("%9Q", Some("SSSSSSSSS")), // Subsecond component of a UTC timestamp (nanoseconds)
    ("%S", Some("ss")),         // Second
    ("%s", None),               // No direct equivalent for UNIX Epoch Time timestamp
    ("%T", Some("HH:mm:ss")),   // Time in 24-hour notation
    ("%X", None),               // No direct equivalent for locale-specific time
    ("%Z", Some("z")),          // Timezone abbreviation
    // Use %z to specify hour and minute, for example ‘+01’ or ‘+0130’ if non-zero minute
    // Use %:z to specify hour and minute separated by a colon, for example -05:00
    // Use %::z to specify hour minute and second separated with colons, for example -05:00:00
    // Use %:::z to specify hour only, for example -05
    // https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html
    // Offset X and x: This formats the offset based on the number of pattern letters. One letter outputs just the hour, such as ‘+01’, unless the minute is non-zero in which case the minute is also output, such as ‘+0130’. Two letters outputs the hour and minute, without a colon, such as ‘+0130’. Three letters outputs the hour and minute, with a colon, such as ‘+01:30’. Four letters outputs the hour and minute and optional second, without a colon, such as ‘+013015’. Five letters outputs the hour and minute and optional second, with a colon, such as ‘+01:30:15’. Six or more letters will fail. Pattern letter ‘X’ (upper case) will output ‘Z’ when the offset to be output would be zero, whereas pattern letter ‘x’ (lower case) will output ‘+00’, ‘+0000’, or ‘+00:00’.
    ("%z", Some("x")),       // Timezone offset from UTC
    ("%:z", Some("xxx")),    // Timezone offset from UTC
    ("%::z", Some("xxxxx")), // Timezone offset from UTC
    ("%:::z", Some("xx")),   // Timezone offset from UTC
    // Date variables
    ("%F", Some("yyyy-MM-dd")), // ISO 8601 date format
    ("%x", None),               // No direct equivalent for locale-specific date
    // Specifying days and weeks
    ("%A", Some("EEEE")), // Full weekday name
    ("%a", Some("EEE")),  // Abbreviated weekday name
    ("%d", Some("dd")),   // Day of the month
    ("%e", Some("d")),    // Day of the month (leading space)
    ("%j", Some("D")),    // Day of year
    // ("%V", Some("w")), // Week of the year (ISO)
    // ("%U", Some("w")), // Week of the year (starting with 0)
    ("%w", Some("e")), // Weekday as a decimal number (1 = Monday, ..., 7 = Sunday)
    // Specifying months
    ("%b", Some("MMM")),  // Abbreviated month name
    ("%B", Some("MMMM")), // Full month name
    ("%m", Some("MM")),   // Month as a decimal number
    // Specifying year
    ("%y", Some("yy")),   // Year without century
    ("%Y", Some("yyyy")), // Year with century
    // Other
    ("%%", Some("%")), // A literal "%" character
];

pub fn convert_time_format(spl_time_format: impl ToString) -> Result<String> {
    let fmt_string = spl_time_format.to_string();

    for (original, replacement) in CONVERSIONS {
        if !fmt_string.contains(original) {
            continue;
        }
        return Ok(match replacement {
            None => bail!("No known replacement pattern for `{}`", original),
            Some(replacement) => {
                let (left, right) = fmt_string
                    .split_once(original)
                    .context("Failed to find pattern even after we checked for it...?")?;
                let left = convert_time_format(left)
                    .context(format!("Failed to convert left remainder {}", left))?;
                let right = convert_time_format(right)
                    .context(format!("Failed to convert right remainder {}", right))?;
                format!("{}{}{}", left, replacement, right)
            }
        });
    }
    Ok(match fmt_string.as_str() {
        s if s.chars().any(|c| c.is_alphanumeric()) => format!("'{}'", s),
        s => s.into(),
    })
}

pub fn ctime_with_timezone(c: impl Into<Expr>, timeformat: String) -> Result<ColumnLike> {
    let converted_time_format = convert_time_format(timeformat)?;
    Ok(column_like!(date_format(
        [c.into()],
        [py_lit(converted_time_format)]
    )))
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    fn test_convert_time_format_1() {
        assert_eq!(
            convert_time_format("%Y-%m-%dT%H:%M:%S").expect("Failed to convert time format"),
            "yyyy-MM-dd'T'HH:mm:ss".to_string()
        )
    }
}
