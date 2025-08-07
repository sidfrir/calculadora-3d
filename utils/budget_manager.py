import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Budget:
    def __init__(self, name: str, period: str, amount: float):
        self.id = self._generate_id()
        self.name = name
        self.period = period  # monthly, quarterly, yearly
        self.amount = amount
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.start_date = datetime.now().isoformat()
        self.end_date = self._calculate_end_date(period)
        self.status = "active"  # active, completed, archived
        self.category = "general"  # general, materials, labor, maintenance, marketing
        self.description = ""
        self.spent_amount = 0.0
        self.reserved_amount = 0.0
        self.notes = ""
        self.alert_threshold = 0.8  # Porcentaje para alerta de gasto
        self.transactions = []  # Lista de transacciones
    
    def _generate_id(self):
        """Genera un ID único para el presupuesto."""
        import uuid
        return str(uuid.uuid4())
    
    def _calculate_end_date(self, period: str):
        """Calcula la fecha de finalización basada en el período."""
        from datetime import timedelta
        
        start_date = datetime.now()
        if period == "monthly":
            # Aproximadamente un mes
            end_date = start_date + timedelta(days=30)
        elif period == "quarterly":
            # 3 meses
            end_date = start_date + timedelta(days=90)
        elif period == "yearly":
            # 1 año
            end_date = start_date + timedelta(days=365)
        else:
            # Por defecto 30 días
            end_date = start_date + timedelta(days=30)
        
        return end_date.isoformat()
    
    def to_dict(self):
        """Convierte el presupuesto a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "period": self.period,
            "amount": self.amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "category": self.category,
            "description": self.description,
            "spent_amount": self.spent_amount,
            "reserved_amount": self.reserved_amount,
            "notes": self.notes,
            "alert_threshold": self.alert_threshold,
            "transactions": self.transactions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea un presupuesto desde un diccionario."""
        budget = cls(
            data["name"], 
            data["period"], 
            data["amount"]
        )
        budget.id = data["id"]
        budget.created_at = data["created_at"]
        budget.updated_at = data["updated_at"]
        budget.start_date = data.get("start_date", datetime.now().isoformat())
        budget.end_date = data.get("end_date", budget._calculate_end_date(data["period"]))
        budget.status = data.get("status", "active")
        budget.category = data.get("category", "general")
        budget.description = data.get("description", "")
        budget.spent_amount = data.get("spent_amount", 0.0)
        budget.reserved_amount = data.get("reserved_amount", 0.0)
        budget.notes = data.get("notes", "")
        budget.alert_threshold = data.get("alert_threshold", 0.8)
        budget.transactions = data.get("transactions", [])
        return budget
    
    def get_remaining_amount(self):
        """Obtiene el monto restante del presupuesto."""
        return self.amount - self.spent_amount - self.reserved_amount
    
    def get_utilization_percentage(self):
        """Obtiene el porcentaje de utilización del presupuesto."""
        if self.amount > 0:
            return (self.spent_amount / self.amount) * 100
        return 0
    
    def is_over_budget(self):
        """Verifica si se ha excedido el presupuesto."""
        return self.spent_amount > self.amount
    
    def is_near_limit(self):
        """Verifica si se está cerca del límite del presupuesto."""
        return self.get_utilization_percentage() >= (self.alert_threshold * 100)
    
    def add_transaction(self, amount: float, description: str, category: str = ""):
        """Añade una transacción al presupuesto."""
        transaction = {
            "id": self._generate_id(),
            "amount": amount,
            "description": description,
            "category": category or self.category,
            "date": datetime.now().isoformat(),
            "type": "expense" if amount > 0 else "income"
        }
        
        self.transactions.append(transaction)
        self.spent_amount += amount
        self.updated_at = datetime.now().isoformat()
        
        return transaction

