function res = MYgss(x,x0,sgm)

if nargin == 1
    x0 = 0;
    sgm = 1;
end

res = 1/sqrt(2*pi*sgm^2) * exp( - ((x-x0).^2)/(2*sgm^2));

end
