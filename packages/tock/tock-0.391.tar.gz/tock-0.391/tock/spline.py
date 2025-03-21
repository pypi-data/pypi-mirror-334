cstr = "e,171.01,26.324 65.119,295.61 48.026,287.01 25.581,272.5 15.216,252 -6.4424,209.16 -3.1531,188.35 15.216,144 40.934,81.911 116.86,45.992 161.46,29.689"

c = []
s = None
e = None
for pstr in cstr.split():
    fields = pstr.split(',')
    if fields[0] == 's':
        s = fields[1:]
    elif fields[0] == 'e':
        e = fields[1:]
    else:
        x = tuple(map(float, fields))
        c.append(x)

c[-1:] = c[-1:] * 3
c[:1] = c[:1] * 3

for t in range(len(c)-3):
    for s in range(0, 10):
        s = s/10
        x = []
        for i in [0,1]:
            x.append(1/6 * (
                c[t][i] * (1-s)**3 +
                c[t+1][i] * ((s+2)*(1-s)**2 + (s+1)*(1-s)*(2-s) + s*(2-s)**2) +
                c[t+2][i] * ((s+1)**2*(1-s) + s*(s+1)*(2-s) + s**2*(3-s)) +
                c[t+3][i] * s**3
            ))
        print(x[0], x[1])

if e is not None:        
    print(e[0], e[1])

#for x in c:
#    print(x[0], x[1])
