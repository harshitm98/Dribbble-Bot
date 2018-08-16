import random
with open('first_names.txt', 'r') as file:
    f = file.read()
    first_names = f.split('\n')
    file.close()
with open('last_names.txt', 'r') as file:
    f = file.read()
    last_names = f.split('\n')
    file.close()
for i in range(150):
    with open('credentials.txt', 'a+') as file:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email_id = first_name + last_name
        k = random.choice([4, 5, 6, 7, 8])
        for j in range(k):
            if j == k-1:
                email_id = email_id + str(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))
            else:
                email_id = email_id + str(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '.']))
        email_id = email_id.lower()
        password = ""
        for j in range(10):
            password = password + random.choice(list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOSDFGHJKLZXCVBNM123456789"))
        credentials = first_name + " " + last_name + " " + email_id + " " + password + "\n"
        file.write(credentials)
file.close()
