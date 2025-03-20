function grad_value = getGradient(x, y, theta, grid, vx, vy)
    % 确保输入的 grid 是数值数组
    if ~isnumeric(grid)
        error('grid 必须是一个数值数组');
    end

    % 网格分辨率
    dx = 0.1;
    dy = 0.1;

    %坐标转换
    height=1484.3;
    x=x+346;
    y=height-(y+990);

    % 获取网格的最小 x 和 y 值
    x_min = min(grid(:, :, 1), [], 'all');
    y_min = min(grid(:, :, 2), [], 'all');


    % 计算索引
    i = round((x - x_min) / dx);
    j = round((y - y_min) / dy);

    % 确保索引在有效范围内
    i = max(1, min(i, size(vx, 1)));
    j = max(1, min(j, size(vx, 2)));

    % 查询梯度分量
    dx_val = vx(i, j);
    dy_val = vy(i, j);

    % 计算方向梯度
    grad_value = dx_val * cos(theta) + dy_val * sin(theta);
end