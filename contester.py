from subprocess import run, PIPE


def file_to_str(name, param, num):
    file = open(f'tests/{name}/test{num}_{param}.txt', 'r')
    f = file.readlines()
    s = ''
    for i in f:
        s += i
    file.close()
    return s


def main(name, path):

    error = 0
    i = 1
    while True:
        try:
            input_str = file_to_str(name, 'input', i)
            output_str = file_to_str(name, 'output', i)

            sol = run(['python', path], stdout=PIPE, input=input_str, encoding='UTF-8')
            print(sol.stdout[:-1], output_str)
            if sol.stdout[:-1] != output_str:
                error = i
                break
            i += 1
        except FileNotFoundError:
            break
    return error
