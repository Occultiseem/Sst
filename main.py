# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from flask import  Flask
app=Flask(__name__)

@app.route('/')
def index():
    return 'welcome to my webpage!'

if __name__=="__main__":
    app.run(port=2020,host="127.0.0.1",debug=True) #调用run方法，设定端口号，启动服务