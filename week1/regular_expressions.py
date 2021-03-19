def calculate(data, findall):
    matches = findall(r"([abc])([+-]?=)([abc])?([+-]?\d+)?")  # Если придумать хорошую регулярку, будет просто
    for x, sign, y, num in matches:
        if sign == '=':
            data[x] = data.get(y, 0) + int(num or 0)
        elif sign == '+=':
            data[x] += data.get(y, 0) + int(num or 0)
        else:
            data[x] -= data.get(y, 0) + int(num or 0)
    return data

