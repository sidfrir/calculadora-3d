import re

class DataValidator:
    @staticmethod
    def validate_piece_name(name):
        """Valida el nombre de la pieza."""
        if not name or not isinstance(name, str):
            return False, "El nombre de la pieza es requerido"
        
        if len(name.strip()) < 1:
            return False, "El nombre de la pieza no puede estar vacío"
        
        if len(name) > 100:
            return False, "El nombre de la pieza es demasiado largo (máximo 100 caracteres)"
        
        return True, "Nombre válido"
    
    @staticmethod
    def validate_print_time(hours):
        """Valida el tiempo de impresión en horas."""
        try:
            hours_float = float(hours)
            if hours_float <= 0:
                return False, "El tiempo de impresión debe ser mayor a cero"
            
            if hours_float > 1000:  # 1000 horas parece un límite razonable
                return False, "El tiempo de impresión es demasiado largo (máximo 1000 horas)"
            
            return True, "Tiempo válido"
        except (ValueError, TypeError):
            return False, "El tiempo de impresión debe ser un número válido"
    
    @staticmethod
    def validate_filament_used(grams):
        """Valida la cantidad de filamento usado en gramos."""
        try:
            grams_float = float(grams)
            if grams_float <= 0:
                return False, "La cantidad de filamento debe ser mayor a cero"
            
            if grams_float > 10000:  # 10kg parece un límite razonable
                return False, "La cantidad de filamento es demasiado grande (máximo 10000g)"
            
            return True, "Cantidad válida"
        except (ValueError, TypeError):
            return False, "La cantidad de filamento debe ser un número válido"
    
    @staticmethod
    def validate_cost(cost):
        """Valida los costos monetarios."""
        try:
            cost_float = float(cost)
            if cost_float < 0:
                return False, "El costo no puede ser negativo"
            
            if cost_float > 1000000:  # $1,000,000 parece un límite razonable
                return False, "El costo es demasiado alto (máximo $1,000,000)"
            
            return True, "Costo válido"
        except (ValueError, TypeError):
            return False, "El costo debe ser un número válido"
    
    @staticmethod
    def validate_profit_margin(margin):
        """Valida el margen de ganancia en porcentaje."""
        try:
            margin_float = float(margin)
            if margin_float < 0:
                return False, "El margen de ganancia no puede ser negativo"
            
            if margin_float > 1000:  # 1000% parece un límite razonable
                return False, "El margen de ganancia es demasiado alto (máximo 1000%)"
            
            return True, "Margen válido"
        except (ValueError, TypeError):
            return False, "El margen de ganancia debe ser un número válido"
    
    @staticmethod
    def validate_settings(settings):
        """Valida la configuración completa."""
        errors = []
        
        # Validar costo de máquina
        is_valid, message = DataValidator.validate_cost(settings.get('machine_cost_per_hour', 0))
        if not is_valid:
            errors.append(f"Costo máquina: {message}")
        
        # Validar costo de electricidad
        is_valid, message = DataValidator.validate_cost(settings.get('electricity_kwh_price', 0))
        if not is_valid:
            errors.append(f"Costo electricidad: {message}")
        
        # Validar consumo de impresora
        try:
            power = float(settings.get('printer_power_watts', 0))
            if power <= 0:
                errors.append("El consumo de la impresora debe ser mayor a cero")
            elif power > 10000:  # 10kW parece un límite razonable
                errors.append("El consumo de la impresora es demasiado alto (máximo 10000W)")
        except (ValueError, TypeError):
            errors.append("El consumo de la impresora debe ser un número válido")
        
        # Validar precios de filamentos
        filaments = settings.get('filaments', {})
        for name, filament in filaments.items():
            is_valid, message = DataValidator.validate_cost(filament.get('price_per_kg', 0))
            if not is_valid:
                errors.append(f"Filamento {name}: {message}")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, "Configuración válida"
    
    @staticmethod
    def validate_quote(quote_data):
        """Valida todos los datos de una cotización."""
        errors = []
        
        # Validar nombre de pieza
        is_valid, message = DataValidator.validate_piece_name(quote_data.get('piece_name', ''))
        if not is_valid:
            errors.append(message)
        
        # Validar tiempo de impresión
        is_valid, message = DataValidator.validate_print_time(quote_data.get('print_time', 0))
        if not is_valid:
            errors.append(message)
        
        # Validar filamento usado
        is_valid, message = DataValidator.validate_filament_used(quote_data.get('filament_used', 0))
        if not is_valid:
            errors.append(message)
        
        # Validar costos
        cost_fields = ['material_cost', 'labor_cost', 'total_cost', 'final_price']
        for field in cost_fields:
            is_valid, message = DataValidator.validate_cost(quote_data.get(field, 0))
            if not is_valid:
                errors.append(f"{field}: {message}")
        
        # Validar margen de ganancia
        is_valid, message = DataValidator.validate_profit_margin(quote_data.get('profit_margin', 0))
        if not is_valid:
            errors.append(message)
        
        if errors:
            return False, "; ".join(errors)
        
        return True, "Cotización válida"
    
    @staticmethod
    def sanitize_input(text):
        """Limpia y sanitiza el texto de entrada."""
        if not isinstance(text, str):
            return str(text)
        
        # Eliminar caracteres no deseados pero mantener texto legible
        # Permitir letras, números, espacios y algunos caracteres especiales comunes
        sanitized = re.sub(r'[^\w\s\-\._áéíóúÁÉÍÓÚüÜñÑ]', '', text, flags=re.UNICODE)
        return sanitized.strip()
    
    @staticmethod
    def format_currency(value):
        """Formatea un valor como moneda."""
        try:
            return f"${float(value):.2f}"
        except (ValueError, TypeError):
            return "$0.00"
    
    @staticmethod
    def format_time(hours):
        """Formatea horas como tiempo legible."""
        try:
            hours_float = float(hours)
            hours_int = int(hours_float)
            minutes = int((hours_float - hours_int) * 60)
            
            if hours_int > 0 and minutes > 0:
                return f"{hours_int}h {minutes}m"
            elif hours_int > 0:
                return f"{hours_int}h"
            else:
                return f"{minutes}m"
        except (ValueError, TypeError):
            return "0m"
