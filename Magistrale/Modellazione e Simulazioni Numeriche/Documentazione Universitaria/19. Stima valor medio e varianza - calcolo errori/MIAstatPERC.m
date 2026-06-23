clear
clc

N = 1000;
p = [0.1:0.05:0.3 0.3:0.005:0.75 0.8:0.05:0.95];

prob = zeros(1, length(p));
LL = 10:10:30;

StatCluster = zeros(N,length(p),length(LL),5);

for ij = 1:length(LL)
    L = LL(ij);

    for ii = 1:length(p)
        pp = p(ii);
    
        s = 0;
        for j = 1:N
            res = CercaCluster(L, pp);

            StatCluster(j,ii,ij,1) = length(res.clusters);
            StatCluster(j,ii,ij,2) = mean(res.clusters);
            StatCluster(j,ii,ij,3) = max(res.clusters);
            StatCluster(j,ii,ij,4) = res.percolazioneLR;
            StatCluster(j,ii,ij,5) = res.percolazioneTB;
            
            tmp = res.percolazioneTB || res.percolazioneLR;
    
            s = s + tmp;
        end
    
        prob(ii) = s / N;
    
    
    end
    hold on
    plot(p, prob);

end

