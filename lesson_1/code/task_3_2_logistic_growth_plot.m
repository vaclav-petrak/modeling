figure(1)
tiledlayout(2, 2)
nexttile
    plot(t_num, P_num, LineWidth=2, Color = "#0072BD")
    title('Population')
    xlabel('Time (years)') 
    ylabel('Population (milions)')

nexttile 
    plot(t_num, P_diff*1000, LineWidth=2,Color = "#D95319")
    title('Population growth')
    xlabel('Time (years)') 
    ylabel( {'Population change';'(thousands/month)'})

nexttile 
    plot(P_num, 1000*P_diff./P_num, LineWidth=2, Color="#EDB120")
     title('Per capita growth rate vs population')
    ylabel('Per capita growth rate')
    xlabel('Population (milions)')
 
nexttile 
    plot(P_num,1000*P_diff, LineWidth=2,Color = "#77AC30")
    title('Population growth rate vs population')
    ylabel('Population growth rate')
    xlabel('Population (milions)')