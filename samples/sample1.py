def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

def add_item(item, items=[]):
    items.append(item)
    return items

def GetMax(l):
    m = l[0]
    for i in range(1, len(l) + 1):
        if l[i] > m:
            m = l[i]
    return m