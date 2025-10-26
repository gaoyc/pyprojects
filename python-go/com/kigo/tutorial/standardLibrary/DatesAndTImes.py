# encoding :utf-8
# dates are easily constructed and formatted
from datetime import date
now = date.today()

# result: datetime.date(2003, 12, 2)
ret = now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
'12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

print(ret)

# dates support calendar arithmetic
birthday = date(1964, 7, 31)
age = now - birthday
print(age.days)
14368