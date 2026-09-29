function res = TreCarteMovie(N,MYfile,ff)
% res = TreCarteMovie(N,MYfile,ff)
% MYfile è una stringa, ad esempio 'filmino.avi'
% ff rappresenta il numero di frame per secondo
% ... NON COMPLETO!!! Solo lo scheletro del movie...

mov = VideoWriter(MYfile);
mov.FrameRate=ff;
open(mov);

...
    
WW = [0 0 0];
bar(WW);
axis([0.5 3.5 0 1.0]);

    
for i = 1:N,

    ...
        
    WW = [W_1st W_ch W_ra];
    
    bar(WW);
    axis([0.5 3.5 0 1.0]);
    current = getframe;
    writeVideo(mov,current); 

end;

close(mov);

res(1) = W_1stchoice/N;
res(2) = W_change/N;
res(3) = W_rand/N;
