async def rounder(num_list):
    res_list = []
    for num in num_list:
        if num == int(num):
            res_list.append(int(num))
        else:
            res_list.append(num)
    return res_list


async def calculator(num1, num2, operator):
    res = None
    if operator == '+':
        res = round(num1 + num2, 2)
    if operator == '-':
        res = round(num1 - num2, 2)
    if operator == '*':
        res = round(num1 * num2, 2)
    if operator == '/':
        res = round(num1 / num2, 2)
    result = await rounder([num1, num2, res])
    return result
