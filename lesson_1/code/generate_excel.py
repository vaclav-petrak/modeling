import xlsxwriter

def create_advanced_population_excel(filename="Population_Models.xlsx"):
    workbook = xlsxwriter.Workbook(filename)

    # ---------------------------------------------------------
    # COLOR & STYLE PALETTE 
    # ---------------------------------------------------------
    COLOR_HEADER_BG = '#244062'  
    COLOR_HEADER_TXT = '#FFFFFF' 
    COLOR_PARAM_BG = '#E6B8B7'   
    COLOR_ROW_EVEN = '#F2F2F2'   
    COLOR_ROW_ODD = '#FFFFFF'    
    CHART_COLORS = ['#4F81BD', '#C0504D'] # Blue, Red
    
    # Pre-calculate rows to allow for very small time steps
    MAX_ROWS = 500 
    # ---------------------------------------------------------

    # Setup Formats
    header_format = workbook.add_format({'bold': True, 'bg_color': COLOR_HEADER_BG, 'font_color': COLOR_HEADER_TXT, 'border': 1, 'align': 'center'})
    param_label_format = workbook.add_format({'bold': True, 'bg_color': COLOR_ROW_EVEN, 'border': 1, 'align': 'left'})
    param_input_format = workbook.add_format({'bold': True, 'bg_color': COLOR_PARAM_BG, 'border': 1, 'align': 'center'})
    
    # Number formatting (4 significant digits/decimal places)
    even_row_format = workbook.add_format({'bg_color': COLOR_ROW_EVEN, 'border': 1, 'align': 'center', 'num_format': '0.0000'})
    odd_row_format = workbook.add_format({'bg_color': COLOR_ROW_ODD, 'border': 1, 'align': 'center', 'num_format': '0.0000'})

    # ==========================================
    # SHEET 1: MALTHUSIAN MODEL
    # ==========================================
    ws_malthus = workbook.add_worksheet("Malthusian Model")
    ws_malthus.hide_gridlines(2)
    ws_malthus.set_column('A:C', 20)
    ws_malthus.set_column('F:F', 10) # Symbol
    ws_malthus.set_column('G:G', 22) # Description
    ws_malthus.set_column('H:H', 15) # Value

    # Parameter Table
    malthus_params = [
        ('P0', 'Initial Population', 10), 
        ('r', 'Growth Rate', 0.1), 
        ('dt', 'Time Step', 1.0),
        ('T_max', 'Total Sim Time', 50)
    ]
    
    ws_malthus.write_row('F2', ['Symbol', 'Description', 'Value'], header_format)
    for row_num, (sym, desc, val) in enumerate(malthus_params, start=2):
        ws_malthus.write(row_num, 5, sym, param_label_format)
        ws_malthus.write(row_num, 6, desc, param_label_format)
        ws_malthus.write(row_num, 7, val, param_input_format)

    # Headers & Data
    ws_malthus.write_row('A2', ['Time (t)', 'Explicit Formula', 'Euler Method'], header_format)

    # Initial Conditions (t=0)
    ws_malthus.write(2, 0, 0, even_row_format)
    ws_malthus.write(2, 1, '=$H$3', even_row_format)
    ws_malthus.write(2, 2, '=$H$3', even_row_format)

    # Formulas using IF and NA() for dynamic time bounds
    for row in range(3, MAX_ROWS + 2):
        fmt = even_row_format if row % 2 == 0 else odd_row_format
        # Time: IF(Previous is NA, NA, IF(Prev + dt <= T_max, Prev + dt, NA))
        ws_malthus.write_formula(row, 0, f'=IF(ISNA(A{row}), NA(), IF(A{row} + $H$5 <= $H$6 + 1E-9, A{row} + $H$5, NA()))', fmt)
        # Explicit: IF(Time is NA, NA, P0 * EXP(r * t))
        ws_malthus.write_formula(row, 1, f'=IF(ISNA(A{row+1}), NA(), $H$3 * EXP($H$4 * A{row+1}))', fmt)
        # Euler: IF(Time is NA, NA, P_prev + r * P_prev * dt)
        ws_malthus.write_formula(row, 2, f'=IF(ISNA(A{row+1}), NA(), C{row} + $H$4 * C{row} * $H$5)', fmt)

    # Malthusian Chart (Scatter with straight lines AND markers)
    chart_m = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
    chart_m.set_title({'name': 'Malthusian Exponential Growth'})
    chart_m.set_x_axis({'name': 'Time (t)'})
    chart_m.set_y_axis({'name': 'Population (P)'})
    chart_m.set_chartarea({'border': {'none': True}, 'fill': {'none': True}})
    
    for i in range(1, 3):
        chart_m.add_series({
            'name':       ['Malthusian Model', 1, i],
            'categories': ['Malthusian Model', 2, 0, MAX_ROWS + 1, 0],
            'values':     ['Malthusian Model', 2, i, MAX_ROWS + 1, i],
            'line':       {'color': CHART_COLORS[i-1], 'width': 2},
            'marker':     {'type': 'circle', 'size': 5, 'border': {'color': CHART_COLORS[i-1]}, 'fill': {'color': CHART_COLORS[i-1]}}
        })
    ws_malthus.insert_chart('F8', chart_m, {'x_scale': 1.5, 'y_scale': 1.2})


    # ==========================================
    # SHEET 2: LOGISTIC MODEL
    # ==========================================
    ws_logistic = workbook.add_worksheet("Logistic Model")
    ws_logistic.hide_gridlines(2)
    ws_logistic.set_column('A:C', 20)
    ws_logistic.set_column('F:F', 10)
    ws_logistic.set_column('G:G', 22)
    ws_logistic.set_column('H:H', 15)

    # Parameter Table
    logistic_params = [
        ('P0', 'Initial Population', 10), 
        ('r', 'Growth Rate', 0.1), 
        ('K', 'Carrying Capacity', 1000), 
        ('dt', 'Time Step', 1.0),
        ('T_max', 'Total Sim Time', 100)
    ]
    
    ws_logistic.write_row('F2', ['Symbol', 'Description', 'Value'], header_format)
    for row_num, (sym, desc, val) in enumerate(logistic_params, start=2):
        ws_logistic.write(row_num, 5, sym, param_label_format)
        ws_logistic.write(row_num, 6, desc, param_label_format)
        ws_logistic.write(row_num, 7, val, param_input_format)

    # Headers & Data
    ws_logistic.write_row('A2', ['Time (t)', 'Explicit Formula', 'Euler Method'], header_format)

    # Initial Conditions (t=0)
    ws_logistic.write(2, 0, 0, even_row_format)
    ws_logistic.write(2, 1, '=$H$3', even_row_format)
    ws_logistic.write(2, 2, '=$H$3', even_row_format)

    # Formulas using IF and NA()
    for row in range(3, MAX_ROWS + 2):
        fmt = even_row_format if row % 2 == 0 else odd_row_format
        ws_logistic.write_formula(row, 0, f'=IF(ISNA(A{row}), NA(), IF(A{row} + $H$6 <= $H$7 + 1E-9, A{row} + $H$6, NA()))', fmt)
        ws_logistic.write_formula(row, 1, f'=IF(ISNA(A{row+1}), NA(), $H$5 / (1 + (($H$5 - $H$3) / $H$3) * EXP(-$H$4 * A{row+1})))', fmt)
        ws_logistic.write_formula(row, 2, f'=IF(ISNA(A{row+1}), NA(), C{row} + $H$4 * C{row} * (1 - C{row} / $H$5) * $H$6)', fmt)

    # Logistic Chart (Scatter with straight lines AND markers)
    chart_l = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
    chart_l.set_title({'name': 'Logistic Growth'})
    chart_l.set_x_axis({'name': 'Time (t)'})
    chart_l.set_y_axis({'name': 'Population (P)'})
    chart_l.set_chartarea({'border': {'none': True}, 'fill': {'none': True}})
    
    for i in range(1, 3):
        chart_l.add_series({
            'name':       ['Logistic Model', 1, i],
            'categories': ['Logistic Model', 2, 0, MAX_ROWS + 1, 0],
            'values':     ['Logistic Model', 2, i, MAX_ROWS + 1, i],
            'line':       {'color': CHART_COLORS[i-1], 'width': 2},
            'marker':     {'type': 'circle', 'size': 5, 'border': {'color': CHART_COLORS[i-1]}, 'fill': {'color': CHART_COLORS[i-1]}}
        })
    ws_logistic.insert_chart('F9', chart_l, {'x_scale': 1.5, 'y_scale': 1.2})

    workbook.close()
    print(f"Excel file '{filename}' generated successfully!")

if __name__ == "__main__":
    create_advanced_population_excel()