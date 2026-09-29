nn100 = biglie(1e2,1e7);
ff100 = hist(nn100(1e3:end),0:1e2)/length(nn100(1e3:end));

nn500 = biglie(5e2,1e8);
ff500 = hist(nn500(1e3:end),0:5e2)/length(nn500(1e3:end));

nn1000 = biglie(1e3,1e9);
ff1000 = hist(nn1000(1e3:end),0:1e3)/length(nn1000(1e3:end));