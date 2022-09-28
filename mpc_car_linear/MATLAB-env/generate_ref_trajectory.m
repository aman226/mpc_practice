function generate_ref_trajectory(t,x_dot)
     y=9*tanh(t-t(size(t,2))/2);
     for i=1:size(t,2)
         x(i) = x_dot*t(i);
     end
     dx = x(2:size(t,2)) - x(1:size(t,2)-1);
     dy = y(2:size(t,2)) - y(1:size(t,2)-1);
     
     for i=1:size(t,2)-1
         psi(i+1) = atan2(dy(i),dx(i));
     end

     plot(x(2:size(t,2)),psi)   
end