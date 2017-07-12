import execjs
import os


def get_js_content(file_name):
    f = open(file_name, 'r')
    file_content = f.read().decode('utf-8')
    return file_content


if __name__ == '__main__':
    os.environ["NODE_PATH"] = os.getcwd() + "/node_modules"
    content = get_js_content('./js/index.js')
    ctx = execjs.compile(content)
    print ctx.call('generateImage')
