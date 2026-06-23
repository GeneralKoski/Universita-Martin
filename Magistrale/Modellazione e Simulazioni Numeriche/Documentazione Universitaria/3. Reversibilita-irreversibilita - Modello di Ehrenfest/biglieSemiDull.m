function res=biglieSemiDull(N, iter)
% qui ci va io commento ...

biglie = ones(1,N);
res = zeros(1,iter);

for j = 1: iter
    estr = randi(N);
    biglie(estr) = ~biglie(estr);
    res(j) = sum(biglie);
end

end