import execjs


def get_js_content(file_name):
    f = open(file_name, 'r')
    file_content = f.read()
    return file_content


if __name__ == '__main__':
    content = get_js_content('./test.js')
    ctx = execjs.compile(content)
    print ctx.call('add', 1, 2)
