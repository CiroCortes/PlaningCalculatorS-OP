from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
from services.sop_calculator import SOPCalculatorService
from .models import Product, PurchaseRequest, Brand
import os
import json

class SOPDashboardView(View):
    template_name = 'sop/dashboard.html'

    def get(self, request):
        products = Product.objects.all().order_by('brand__name', 'item_code')
        active_requests = PurchaseRequest.objects.all().order_by('-created_at')
        
        # Manejo de Roles (Planificador vs Solicitante)
        role = request.GET.get('role') or request.session.get('active_role', 'planner')
        request.session['active_role'] = role

        # Carga opcional de Excel con archivo por defecto en raíz como fallback
        active_excel_path = request.session.get('active_excel_path')
        file_name = request.session.get('active_excel_name')

        if not active_excel_path or not os.path.exists(active_excel_path):
            default_path = os.path.join(os.getcwd(), "S&OP - Análisis HIAB (Julio) 1.xlsx")
            if os.path.exists(default_path):
                active_excel_path = default_path
                file_name = "S&OP - Análisis HIAB (Julio) 1.xlsx (Por Defecto)"
                request.session['active_excel_path'] = default_path
                request.session['active_excel_name'] = file_name

        context = {
            'products': products,
            'active_requests': active_requests,
            'file_name': file_name,
            'success': False,
            'status_choices': PurchaseRequest.STATUS_CHOICES,
            'active_role': role
        }
        
        if active_excel_path and os.path.exists(active_excel_path):
            try:
                metrics = SOPCalculatorService.calculate_sop_metrics(active_excel_path)
                context['metrics'] = metrics
                context['success'] = True
            except Exception as e:
                context['error'] = f'Error al procesar la planilla activa: {str(e)}'
                
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        
        # 1. ACCIÓN: CARGAR NUEVA PLANILLA
        if action == 'upload_excel':
            excel_file = request.FILES.get('excel_file')
            if excel_file:
                old_path = request.session.get('active_excel_path')
                if old_path and os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except:
                        pass
                
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                file_path = fs.path(filename)
                
                request.session['active_excel_path'] = file_path
                request.session['active_excel_name'] = excel_file.name
                
        # 2. ACCIÓN: CREAR SOLICITUD DESDE LISTADO BORRADOR (CARRITO)
        elif action == 'add_request_list':
            requested_by = request.POST.get('requested_by')
            items_json = request.POST.get('request_items_json')
            
            if requested_by and items_json:
                try:
                    items = json.loads(items_json)
                    for item in items:
                        product_id = item.get('product_id')
                        quantity = item.get('quantity')
                        unit_cost = item.get('unit_cost')
                        
                        if product_id and quantity and unit_cost:
                            product = Product.objects.get(id=product_id)
                            PurchaseRequest.objects.create(
                                product=product,
                                quantity=int(quantity),
                                unit_cost_usd=float(unit_cost),
                                requested_by=requested_by
                            )
                except Exception as e:
                    request.session['form_error'] = f"Error al procesar lote de solicitudes: {str(e)}"

        # 3. ACCIÓN: EVALUAR SOLICITUD (PLANIFICADOR / ADMIN)
        elif action == 'evaluate_request':
            request_id = request.POST.get('request_id')
            status = request.POST.get('status')
            planned_date = request.POST.get('planned_date')
            decision_note = request.POST.get('decision_note')
            
            if request_id and status:
                try:
                    req_obj = PurchaseRequest.objects.get(id=request_id)
                    req_obj.status = status
                    req_obj.planned_date = planned_date
                    req_obj.decision_note = decision_note
                    req_obj.save()
                except Exception as e:
                    pass
                    
        # 4. ACCIÓN: ELIMINAR SOLICITUD DE COMPRA
        elif action == 'delete_request':
            request_id = request.POST.get('request_id')
            if request_id:
                try:
                    PurchaseRequest.objects.filter(id=request_id).delete()
                except Exception as e:
                    pass
                    
        return redirect('sop_dashboard')
