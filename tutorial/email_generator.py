from coota.preset import *


# generate an email address with a 7-digit name ending with "outlook.com"
domain, name_length = "outlook.com", 7

generator = EmailGenerator(domain=domain)
email = generator.generate(name_length)
print(type(email), email)
