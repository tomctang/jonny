symbols='abcdefghijklm`nopqrstuvwxyz`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
decimal='1234567890 '
lst=['!','"','$','%','&',"'",'(',')','*',',','-','.',':','?','@']
def row(s):
    if s=='.X': return 0
    elif s=='X.': return 1
    elif s=='..': return 2
    else: return 4
def alter_row(s):
    if s=='X.': return 0
    elif s=='.X': return 1
    elif s=='..': return 2
    else: return 4
def decode(s):
    rows=[s[2*i:2*i+2] for i in range(4)]
    rows=[alter_row(rows[0])]+[row(s) for s in rows[1:]]
    return rows[0]*27+rows[1]*9+rows[2]*3+rows[3]
num=int(input())
sl=[input() for _ in range(num)]
ans=''
for s in sl:
    num=decode(s[::-1])
    if num<52:
        if symbols[num]=='`': ans+='#'
        else: ans+=symbols[num]
    elif num<65: ans+=decimal[num-54]
    elif num==80:
        broken=True
        break
    elif num<80: ans+=lst[num-65]
    else: ans+='#'
if not broken:print(ans)
else: print(ans+'LOCKOUT')