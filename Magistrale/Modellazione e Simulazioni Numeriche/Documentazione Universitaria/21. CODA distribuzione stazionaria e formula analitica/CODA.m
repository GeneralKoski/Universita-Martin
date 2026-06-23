function [Qn] = CODA(t_max, den_arr, s, N_max, Q0)
    if nargin < 4
        display("invalid arguments");
        return;
    else
        if nargin == 4
            Q = 0;
        else
            Q = Q0;
        end
    end
    
    t_a = gen_a(den_arr);
    if Q == 0
        t_s = inf;
    else
        t_s = s * rand();
    end
    
    Qn = [];
    t = min([t_a, t_s, t_max]);
    if (isfinite(N_max))
        while (t < t_max)
            if (t == t_a)
                % gestici arrivo
                t_a = t + gen_a(den_arr);
                if ~isfinite(t_s)
                    t_s = t + s;
                else
                    if (Q < N_max)
                        Q = Q + 1;
                    end
                end
            else
                % gestisci servizio
                Qn(end + 1) = Q;
                if Q == 0
                    t_s = inf;
                else
                    Q = Q - 1;
                    t_s = t + s;
                end
            end
            t = min([t_a, t_s, t_max]);
        end
    else
        while (t < t_max)
            if (t == t_a)
                % gestici arrivo
                t_a = t + gen_a(den_arr);
                if ~isfinite(t_s)
                    t_s = t + s;
                else   
                    Q = Q + 1;
                end
            else
                % gestisci servizio
                Qn(end + 1) = Q;
                if Q == 0
                    t_s = inf;
                else
                    Q = Q - 1;
                    t_s = t + s;
                end
            end
            t = min([t_a, t_s, t_max]);
        end
    end
end

function a = gen_a(lambda)
    a = -(1 / lambda) * log(rand());
end

