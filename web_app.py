from flask import Flask, render_template_string, request
from ip_subnet_calculator import split_subnet

app = Flask(__name__)

# 模板过滤器
def enumerate_filter(sequence, start=0):
    return enumerate(sequence, start)

app.jinja_env.filters['enumerate'] = enumerate_filter

# HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP子网切分工具</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fa;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 30px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 6px;
        }
        .result h2 {
            color: #27ae60;
            margin-top: 0;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        .subnet-info {
            margin: 15px 0;
            padding: 15px;
            background-color: white;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .subnet-info h3 {
            color: #34495e;
            margin-top: 0;
            margin-bottom: 15px;
        }
        .info-row {
            display: flex;
            margin-bottom: 8px;
        }
        .info-label {
            font-weight: bold;
            width: 120px;
            color: #666;
        }
        .info-value {
            color: #333;
        }
        .error {
            color: #e74c3c;
            background-color: #fee;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .success {
            color: #27ae60;
            background-color: #efe;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>IP子网切分工具</h1>
        
        <form method="POST">
            <div class="form-group">
                <label for="parent">父网段 (如：10.0.0.0/8)</label>
                <input type="text" id="parent" name="parent" value="{{ parent if parent else '10.0.0.0/8' }}" required>
            </div>
            <div class="form-group">
                <label for="split">要切分的子网 (如：10.21.60.0/23)</label>
                <input type="text" id="split" name="split" value="{{ split if split else '10.21.60.0/23' }}" required>
            </div>
            <button type="submit">执行切分</button>
        </form>
        
        {% if result %}
            <div class="result">
                {% if result.error %}
                    <div class="error">
                        <strong>错误：</strong>{{ result.error }}
                    </div>
                {% else %}
                    <h2>切分结果</h2>
                    
                    <div class="subnet-info">
                        <h3>父网段: {{ result.parent }}</h3>
                        <h3>切分网段: {{ result.split }}</h3>
                    </div>
                    
                    <div class="subnet-info">
                        <h3>切分网段信息</h3>
                        <div class="info-row">
                            <div class="info-label">网络地址:</div>
                            <div class="info-value">{{ result.split_info.network }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">子网掩码:</div>
                            <div class="info-value">{{ result.split_info.netmask }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">广播地址:</div>
                            <div class="info-value">{{ result.split_info.broadcast }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">CIDR表示:</div>
                            <div class="info-value">{{ result.split_info.cidr }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">前缀长度:</div>
                            <div class="info-value">{{ result.split_info.prefixlen }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">地址总数:</div>
                            <div class="info-value">{{ result.split_info.num_addresses }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">可用地址:</div>
                            <div class="info-value">{{ result.split_info.usable_addresses }}</div>
                        </div>
                    </div>
                    
                    <h3>剩余网段 ({{ result.remaining_subnets|length }} 个)</h3>
                    {% for i, subnet in enumerate(result.remaining_subnets_info) %}
                        <div class="subnet-info">
                            <h4>网段 {{ i+1 }}</h4>
                            <div class="info-row">
                                <div class="info-label">网络地址:</div>
                                <div class="info-value">{{ subnet.network }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">子网掩码:</div>
                                <div class="info-value">{{ subnet.netmask }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">广播地址:</div>
                                <div class="info-value">{{ subnet.broadcast }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">CIDR表示:</div>
                                <div class="info-value">{{ subnet.cidr }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">前缀长度:</div>
                                <div class="info-value">{{ subnet.prefixlen }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">地址总数:</div>
                                <div class="info-value">{{ subnet.num_addresses }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">可用地址:</div>
                                <div class="info-value">{{ subnet.usable_addresses }}</div>
                            </div>
                        </div>
                    {% endfor %}
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>

@app.route('/', methods=['GET', 'POST'])
def index():
    parent = request.form.get('parent', '10.0.0.0/8')
    split = request.form.get('split', '10.21.60.0/23')
    result = None
    
    if request.method == 'POST':
        # 执行切分
        result = split_subnet(parent, split)
    
    return render_template_string(HTML_TEMPLATE, parent=parent, split=split, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
