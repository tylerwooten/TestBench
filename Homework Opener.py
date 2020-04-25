from selenium import webdriver

my_string = '8-26; 8-27; 8-29; 8-30; 8-45; 8-64'
my_list = my_string.split("; ")

print(my_list)
b = []

for a in my_list:
    b.append(a[2:])

print(b)

for item in b:
    print("https://www.chegg.com/homework-help/Shigley-s-Mechanical-Engineering-Design-10th-edition-chapter-8-problem-%sP-solution-9780073398204" % item)

