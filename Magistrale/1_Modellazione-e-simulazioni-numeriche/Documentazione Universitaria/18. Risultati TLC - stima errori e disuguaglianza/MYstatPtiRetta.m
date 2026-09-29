quale = input('quale? ')
NN = input('quanti? ')

switch(quale)

    case 1

        tic,
        for ii=1:NN

            RR = puntiRetta(0.8,5,1e4);
            MIEmedie_4_1e4(end+1) = sum(RR(1,:).*RR(2,:));

        end
        toc

    case 2

        tic,
        for ii=1:NN

            RR = puntiRetta(0.8,5,1e3);
            MIEmedie_4_1e3(end+1) = sum(RR(1,:).*RR(2,:));

        end
        toc

    case 3

        tic,
        for ii=1:NN

            RR = puntiRetta(1.5,4,1e4);
            MIEmedie_6_1e4(end+1) = sum(RR(1,:).*RR(2,:));

        end
        toc

    otherwise

        return

end
