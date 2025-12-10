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
    <title>IP子网切分工具 v1.0.0</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fa;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            max-width: 1200px;
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
         /* 标签页样式 */
         .tabs {
             display: flex;
             margin-bottom: 20px;
             border-bottom: 2px solid #ddd;
         }
         .tab {
             padding: 10px 20px;
             cursor: pointer;
             border: none;
             background-color: transparent;
             font-size: 16px;
             font-weight: bold;
             color: #666;
             border-bottom: 3px solid transparent;
             margin-right: 5px;
         }
         .tab.active {
             color: #3498db;
             border-bottom-color: #3498db;
         }
         .tab:nth-child(1) {
             background-color: rgba(227, 242, 253, 0.5);
         }
         .tab:nth-child(2) {
             background-color: rgba(232, 245, 233, 0.5);
         }
         .tab:nth-child(3) {
             background-color: rgba(243, 229, 245, 0.5);
         }
         .tab-content {
             display: none;
         }
         .tab-content.active {
             display: block;
         }
         /* 表格样式 */
         .subnet-table {
             width: 100%;
             border-collapse: collapse;
             margin: 10px 0;
         }
         .subnet-table th,
         .subnet-table td {
             padding: 8px;
             text-align: left;
             border: 1px solid #ddd;
         }
         .subnet-table th {
             background-color: #f2f2f2;
             font-weight: bold;
         }
         /* 表格容器样式 */
        .table-container {
            border: 1px solid #ddd;
            border-radius: 4px;
        }
     </style>
