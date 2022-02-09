def calculate(data, findall):
    matches = findall(r'([abc]{1})([+-]?)=([abc]?)([+-]?\d*)')
    for v1, s, v2, n in matches:
        if not s:
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s == '+':
            data[v1] += data.get(v2, 0) + int(n or 0)
        elif s == '-':
            data[v1] -= data.get(v2, 0) + int(n or 0)
        # print(v1, s, v2, n)
        # print(data[v1])
    return data

