simout = sim('VehicleModel_SJTU', 'SimulationMode', 'normal', 'StopTime', '10');
plt_x = simout.x.Data;
plt_y = simout.y.Data;
plt_t = simout.tout;
plt_phi = simout.phi.Data;
plt_v = simout.velocity.Data;
figure(1);
scatter(plt_t, plt_v);
title('velocity');
xlabel('time');
ylabel('velocity');
axis equal;
grid on;

figure(2);
scatter(plt_x, plt_y);
title('position');
xlabel('X');
ylabel('Y');
axis equal;
grid on;

figure(3);
scatter(plt_t, plt_phi);
title('heading');
xlabel('time');
ylabel('heading');
axis equal;
grid on;
