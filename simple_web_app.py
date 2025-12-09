#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
不依赖Flask的简单Web服务器版本
使用Python标准库的http.server模块实现
"""

import http.server
import socketserver
import urllib.parse
import json
from ip_subnet_calculator import split_subnet

PORT = 5000

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
                <input type="text" id="parent" name="parent" value="{{ parent }}" required>
            </div>
            <div class="form-group">
                <label for="split">要切分的子网 (如：10.21.60.0/23)</label>
                <input type="text" id="split" name="split" value="{{ split }}" required>
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
                    
                    <h3>剩余网段 ({{ len_remaining }} 个)</h3>
                    {% for i, subnet in enumerate_remaining %}
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
'''

def render_template(template, **kwargs):
    """
    简单的模板渲染函数
    """
    result = template
    for key, value in kwargs.items():
        if key == 'enumerate_remaining' and isinstance(value, list):
            # 处理enumerate_remaining特殊情况
            placeholder = '{% for i, subnet in enumerate_remaining %}'
            end_placeholder = '{% endfor %}'
            if placeholder in result and end_placeholder in result:
                start_idx = result.find(placeholder)
                end_idx = result.find(end_placeholder)
                if start_idx < end_idx:
                    loop_content = result[start_idx + len(placeholder):end_idx]
                    rendered_loop = ''
                    for i, item in enumerate(value):
                        item_html = loop_content
                        for k, v in item.items():
                            item_html = item_html.replace(f'{{{{ subnet.{k} }}}}', str(v))
                        item_html = item_html.replace('{{ i+1 }}', str(i+1))
                        rendered_loop += item_html
                    result = result[:start_idx] + rendered_loop + result[end_idx + len(end_placeholder):]
        else:
            result = result.replace(f'{{{{ {key} }}}}', str(value))
    return result

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # 渲染默认页面
        html = render_template(HTML_TEMPLATE, parent='10.0.0.0/8', split='10.21.60.0/23', result=None)
        self.wfile.write(html.encode('utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 解析表单数据
        form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        parent = form_data.get('parent', [''])[0].strip()
        split = form_data.get('split', [''])[0].strip()
        
        # 执行切分
        result = split_subnet(parent, split)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # 渲染结果页面
        len_remaining = len(result.get('remaining_subnets_info', [])) if not result.get('error') else 0
        enumerate_remaining = result.get('remaining_subnets_info', []) if not result.get('error') else []
        
        html = render_template(HTML_TEMPLATE, 
                              parent=parent, 
                              split=split, 
                              result=result,
                              len_remaining=len_remaining,
                              enumerate_remaining=enumerate_remaining)
        self.wfile.write(html.encode('utf-8'))

def run_server():
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"服务器已启动，访问地址: http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    run_server()
