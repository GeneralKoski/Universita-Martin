function c = MYautocorr(QQ,n)

if length(QQ) < 50*n
    disp(['Your sample is small... consider getting a larger number ' ...
          'of measurements'])
    return
end

for i = 1:n
   c(i) = mean(QQ(1:(end+1-i)).*QQ(i:end)); 
end

c = c - mean(QQ)^2; %Cff(t)

c = c/c(1); %pho_ff(t)
end