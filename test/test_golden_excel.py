import os
import pytest
from services.sop_calculator import SOPCalculatorService

@pytest.mark.django_db
def test_golden_dataset_metrics():
    """
    Valida que los KPIs calculados por el motor de Django coincidan al 100% 
    con las celdas consolidadas del Resumen del Excel original, considerando 
    que tanto 'En Proceso' como 'Solicitud de Compras' se inicializan en 0 y
    se alimentan dinámicamente de la BD.
    """
    excel_path = "S&OP - Análisis HIAB (Julio) 1.xlsx"
    assert os.path.exists(excel_path), f"El archivo {excel_path} debe existir en la raíz."
    
    # Ejecutamos el motor de cálculo
    metrics = SOPCalculatorService.calculate_sop_metrics(excel_path)
    
    global_m = metrics['global']
    demand = global_m['demand']
    inventory = global_m['inventory']
    
    # 🎯 VALIDACIONES DE VALOR (DINERO USD) - Con solicitudes iniciales vaciadas del Excel
    assert abs(inventory['initial_inventory_val'] - 15706658.63) < 1.0
    assert abs(inventory['final_inventory_val'] - 8268477.74) < 1.0
    assert abs(inventory['final_projected_val'] - 8268477.74) < 1.0
    
    # 🎯 VALIDACIONES DE CANTIDAD (UNIDADES) - Con solicitudes iniciales vaciadas del Excel
    assert inventory['initial_inventory_qty'] == 163
    assert inventory['final_inventory_qty'] == 114
    assert inventory['final_projected_qty'] == 114

    # 🎯 VALIDACIONES DE ROTACIÓN
    assert demand['rotation_months'] == 8.15
    assert demand['rotation_with_purchase_months'] == 7.09

    print("OK - Todos los KPIs coinciden perfectamente con los nuevos cálculos dinámicos!")
