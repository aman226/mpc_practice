state = [5;-2;3];

for i=1:500
    hold on
    state = rungeKuttaSolver([0 1 0;0 0 1;-10 -5 -2],[1;2;3],state,0,0.01);
    plot(i*0.01,state(1),LineStyle='-',Marker='.')
end