class Transaction:
    def __init__(self, amount: float, description: str, budget_id: str = ""):
        self.id = self._generate_id()
        self.amount = amount
        self.description = description
        self.budget_id = budget_id
        self.date = datetime.now().isoformat()
        self.category = "general"
        self.type = "expense" if amount > 0 else "income"
        self.notes = ""
        self.related_quote_id = ""
        self.related_project_id = ""
    
    def _generate_id(self):
        """Genera un ID único para la transacción."""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self):
        """Convierte la transacción a diccionario."""
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "budget_id": self.budget_id,
            "date": self.date,
            "category": self.category,
            "type": self.type,
            "notes": self.notes,
            "related_quote_id": self.related_quote_id,
            "related_project_id": self.related_project_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea una transacción desde un diccionario."""
        transaction = cls(
            data["amount"], 
            data["description"], 
            data.get("budget_id", "")
        )
        transaction.id = data["id"]
        transaction.date = data["date"]
        transaction.category = data.get("category", "general")
        transaction.type = data.get("type", "expense")
        transaction.notes = data.get("notes", "")
        transaction.related_quote_id = data.get("related_quote_id", "")
        transaction.related_project_id = data.get("related_project_id", "")
        return transaction

class BudgetManager:
    def __init__(self, budgets_file="budgets.json", transactions_file="transactions.json"):
        self.budgets_file = budgets_file
        self.transactions_file = transactions_file
        self.budgets = self.load_budgets()
        self.transactions = self.load_transactions()
    
    def load_budgets(self):
        """Carga los presupuestos desde el archivo."""
        if os.path.exists(self.budgets_file):
            try:
                with open(self.budgets_file, 'r') as f:
                    data = json.load(f)
                    return [Budget.from_dict(budget_data) for budget_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar presupuestos: {e}")
                return []
        return []
    
    def save_budgets(self):
        """Guarda los presupuestos en el archivo."""
        try:
            with open(self.budgets_file, 'w') as f:
                json.dump([budget.to_dict() for budget in self.budgets], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar presupuestos: {e}")
            return False
    
    def load_transactions(self):
        """Carga las transacciones desde el archivo."""
        if os.path.exists(self.transactions_file):
            try:
                with open(self.transactions_file, 'r') as f:
                    data = json.load(f)
                    return [Transaction.from_dict(transaction_data) for transaction_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar transacciones: {e}")
                return []
        return []
    
    def save_transactions(self):
        """Guarda las transacciones en el archivo."""
        try:
            with open(self.transactions_file, 'w') as f:
                json.dump([transaction.to_dict() for transaction in self.transactions], f, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar transacciones: {e}")
            return False
    
    def create_budget(self, name: str, period: str, amount: float):
        """Crea un nuevo presupuesto."""
        budget = Budget(name, period, amount)
        self.budgets.append(budget)
        self.save_budgets()
        return budget
    
    def get_budget(self, budget_id: str):
        """Obtiene un presupuesto por ID."""
        for budget in self.budgets:
            if budget.id == budget_id:
                return budget
        return None
    
    def get_budgets(self, status=None, category=None):
        """Obtiene todos los presupuestos, opcionalmente filtrados."""
        filtered_budgets = self.budgets
        
        if status:
            filtered_budgets = [b for b in filtered_budgets if b.status == status]
        
        if category:
            filtered_budgets = [b for b in filtered_budgets if b.category == category]
        
        return filtered_budgets
    
    def update_budget(self, budget_id: str, **kwargs):
        """Actualiza un presupuesto con los valores proporcionados."""
        budget = self.get_budget(budget_id)
        if not budget:
            return False, "Presupuesto no encontrado"
        
        # Actualizar campos proporcionados
        for key, value in kwargs.items():
            if hasattr(budget, key):
                setattr(budget, key, value)
        
        # Actualizar fecha de modificación
        budget.updated_at = datetime.now().isoformat()
        
        self.save_budgets()
        return True, "Presupuesto actualizado"
    
    def delete_budget(self, budget_id: str):
        """Elimina un presupuesto."""
        budget = self.get_budget(budget_id)
        if not budget:
            return False, "Presupuesto no encontrado"
        
        self.budgets.remove(budget)
        self.save_budgets()
        return True, "Presupuesto eliminado"
    
    def search_budgets(self, query: str):
        """Busca presupuestos por nombre o descripción."""
        query = query.lower()
        results = []
        
        for budget in self.budgets:
            if (query in budget.name.lower() or 
                query in budget.description.lower() or
                query in budget.category.lower()):
                results.append(budget)
        
        return results
    
    def get_budget_statistics(self):
        """Obtiene estadísticas de presupuestos."""
        if not self.budgets:
            return None
        
        total_budgets = len(self.budgets)
        active_budgets = len([b for b in self.budgets if b.status == "active"])
        completed_budgets = len([b for b in self.budgets if b.status == "completed"])
        
        # Agrupar por categoría
        categories = {}
        for budget in self.budgets:
            category = budget.category
            if category not in categories:
                categories[category] = {
                    "count": 0,
                    "total_amount": 0,
                    "total_spent": 0
                }
            categories[category]["count"] += 1
            categories[category]["total_amount"] += budget.amount
            categories[category]["total_spent"] += budget.spent_amount
        
        # Calcular totales
        total_amount = sum(b.amount for b in self.budgets)
        total_spent = sum(b.spent_amount for b in self.budgets)
        
        # Presupuestos excedidos
        over_budget_count = len([b for b in self.budgets if b.is_over_budget()])
        
        # Presupuestos cerca del límite
        near_limit_count = len([b for b in self.budgets if b.is_near_limit() and not b.is_over_budget()])
        
        stats = {
            "total_budgets": total_budgets,
            "active_budgets": active_budgets,
            "completed_budgets": completed_budgets,
            "total_amount": total_amount,
            "total_spent": total_spent,
            "utilization_rate": (total_spent / total_amount * 100) if total_amount > 0 else 0,
            "over_budget_count": over_budget_count,
            "near_limit_count": near_limit_count,
            "categories": categories
        }
        
        return stats
    
    def add_transaction(self, amount: float, description: str, budget_id: str = "", category: str = ""):
        """Añade una transacción."""
        transaction = Transaction(amount, description, budget_id)
        transaction.category = category or "general"
        
        self.transactions.append(transaction)
        
        # Si hay un presupuesto asociado, actualizarlo
        if budget_id:
            budget = self.get_budget(budget_id)
            if budget:
                budget.add_transaction(amount, description, category)
                self.save_budgets()
        
        self.save_transactions()
        return transaction
    
    def get_transactions(self, budget_id=None, category=None, transaction_type=None):
        """Obtiene transacciones, opcionalmente filtradas."""
        filtered_transactions = self.transactions
        
        if budget_id:
            filtered_transactions = [t for t in filtered_transactions if t.budget_id == budget_id]
        
        if category:
            filtered_transactions = [t for t in filtered_transactions if t.category == category]
        
        if transaction_type:
            filtered_transactions = [t for t in filtered_transactions if t.type == transaction_type]
        
        # Ordenar por fecha (más recientes primero)
        filtered_transactions.sort(key=lambda x: x.date, reverse=True)
        
        return filtered_transactions
    
    def get_over_budget_budgets(self):
        """Obtiene presupuestos que han excedido su límite."""
        return [b for b in self.budgets if b.is_over_budget()]
    
    def get_near_limit_budgets(self):
        """Obtiene presupuestos cerca de su límite."""
        return [b for b in self.budgets if b.is_near_limit() and not b.is_over_budget()]
    
    def get_budget_utilization(self, budget_id: str):
        """Obtiene la utilización de un presupuesto específico."""
        budget = self.get_budget(budget_id)
        if not budget:
            return None
        
        return {
            "spent_amount": budget.spent_amount,
            "reserved_amount": budget.reserved_amount,
            "remaining_amount": budget.get_remaining_amount(),
            "utilization_percentage": budget.get_utilization_percentage(),
            "is_over_budget": budget.is_over_budget(),
            "is_near_limit": budget.is_near_limit()
        }
    
    def reserve_amount(self, budget_id: str, amount: float, description: str = ""):
        """Reserva una cantidad de un presupuesto."""
        budget = self.get_budget(budget_id)
        if not budget:
            return False, "Presupuesto no encontrado"
        
        if budget.get_remaining_amount() < amount:
            return False, "Fondos insuficientes para la reserva"
        
        budget.reserved_amount += amount
        budget.updated_at = datetime.now().isoformat()
        
        # Añadir transacción de reserva
        self.add_transaction(0, f"Reserva: {description}", budget_id, budget.category)
        
        self.save_budgets()
        return True, f"${amount} reservados exitosamente"
    
    def release_reserved_amount(self, budget_id: str, amount: float):
        """Libera una cantidad reservada de un presupuesto."""
        budget = self.get_budget(budget_id)
        if not budget:
            return False, "Presupuesto no encontrado"
        
        if budget.reserved_amount < amount:
            return False, "Cantidad reservada insuficiente"
        
        budget.reserved_amount -= amount
        budget.updated_at = datetime.now().isoformat()
        
        self.save_budgets()
        return True, f"${amount} liberados exitosamente"
    
    def get_budgets_by_category(self, category: str):
        """Obtiene presupuestos de una categoría específica."""
        return [b for b in self.budgets if b.category == category]
    
    def get_budgets_by_period(self, period: str):
        """Obtiene presupuestos de un período específico."""
        return [b for b in self.budgets if b.period == period]
    
    def complete_budget(self, budget_id: str):
        """Marca un presupuesto como completado."""
        return self.update_budget(budget_id, status="completed")
    
    def get_monthly_summary(self, year: int, month: int):
        """Obtiene un resumen de transacciones para un mes específico."""
        from datetime import datetime
        
        monthly_transactions = []
        for transaction in self.transactions:
            try:
                trans_date = datetime.fromisoformat(transaction.date)
                if trans_date.year == year and trans_date.month == month:
                    monthly_transactions.append(transaction)
            except Exception:
                continue
        
        total_income = sum(t.amount for t in monthly_transactions if t.type == "income")
        total_expenses = sum(t.amount for t in monthly_transactions if t.type == "expense")
        
        return {
            "year": year,
            "month": month,
            "transactions": monthly_transactions,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": total_income - total_expenses,
            "transaction_count": len(monthly_transactions)
        }
    
    def export_budgets_to_csv(self, filename: str):
        """Exporta la lista de presupuestos a un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'name', 'period', 'amount', 'spent_amount', 'status',
                    'category', 'start_date', 'end_date'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for budget in self.budgets:
                    writer.writerow({
                        'name': budget.name,
                        'period': budget.period,
                        'amount': budget.amount,
                        'spent_amount': budget.spent_amount,
                        'status': budget.status,
                        'category': budget.category,
                        'start_date': budget.start_date,
                        'end_date': budget.end_date
                    })
            
            return True, f"Presupuestos exportados a {filename}"
        except Exception as e:
            return False, f"Error al exportar presupuestos: {str(e)}"
    
    def export_transactions_to_csv(self, filename: str):
        """Exporta la lista de transacciones a un archivo CSV."""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'description', 'amount', 'type', 'category', 'date',
                    'budget_id'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for transaction in self.transactions:
                    writer.writerow({
                        'description': transaction.description,
                        'amount': transaction.amount,
                        'type': transaction.type,
                        'category': transaction.category,
                        'date': transaction.date,
                        'budget_id': transaction.budget_id
                    })
            
            return True, f"Transacciones exportadas a {filename}"
        except Exception as e:
            return False, f"Error al exportar transacciones: {str(e)}"
    
    def get_budget_timeline(self, budget_id: str):
        """Obtiene la línea de tiempo de transacciones de un presupuesto."""
        budget = self.get_budget(budget_id)
        if not budget:
            return None
        
        # Filtrar transacciones del presupuesto
        budget_transactions = [t for t in self.transactions if t.budget_id == budget_id]
        
        # Ordenar por fecha
        budget_transactions.sort(key=lambda x: x.date)
        
        timeline = [
            {
                "event": "Presupuesto creado",
                "date": budget.created_at,
                "amount": budget.amount,
                "type": "creation"
            }
        ]
        
        # Añadir transacciones
        for transaction in budget_transactions:
            timeline.append({
                "event": transaction.description,
                "date": transaction.date,
                "amount": transaction.amount,
                "type": transaction.type
            })
        
        # Añadir eventos de actualización
        if budget.updated_at != budget.created_at:
            timeline.append({
                "event": "Presupuesto actualizado",
                "date": budget.updated_at,
                "amount": 0,
                "type": "update"
            })
        
        # Añadir evento de finalización si está completado
        if budget.status == "completed":
            timeline.append({
                "event": "Presupuesto completado",
                "date": budget.updated_at,
                "amount": 0,
                "type": "completion"
            })
        
        return timeline
