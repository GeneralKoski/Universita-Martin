function W = WcodaSA(lambda,s,N)

W = zeros(N+1);

K = poisspdf(0:(N-1),lambda*s)';

W(1:N,1:2) = [K K];

for j = 3:(N+1)
    W((j-1):N,j) = K(1:(end-j+2));
end
W(end,:) = 1-sum(W(1:end-1,:));
end