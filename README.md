# PESCO S.A. - Calculadora S&OP Planning & Decisions

Este proyecto es un sistema de planificación de ventas y operaciones (**S&OP**) diseñado a medida para **PESCO S.A.** Permite consolidar la información logística del ERP SAP cargada a través de planillas Excel y complementarla dinámicamente con solicitudes de compra emitidas en tiempo real por el equipo de ventas.

---

## 📊 Fórmulas y Cálculos del Dashboard S&OP

El motor de cálculo híbrido del sistema (**`services/sop_calculator.py`**) procesa los datos de la pestaña **`Resumen`** del Excel y los consolida con la base de datos de Django en tiempo real utilizando las siguientes ecuaciones:

### 1. Demanda y Objetivos (Demand & Targets)
*   **Entregado últimos 12 meses**: Cantidad acumulada física (`delivered_12m_qty`) y costo total (`delivered_12m_val`) extraídos del Excel.
*   **Entregado 2026**: Progreso actual del año en cantidad (`delivered_2026_qty`) y valor (`delivered_2026_val`) extraídos del Excel.
*   **Backlog**: Pedidos comprometidos pendientes de entrega en cantidad (`backlog_qty`) y valor (`backlog_val`) extraídos del Excel.
*   **Cotizado (NEC 3)**: Cotizaciones en curso en cantidad (`cotizado_qty`) y valor (`cotizado_val`) extraídos del Excel.
*   **Presupuesto 2026**: La meta anual asignada en cantidad (`budget_qty`) y valor (`budget_val`).
*   **Cumplimiento Presupuesto (%)**:
    $$\text{Cumplimiento Cantidad} = \left( \frac{\text{Entregado 2026 Qty}}{\text{Presupuesto 2026 Qty}} \right) \times 100\%$$
    $$\text{Cumplimiento Dinero} = \left( \frac{\text{Entregado 2026 Val}}{\text{Presupuesto 2026 Val}} \right) \times 100\%$$

---

### 2. Inventario y Suministro (Supply & Inventory)
*   **Stock (+)**: Cantidad física actualmente en bodega y su valorización.
*   **Tránsito Real (+)**: Unidades en importación física confirmada y su costo.
*   **Tránsito Proyectado (+)**: Unidades en importación planificada y su costo.
*   **En Proceso (+)**:
    *   *Excel Estático*: Se ignora/vacía a 0 para evitar duplicación de datos manuales.
    *   *Dynamic Web App*: Suma acumulada de solicitudes de compra creadas en la aplicación Django que se encuentran en estado **`PENDIENTE`** o **`APROBADO`**.
        $$\text{En Proceso Qty} = \sum (\text{Cantidad de Solicitudes Activas})$$
*   **Inventario Inicial**:
    $$\text{Inventario Inicial Qty} = \text{Stock Qty} + \text{Tránsito Real Qty} + \text{Tránsito Proyectado Qty} + \text{En Proceso Qty}$$
*   **Backlog (-)**: Unidades comprometidas que restan inventario.
*   **Inventario Final**:
    $$\text{Inventario Final Qty} = \text{Inventario Inicial Qty} - \text{Backlog Qty}$$
*   **Solicitud de compras (+)**: Suma de las solicitudes de compra **`APROBADAS`** en la base de datos de Django.
*   **Inventario Final Proyectado**:
    $$\text{Inventario Final Proyectado Qty} = \text{Inventario Final Qty} + \text{Solicitud de compras Qty}$$

---

### 3. Rotación e Indicadores de Negocio
*   **Demanda Promedio Mensual**:
    $$\text{Demanda Mensual Qty} = \frac{\text{Entregado últimos 12 meses Qty} + \text{Backlog Qty}}{12}$$
*   **Rotación Estándar (Meses de Cobertura)**:
    $$\text{Rotación estándar} = \frac{\text{Inventario Final Qty}}{\text{Demanda Mensual Qty}}$$
*   **Rotación con Solicitud (Meses Proyectados)**:
    $$\text{Rotación con Solicitud} = \frac{\text{Inventario Final Proyectado Qty}}{\text{Demanda Mensual Qty}}$$

*Este último indicador es el corazón de la toma de decisiones S&OP: si un solicitante pide 70 grúas, el planificador ve instantáneamente si la rotación se dispara a niveles excesivos (ej: de 8.1 a 12.5 meses), permitiendo refutar la compra con base numérica.*

---

## ⚙️ Tecnologías Utilizadas
*   **Django 5.2**: Servidor y base de datos (con modelos de solicitudes y estados `PENDIENTE`, `APROBADO`, `RECHAZADO`).
*   **OpenPyXL**: Extracción híbrida de datos de celdas consolidadas y filas individuales (16 a 111) de la hoja `Resumen`.
*   **TailwindCSS**: Interfaz visual ultra-premium y responsiva con paleta de colores corporativa PESCO.
*   **Chart.js**: Visualización de gráficos para distribución de inventarios y cumplimiento de presupuestos.
*   **JavaScript (Reactivo)**: Filtrado instantáneo y re-dibujado dinámico de la ficha individual del SKU al buscar o seleccionar un código.
