function [psiInt,x,y] = generate_ref_trajectory(t,x_dot)
     y=3*tanh(t-t(size(t,2))/2);
     for i=1:size(t,2)
         x(i) = x_dot*t(i);
     end
     dx = x(2:size(t,2)) - x(1:size(t,2)-1);
     dy = y(2:size(t,2)) - y(1:size(t,2)-1);
     
  
     psi(2:size(t,2)) = atan2(dy,dx);
     psi(1)=psi(2);

     psiInt=psi;
     dpsi=psi(2:size(psi,2))-psi(1:size(psi,2)-1);

     for i=1:size(psiInt,2)-1
        if dpsi(i)<-pi
            psiInt(i+1)=psiInt(i)+(dpsi(i)+2*pi);
        elseif dpsi(i)>pi
            psiInt(i+1)=psiInt(i)+(dpsi(i)-2*pi);
        else
            psiInt(i+1)=psiInt(i)+dpsi(i);
        end
     end 
end