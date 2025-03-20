currentDir = pwd;
cd ..
cd(currentDir);
x0=66.5;
y0=257.9;
yaw=-1.125;
v0=3;
acc=0.0;
gear=2;
steer=0.0;
slope=-0.2;
load('a_brake.mat');
load('a_thr.mat');
load('brake.mat');
load('thr.mat');
modelName='VehicleModel_SJTU';
run('control_simulink.m');