</head>
<body>
    <div class="container">
        <h1>IP子网切分工具 v1.0.0</h1>
        
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
                    
                    <!-- 标签页控制 -->
                    <div class="tabs">
                        <button class="tab active" onclick="openTab(event, 'split-info')">切分网段信息</button>
                        <button class="tab" onclick="openTab(event, 'remaining-subnets')">剩余网段列表</button>
                        <button class="tab" onclick="openTab(event, 'subnet-chart')">网段分布图表</button>
                    </div>
                    
                    <!-- 切分网段信息标签页 -->
                    <div id="split-info" class="tab-content active" style="background-color: rgba(227, 242, 253, 0.3); padding: 15px; border-radius: 4px;">
                        <div class="subnet-info">
                            <h3>父网段: {{ result.parent }}</h3>
                            <h3>切分网段: {{ result.split }}</h3>
                        </div>
                        
                        <div class="table-container">
                            <table class="subnet-table">
                                <tr>
                                    <th>项目</th>
                                    <th>值</th>
                                </tr>
                                <tr>
                                    <td>网络地址</td>
                                    <td>{{ result.split_info.network }}</td>
                                </tr>
                                <tr>
                                    <td>子网掩码</td>
                                    <td>{{ result.split_info.netmask }}</td>
                                </tr>
                                <tr>
                                    <td>广播地址</td>
                                    <td>{{ result.split_info.broadcast }}</td>
                                </tr>
                                <tr>
                                    <td>CIDR表示</td>
                                    <td>{{ result.split_info.cidr }}</td>
                                </tr>
                                <tr>
                                    <td>前缀长度</td>
                                    <td>{{ result.split_info.prefixlen }}</td>
                                </tr>
                                <tr>
                                    <td>地址总数</td>
                                    <td>{{ result.split_info.num_addresses }}</td>
                                </tr>
                                <tr>
                                    <td>可用地址</td>
                                    <td>{{ result.split_info.usable_addresses }}</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    
                    <!-- 剩余网段列表标签页 -->
                    <div id="remaining-subnets" class="tab-content" style="background-color: rgba(232, 245, 233, 0.3); padding: 15px; border-radius: 4px;">
                        <h3>剩余网段 ({{ result.remaining_subnets_info|length }} 个)</h3>
                        
                        <div class="table-container">
                            <table class="subnet-table">
                                <tr>
                                    <th>序号</th>
                                    <th>CIDR</th>
                                    <th>网络地址</th>
                                    <th>子网掩码</th>
                                    <th>通配符掩码</th>
                                    <th>广播地址</th>
                                    <th>可用地址数</th>
                                </tr>
                                {% for subnet in result.remaining_subnets_info %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td>{{ subnet.cidr }}</td>
                                        <td>{{ subnet.network }}</td>
                                        <td>{{ subnet.netmask }}</td>
                                        <td>{{ subnet.wildcard }}</td>
                                        <td>{{ subnet.broadcast }}</td>
                                        <td>{{ subnet.usable_addresses }}</td>
                                    </tr>
                                {% endfor %}
                            </table>
                        </div>
                    </div>
                    
                    <!-- 网段分布图表标签页 -->
                    <div id="subnet-chart" class="tab-content" style="background-color: rgba(243, 229, 245, 0.3); padding: 15px; border-radius: 4px;">
                        <h3>网段分布图表</h3>
                        <div style="width: 100%; overflow: hidden;">
                            <canvas id="subnetChartCanvas"></canvas>
                        </div>
                        <script>
                            function drawSubnetChart() {
                                var canvas = document.getElementById('subnetChartCanvas');
                                if (!canvas) return;
                                
                                var ctx = canvas.getContext('2d');
                                
                                // 获取数据
                                try {
                                    // 从模板获取数据
                                    var parentCidr = "{{ result.parent }}";
                                    var splitCidr = "{{ result.split }}";
                                    var splitInfo = {
                                        network: "{{ result.split_info.network }}",
                                        cidr: "{{ result.split_info.cidr }}",
                                        prefixlen: {{ result.split_info.prefixlen }},
                                        num_addresses: {{ result.split_info.num_addresses }},
                                        usable_addresses: {{ result.split_info.usable_addresses }}
                                    };
                                    
                                    var remainingSubnets = [
                                        {% for subnet in result.remaining_subnets_info %}
                                            {
                                                network: "{{ subnet.network }}",
                                                cidr: "{{ subnet.cidr }}",
                                                prefixlen: {{ subnet.prefixlen }},
                                                num_addresses: {{ subnet.num_addresses }},
                                                usable_addresses: {{ subnet.usable_addresses }}
                                            },
                                        {% endfor %}
                                    ];
                                    
                                    // 检查数据是否有效
                                    if (!parentCidr || !splitInfo || !remainingSubnets) {
                                        console.error('图表数据不完整');
                                        return;
                                    }
                                    
                                    // 计算父网段的总地址数
                                    var parentPrefix = parseInt(parentCidr.split('/')[1]);
                                    var parentTotalAddresses = Math.pow(2, 32 - parentPrefix);
                                    
                                    // 使用对数比例尺来更好地显示差距巨大的网段大小
                                    var logMax = Math.log10(parentTotalAddresses);
                                    var logMin = 3; // 最小显示3个数量级（1000个地址）
                                    
                                    // 为小网段设置最小显示宽度
                                    var minBarWidth = 50;
                                    
                                    // 获取容器宽度
                                    var containerWidth = canvas.parentElement.clientWidth;
                                    var availableWidth = containerWidth - 80; // 减少边距，增加可用宽度
                                    
                                    // 绘制配置
                                    var x = 50;
                                    var y = 50;
                                    var barHeight = 40;
                                    var padding = 20;
                                    
                                    // 设置画布宽度为容器宽度
                                    canvas.width = containerWidth;
                                    
                                    // 计算所需的画布高度
                                    var requiredHeight = y + 40 + // 父网段信息
                                                       (barHeight + padding) + // 切分网段
                                                       40 + // 剩余网段标题
                                                       (remainingSubnets.length * (barHeight + padding)) + // 所有剩余网段
                                                       80; // 图例和底部边距
                                    
                                    // 动态设置画布高度
                                    canvas.height = requiredHeight;
                                    
                                    // 清空画布
                                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                                    
                                    // 绘制父网段信息
                                    ctx.fillStyle = '#34495e';
                                    ctx.font = '18px Arial bold';
                                    ctx.textAlign = 'left';
                                    ctx.fillText('父网段: ' + parentCidr, x, y - 10);
                                    
                                    // 绘制切分网段
                                    y += 20;
                                    // 使用对数比例尺计算宽度
                                    var splitLogValue = Math.max(logMin, Math.log10(splitInfo.num_addresses));
                                    var splitBarWidth = Math.max(minBarWidth, ((splitLogValue - logMin) / (logMax - logMin)) * availableWidth);
                                    ctx.fillStyle = '#3498db';
                                    ctx.fillRect(x, y, splitBarWidth, barHeight);
                                    
                                    // 绘制切分网段文本
                                    ctx.fillStyle = '#000000'; // 使用黑色文字
                                    ctx.font = '12px Arial';
                                    ctx.textAlign = 'left';
                                    // 添加文字描边提高可读性
                                    ctx.strokeStyle = '#ffffff';
                                    ctx.lineWidth = 2;
                                    
                                    // 根据条宽度调整文本位置和可见性
                                    var textX = x + 15;
                                    var maxTextWidth = splitBarWidth - 30;
                                    
                                    // 绘制切分网段信息和地址数（分开对齐）
                                      ctx.fillStyle = '#000000';
                                      ctx.font = '16px Arial';
                                      ctx.textBaseline = 'middle';
                                      
                                      // 绘制网段信息（左对齐）
                                      var segmentText = '切分网段: ' + splitInfo.cidr;
                                      var addressText = '可用地址数: ' + splitInfo.usable_addresses.toLocaleString();
                                      
                                      // 网段信息左对齐，地址数在固定位置对齐
                                      var addressX = x + 250; // 固定地址数的起始位置
                                      
                                      ctx.strokeText(segmentText, textX, y + barHeight / 2);
                                      ctx.fillText(segmentText, textX, y + barHeight / 2);
                                      ctx.strokeText(addressText, addressX, y + barHeight / 2);
                                      ctx.fillText(addressText, addressX, y + barHeight / 2);
                                    
                                    y += barHeight + padding;
                                    
                                    // 绘制剩余网段标题，与上面蓝色部分拉开更大间距
                                    y += 20; // 额外增加间距
                                    ctx.fillStyle = '#34495e'; // 与父网段保持一致的颜色
                                    ctx.font = '18px Arial';
                                    ctx.textAlign = 'left';
                                    ctx.fillText('剩余网段 (' + remainingSubnets.length + ' 个):', x, y);
                                    
                                    y += 20; // 保持与父网段一致的风格间距
                                    
                                    // 绘制剩余网段
                                    // 定义多种颜色用于剩余网段
                                    var subnetColors = [
                                        '#27ae60', '#e74c3c', '#f39c12', '#8e44ad', '#16a085',
                                        '#2c3e50', '#d35400', '#c0392b', '#2980b9', '#27ae60',
                                        '#f1c40f', '#e67e22', '#9b59b6', '#1abc9c', '#34495e',
                                        '#e74c3c', '#f39c12', '#8e44ad', '#16a085', '#2c3e50'
                                    ];
                                    
                                    for (var i = 0; i < remainingSubnets.length; i++) {
                                        var subnet = remainingSubnets[i];
                                        
                                        // 使用对数比例尺计算宽度
                                        var subnetLogValue = Math.max(logMin, Math.log10(subnet.num_addresses));
                                        var subnetBarWidth = Math.max(minBarWidth, ((subnetLogValue - logMin) / (logMax - logMin)) * availableWidth);
                                        
                                        // 为每个剩余网段选择不同颜色
                                        var colorIndex = i % subnetColors.length;
                                        ctx.fillStyle = subnetColors[colorIndex];
                                        ctx.fillRect(x, y, subnetBarWidth, barHeight);
                                        
                                        // 绘制网段信息
                                        ctx.fillStyle = '#000000'; // 使用黑色文字
                                        ctx.font = '12px Arial';
                                        ctx.textAlign = 'left';
                                        // 添加文字描边提高可读性
                                        ctx.strokeStyle = '#ffffff';
                                        ctx.lineWidth = 2;
                                        
                                        // 根据条宽度调整文本位置和可见性
                                        var textX = x + 15;
                                        var maxTextWidth = subnetBarWidth - 30;
                                        
                                        // 绘制网段信息（水平排列）
                                        // 绘制网段信息和地址数（分开对齐）
                                          ctx.fillStyle = '#000000';
                                          ctx.font = '16px Arial';
                                          ctx.textBaseline = 'middle';
                                          
                                          // 绘制网段信息（左对齐）
                                          var segmentText = '网段 ' + (i + 1) + ': ' + subnet.cidr;
                                          var addressText = '可用地址数: ' + subnet.usable_addresses.toLocaleString();
                                          
                                          // 网段信息左对齐，地址数在固定位置对齐
                                          var addressX = x + 250; // 固定地址数的起始位置
                                          
                                          ctx.strokeText(segmentText, textX, y + barHeight / 2);
                                          ctx.fillText(segmentText, textX, y + barHeight / 2);
                                          ctx.strokeText(addressText, addressX, y + barHeight / 2);
                                          ctx.fillText(addressText, addressX, y + barHeight / 2);
                                        
                                        y += barHeight + padding;
                                    }
                                    
                                    // 绘制图例
                                    ctx.fillStyle = '#34495e';
                                    ctx.font = '14px Arial';
                                    ctx.textAlign = 'left';
                                    ctx.fillText('图例:', x, y + 20);
                                    
                                    // 切分网段图例
                                    ctx.fillStyle = '#3498db';
                                    ctx.fillRect(x, y + 30, 20, 15);
                                    ctx.fillStyle = '#34495e';
                                    ctx.font = '12px Arial';
                                    ctx.textAlign = 'left';
                                    ctx.fillText('切分网段', x + 30, y + 42);
                                    
                                    // 剩余网段图例（显示多彩示例）
                                    var legendColors = ['#27ae60', '#e74c3c', '#f39c12', '#8e44ad'];
                                    for (var j = 0; j < legendColors.length; j++) {
                                        ctx.fillStyle = legendColors[j];
                                        ctx.fillRect(x + 150 + j * 25, y + 30, 20, 15);
                                    }
                                    ctx.fillStyle = '#34495e';
                                    ctx.font = '12px Arial';
                                    ctx.textAlign = 'left';
                                    ctx.fillText('剩余网段(多色)', x + 260, y + 42);
                                    
                                    // 调整页面布局
                                    document.getElementById('subnetChartCanvas').parentElement.style.height = requiredHeight + 'px';
                                    
                                } catch (error) {
                                    console.error('绘制图表时发生错误:', error);
                                    // 设置最小高度以显示错误信息
                                    canvas.height = 200;
                                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                                    ctx.fillStyle = '#e74c3c';
                                    ctx.font = '16px Arial';
                                    ctx.textAlign = 'center';
                                    ctx.fillText('图表加载失败，请刷新页面重试', canvas.width / 2, canvas.height / 2);
                                }
                            }
                            
                            // 页面加载完成后绘制图表
                            window.onload = function() {
                                // 检查是否有结果数据
                                {% if result and not result.error %}
                                    drawSubnetChart();
                                {% endif %}
                            };
                            
                            // 监听标签页切换事件，当切换到图表标签页时重新绘制
                            document.addEventListener('DOMContentLoaded', function() {
                                var tabs = document.getElementsByClassName('tab');
                                for (var i = 0; i < tabs.length; i++) {
                                    tabs[i].addEventListener('click', function(e) {
                                        if (e.target.innerHTML === '网段分布图表') {
                                            setTimeout(drawSubnetChart, 100);
                                        }
                                    });
                                }
                            });
                        </script>
                    </div>
                {% endif %}
            </div>
        {% endif %}
        
        <!-- 标签页切换JavaScript -->
        <script>
            function openTab(evt, tabName) {
                // 获取所有标签页内容
                var tabContents = document.getElementsByClassName("tab-content");
                for (var i = 0; i < tabContents.length; i++) {
                    tabContents[i].classList.remove("active");
                }
                
                // 获取所有标签按钮
                var tabs = document.getElementsByClassName("tab");
                for (var i = 0; i < tabs.length; i++) {
                    tabs[i].classList.remove("active");
                }
                
                // 显示当前标签页内容并激活标签按钮
                document.getElementById(tabName).classList.add("active");
                evt.currentTarget.classList.add("active");
            }
        </script>
    </div>
    <div style="text-align: center; margin-top: 20px; color: #7f8c8d; font-size: 14px;">
        版本: v1.0.0
    </div>
</body>
</html>
'''

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
