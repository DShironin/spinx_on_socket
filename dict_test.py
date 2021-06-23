# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import yaml

with open('/home/shironin/PycharmProjects/unoctl/config.yml') as f:
    data = yaml.safe_load(f)


def test(r, path, res):
    for j in r:
        if isinstance(j, dict):
            print(path)
            path += f'{j}/'
            for i in j.keys():
                test(j[i], path, res)
        else:
            res = j
        return path, res


res = ''
path = ''
path, res = test(data, path, res)
print(res)

