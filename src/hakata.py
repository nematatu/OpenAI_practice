import random
ans = ["は", "か", "た", "の", "し", "お"]
arr = ["す", "し", "ざ", "ん", "ま", "い"]

while(True):
    tmp = random.choice(ans)
    print(tmp, end="")
    arr.append(tmp)
    arr.pop(0)
    if(arr == ans):
        break

print()
print("┏━━━━━━━━┓ \n┃伯方の塩┃ \n┃　　　　┃ \n┃￣Z＿＿_┃ \n┃　　　＠┃ \n┗━━━━━━━━┛")
for s in ans:
    print("　＿人人＿\n ＞　　　＜\n＞　 {} 　＜\n ＞　　　＜\n　￣Y^Y^￣".format(s))