%% 清理资源（每次仿真前运行）
% fclose(u);
% delete(u);
% clear u;

%% 启动仿真
% clear,clc,close all;

% 加载初始状态（根据需要调整）
% run("init.m"); 
% init(x, y, yaw, v0, acc);

%% UDP参数设置
localPort = 25001;        % MATLAB监听端口
remotePort = 25000;       % 控制端端口
remoteIP = '127.0.0.1';   % 控制端IP
chunkSize = 16;            % 每次发送的 double 数据数量

%% 创建UDP对象
u = udp(remoteIP, 'LocalPort', localPort, 'RemotePort', remotePort);
fopen(u);
modelName = 'VehicleModel_SJTU';  % 模型名称
load_system(modelName);
set_param(modelName, 'StopTime', '150');

%% 初始化变量
state_history = [];       % 存储当前控制周期内的状态
if_first = true;          % 首次运行标志

%% 发送就绪信号
readyMessage = 'ready';
fwrite(u, readyMessage, 'char');
disp("开始接收消息");

try
    while true
        %% 检查UDP消息
        if u.BytesAvailable > 0
            % 读取控制量
            data = fread(u, u.BytesAvailable, 'double');
            gear = data(1);
            acc = data(2);
            steer = data(3);
            continue_simulation = data(4);
            slope = data(5);
            disp("接收到消息");
            disp(slope)
            
            % 更新模型参数
            set_param(modelName, 'SimulationCommand', 'update'); % 更新模型
            
            % 处理历史数据
            send_data = state_history; 

            % 获取新状态
            if continue_simulation==0  
                if if_first
                    set_param(modelName, 'SimulationCommand', 'start');
                    if_first = false;
                else
                    set_param(modelName, 'SimulationCommand', 'step');
                end
            
                % 等待仿真暂停
                while ~strcmp(get_param(modelName,'SimulationStatus'),'paused')
                    pause(0.01);
                end

                current_x = out.x.Data(end);
                current_y = out.y.Data(end);
                current_v = out.velocity.Data(end);
                current_head = out.phi.Data(end);
                new_state = [current_v,current_head,current_x, current_y];
                %slope=getGradient(current_x, current_y, current_head, grid, vx, vy);
                % slope = -0.2;
                send_data = [send_data; new_state];  % 追加新状态
                send_data = reshape(send_data', [], 1);
                numChunks = ceil(numel(send_data) / chunkSize);
            
                % 分块发送组合数据，防止超出缓冲区
                for i = 1:numChunks
                    startIdx = (i - 1) * chunkSize + 1;
                    endIdx = min(i * chunkSize, numel(send_data));
                    chunk = send_data(startIdx:endIdx);
                    fwrite(u, chunk, 'double');
                    pause(0.01);  % 稍作延迟，避免发送过快
                end
                
                % 发送结束标志
                endMessage = [-10, -10, -10, -10];  % 假设结束标志是 4 个 -10
                fwrite(u, endMessage, 'double');
                state_history = [];  % 初始化新周期记录

            else
                %% 继续步进采集后续状态
                while u.BytesAvailable == 0
                    % 执行步进
                    set_param(modelName,'SimulationCommand','update');
                    set_param(modelName, 'SimulationCommand', 'step');
               
                    % 等待仿真暂停
                    while ~strcmp(get_param(modelName,'SimulationStatus'),'paused')
                        pause(0.01);
                    end
                    
                    % 记录状态
                    current_x = out.x.Data(end);
                    current_y = out.y.Data(end);
                    current_v = out.velocity.Data(end);
                    current_head = out.phi.Data(end);
                    %slope=getGradient(current_x, current_y, current_head, grid, vx, vy);
                    % slope = -0.2;
                    state_history = [state_history; 
                                   current_v,current_head,current_x, current_y];
                    % disp("运行但不发送")
                    if u.BytesAvailable > 0
                        break;
                    end
                end
            end
            
        else
            pause(0.1);  % 降低CPU占用
        end
    end
catch ME
    fprintf('运行异常: %s\n', ME.message);  % 打印错误信息
    fprintf('堆栈信息:\n');
    for i = 1:length(ME.stack)
        stackItem = ME.stack(i);
        fprintf('  文件: %s\n', stackItem.file);
        fprintf('  函数: %s\n', stackItem.name);
        fprintf('  行号: %d\n', stackItem.line);
        fprintf('  -----------------------------\n');
    end
end

%% 清理资源
fclose(u);
delete(u);
clear u;