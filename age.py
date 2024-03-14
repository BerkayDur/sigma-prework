from datetime import datetime

def calculate_age(DOB):
  return int((datetime.now() - datetime.strptime(DOB, "%d-%m-%Y")).days // (365.25))

print(calculate_age("01-01-1990"))
print(calculate_age("04-12-1972"))