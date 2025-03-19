import matplotlib.pyplot as plt

def plot_regression_line(x, y, fitted_values, x_label, y_label, title):
    plt.scatter(x, y, color='blue', label='Dữ liệu thực tế')
    plt.plot(x, fitted_values, color='red', label='Hồi quy tuyến tính')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()
