simout = sim('VehicleModel_SJTU', 'StopTime', '10');

x = simout.x.data;
y = simout.y.data;
v = simout.velocity.data;
phi = simout.phi.data;
t = simout.tout;

figure; % 创建一个新窗口
plot(x, y, 'LineWidth', 2); % 绘制折线图，设置线条宽度
title('position'); % 添加标题
xlabel('X 轴'); % 添加 X 轴标签
ylabel('Y 轴'); % 添加 Y 轴标签
grid on; % 添加网格
axis equal;

figure; % 创建一个新窗口
plot(t, v, 'LineWidth', 2); % 绘制折线图，设置线条宽度
title('velociity'); % 添加标题
xlabel('time'); % 添加 X 轴标签
ylabel('velocity'); % 添加 Y 轴标签
grid on; % 添加网格
axis equal;

figure; % 创建一个新窗口
plot(t, phi, 'LineWidth', 2); % 绘制折线图，设置线条宽度
title('phi'); % 添加标题
xlabel('time'); % 添加 X 轴标签
ylabel('phi'); % 添加 Y 轴标签
grid on; % 添加网格
axis equal;
