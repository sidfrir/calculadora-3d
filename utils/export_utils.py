import csv
import json
import xml.etree.ElementTree as ET
from datetime import datetime

class ExportUtils:
    @staticmethod
    def export_to_csv(quotes, file_path):
        """Exporta las cotizaciones a un archivo CSV."""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'piece_name', 'print_time', 'filament_used', 
                            'material_cost', 'labor_cost', 'total_cost', 
                            'profit_margin', 'final_price', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for quote in quotes:
                    writer.writerow({
                        'id': quote.id,
                        'piece_name': quote.piece_name,
                        'print_time': quote.print_time,
                        'filament_used': quote.filament_used,
                        'material_cost': quote.material_cost,
                        'labor_cost': quote.labor_cost,
                        'total_cost': quote.total_cost,
                        'profit_margin': quote.profit_margin,
                        'final_price': quote.final_price,
                        'created_at': quote.created_at
                    })
            return True
        except Exception as e:
            print(f"Error al exportar a CSV: {e}")
            return False
    
    @staticmethod
    def export_to_json(quotes, file_path):
        """Exporta las cotizaciones a un archivo JSON."""
        try:
            quotes_data = []
            for quote in quotes:
                quotes_data.append({
                    'id': quote.id,
                    'piece_name': quote.piece_name,
                    'print_time': quote.print_time,
                    'filament_used': quote.filament_used,
                    'material_cost': quote.material_cost,
                    'labor_cost': quote.labor_cost,
                    'total_cost': quote.total_cost,
                    'profit_margin': quote.profit_margin,
                    'final_price': quote.final_price,
                    'created_at': quote.created_at
                })
            
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(quotes_data, jsonfile, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al exportar a JSON: {e}")
            return False
    
    @staticmethod
    def export_to_xml(quotes, file_path):
        """Exporta las cotizaciones a un archivo XML."""
        try:
            root = ET.Element("quotes")
            
            for quote in quotes:
                quote_elem = ET.SubElement(root, "quote")
                ET.SubElement(quote_elem, "id").text = str(quote.id)
                ET.SubElement(quote_elem, "piece_name").text = quote.piece_name
                ET.SubElement(quote_elem, "print_time").text = str(quote.print_time)
                ET.SubElement(quote_elem, "filament_used").text = str(quote.filament_used)
                ET.SubElement(quote_elem, "material_cost").text = str(quote.material_cost)
                ET.SubElement(quote_elem, "labor_cost").text = str(quote.labor_cost)
                ET.SubElement(quote_elem, "total_cost").text = str(quote.total_cost)
                ET.SubElement(quote_elem, "profit_margin").text = str(quote.profit_margin)
                ET.SubElement(quote_elem, "final_price").text = str(quote.final_price)
                ET.SubElement(quote_elem, "created_at").text = quote.created_at
            
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            return True
        except Exception as e:
            print(f"Error al exportar a XML: {e}")
            return False
    
    @staticmethod
    def export_to_txt(quotes, file_path):
        """Exporta las cotizaciones a un archivo de texto plano."""
        try:
            with open(file_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write("Historial de Cotizaciones\n")
                txtfile.write("=" * 50 + "\n\n")
                
                for quote in quotes:
                    txtfile.write(f"ID: {quote.id}\n")
                    txtfile.write(f"Nombre de la Pieza: {quote.piece_name}\n")
                    txtfile.write(f"Tiempo de Impresión: {quote.print_time} horas\n")
                    txtfile.write(f"Filamento Usado: {quote.filament_used} g\n")
                    txtfile.write(f"Costo del Material: ${quote.material_cost:.2f}\n")
                    txtfile.write(f"Costo de Mano de Obra: ${quote.labor_cost:.2f}\n")
                    txtfile.write(f"Costo Total: ${quote.total_cost:.2f}\n")
                    txtfile.write(f"Margen de Ganancia: {quote.profit_margin}%\n")
                    txtfile.write(f"Precio Final: ${quote.final_price:.2f}\n")
                    txtfile.write(f"Fecha: {quote.created_at}\n")
                    txtfile.write("-" * 30 + "\n\n")
            return True
        except Exception as e:
            print(f"Error al exportar a TXT: {e}")
            return False
    
    @staticmethod
    def export_to_html(quotes, file_path):
        """Exporta las cotizaciones a un archivo HTML."""
        try:
            with open(file_path, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write("""<!DOCTYPE html>
<html>
<head>
    <title>Historial de Cotizaciones</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Historial de Cotizaciones</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Nombre de la Pieza</th>
            <th>Tiempo de Impresión</th>
            <th>Filamento Usado (g)</th>
            <th>Costo del Material</th>
            <th>Costo de Mano de Obra</th>
            <th>Costo Total</th>
            <th>Margen de Ganancia (%)</th>
            <th>Precio Final</th>
            <th>Fecha</th>
        </tr>
""")
                
                for quote in quotes:
                    htmlfile.write(f"""        <tr>
            <td>{quote.id}</td>
            <td>{quote.piece_name}</td>
            <td>{quote.print_time}</td>
            <td>{quote.filament_used}</td>
            <td>${quote.material_cost:.2f}</td>
            <td>${quote.labor_cost:.2f}</td>
            <td>${quote.total_cost:.2f}</td>
            <td>{quote.profit_margin}%</td>
            <td>${quote.final_price:.2f}</td>
            <td>{quote.created_at}</td>
        </tr>
""")
                
                htmlfile.write("""    </table>
</body>
</html>""")
            return True
        except Exception as e:
            print(f"Error al exportar a HTML: {e}")
            return False
    
    @staticmethod
    def get_export_formats():
        """Devuelve los formatos de exportación disponibles."""
        return [
            {"name": "CSV", "extension": ".csv", "function": ExportUtils.export_to_csv},
            {"name": "JSON", "extension": ".json", "function": ExportUtils.export_to_json},
            {"name": "XML", "extension": ".xml", "function": ExportUtils.export_to_xml},
            {"name": "Texto Plano", "extension": ".txt", "function": ExportUtils.export_to_txt},
            {"name": "HTML", "extension": ".html", "function": ExportUtils.export_to_html}
        ]
