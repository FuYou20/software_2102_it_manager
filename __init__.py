#从flask包中导入Flask类
from flask import Flask, render_template, request, jsonify
import joblib
from flask import Flask, render_template, redirect, url_for, jsonify
import pandas as pd
from collections import defaultdict

#创建一个Flask对象
app = Flask(__name__,template_folder='./templates')
dictionary = defaultdict(list)

def initDic():
    # 读取Excel文件
    data = pd.read_excel('./templates/name-code.xlsx')

    # 遍历Excel中的每一行
    for index, row in data.iterrows():
        key = row['name']  # 将键的列名替换为你实际的列名
        value = row['code']  # 将值的列名替换为你实际的列名
        dictionary[key].append(value)

@app.route('/index')
def index(mystr=None):
    return render_template('index.html')

@app.route('/pred')
def predPage():
    return render_template('pred.html')

@app.route('/view')
def viewPage():
    return render_template('view.html')

@app.route('/forecast', methods=['POST'])
def pred():
    lift = request.form.get('lift')  # 获取面积参数的值
    address = request.form.get('address')  # 获取小区名参数的值
    floor = request.form.get('floor')  # 获取楼层数参数的值
    print(lift)
    if "1"==lift:
        lift=1
    else:
        lift=0
    floor=float(floor)
    initDic()
    code=dictionary[address]
    if len(code)==0:
        return jsonify(result="小区不存在")
    code=float(code[0])

    path = "model"
    model = joblib.load(path)
    pred =model.predict([[code,lift,floor]])
    res = str(int(pred))
    return jsonify(result=res)  # 返回JSON格式的结果


if __name__ == '__main__':
    #默认为5000端口
    app.run()  #app.run(port=8000)