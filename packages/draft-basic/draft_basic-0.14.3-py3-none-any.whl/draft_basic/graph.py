import matplotlib.pyplot as plt
import warnings

def draw_linechart(data, label, x_interval=1, graph_name='graph', y_label='y_label'):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用微软雅黑字体
    plt.rcParams['axes.unicode_minus'] = False  # 处理负号显示问题
    if len(data) == 0:
        assert ValueError(f"数据为空")
    if len(data) > 8:
        assert ValueError(f"目前只支持最多8种数据，请减少数据种类")
    first_data = data[0]
    for i in range(len(data)):
        if len(first_data) != len(data[i]):
            warnings.warn("每种数据数量不一致", RuntimeWarning)
    epochs_list = [i for i in range(1, len(data[0]) + 1)]
    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    # 绘制损失图
    plt.figure(figsize=(10, 5))
    if len(data) != len(label):
        assert ValueError(f"数据种数需与其标签数量相同")

    for i in range(len(data)):
        plt.plot(epochs_list, data[i], label=label[i], color=color[i])

    # 设置 x 轴刻度为整数
    plt.xticks(range(0, len(epochs_list) + 1, x_interval))
    plt.title(graph_name)
    plt.xlabel('Epoch')
    plt.ylabel(y_label)
    plt.legend()
    plt.grid()
    plt.show()

def draw_confusionmatrix(con_matrix, index):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用微软雅黑字体
    plt.rcParams['axes.unicode_minus'] = False  # 处理负号显示问题
    fig, ax = plt.subplots()

    ax.axis('off')


    table = ax.table(cellText=con_matrix,  # 表格中的数据
                     loc='center',  # 表格位置
                     cellLoc='center',  # 单元格内文字居中
                     colLabels=index,  # 列标题
                     rowLabels=index)  # 行标题
    table.add_cell(0, -1, width=0.1, height=0.045, text='True/Predict', loc='center')
    # 设置表格样式（可选）
    table.auto_set_font_size(False)
    table.set_fontsize(12)  # 设置字体大小
    table.scale(1.5, 1.5)  # 调整表格的宽度和高度比例


    # 调整布局
    plt.tight_layout()

    # 显示表格
    plt.show()
