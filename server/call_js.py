import execjs

def getJsContent(file_name):
    f = open(file_name, 'r')
    file_content = f.read()
    return file_content

if __name__ == '__main__':
    content = getJsContent('./test.js')
    ctx = execjs.compile(content)
    print ctx.call('add', 1, 2)
