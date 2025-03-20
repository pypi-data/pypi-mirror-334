modelName = 'VehicleModel_SJTU';  % 模型名称
load_system(modelName);
set_param(modelName, 'StopTime', '150');

set_param(modelName, 'SimulationCommand', 'update'); % 更新模型

set_param(modelName, 'SimulationCommand', 'start');

for step = 1:100
    set_param(modelName, 'SimulationCommand', 'step');
    % 等待仿真暂停
   while ~strcmp(get_param(modelName,'SimulationStatus'),'paused')
          pause(0.01);
   end
    current_x = out.x.Data(end);
    current_y = out.y.Data(end);
    current_v = out.velocity.Data(end);
    current_head = out.phi.Data(end);
    steer=steer+0.01;

    acc=1;
    set_param(modelName, 'SimulationCommand', 'update'); % 更新模型
end