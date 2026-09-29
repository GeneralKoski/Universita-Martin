iter=1e4;
N = 1e2;
res = zeros(1, iter+1);
    for i = 1:iter
        nn = randi(N);
        if nn <= res(i)
            res(i+1) = res(i) - 1; % estratto ...
        else
            res(i+1) = res(i) + 1; % ...
        end
    end
