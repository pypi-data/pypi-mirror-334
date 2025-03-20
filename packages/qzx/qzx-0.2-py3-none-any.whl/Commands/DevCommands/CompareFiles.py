#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Comando CompareFiles - Compara el contenido de dos archivos
"""

import os
import difflib
from Core.command_base import CommandBase

class CompareFilesCommand(CommandBase):
    """
    Comando para comparar dos archivos y mostrar sus diferencias
    """
    
    name = "compareFiles"
    description = "Compara dos archivos y muestra sus diferencias, útil para IDE"
    category = "dev"
    
    parameters = [
        {
            'name': 'file1',
            'description': 'Ruta al primer archivo',
            'required': True
        },
        {
            'name': 'file2',
            'description': 'Ruta al segundo archivo',
            'required': True
        },
        {
            'name': 'mode',
            'description': 'Modo de comparación: "full" (completo), "summary" (resumen) o "percent" (porcentaje)',
            'required': False,
            'default': 'full'
        }
    ]
    
    examples = [
        {
            'command': 'qzx compareFiles "archivo1.py" "archivo2.py"',
            'description': 'Comparar dos archivos Python y mostrar todas las diferencias'
        },
        {
            'command': 'qzx compareFiles "archivo1.txt" "archivo2.txt" "summary"',
            'description': 'Mostrar un resumen de diferencias entre dos archivos de texto'
        },
        {
            'command': 'qzx compareFiles "versión1.js" "versión2.js" "percent"',
            'description': 'Mostrar el porcentaje de similitud entre dos archivos JavaScript'
        }
    ]
    
    def execute(self, file1, file2, mode='full'):
        """
        Compara dos archivos y muestra sus diferencias
        
        Args:
            file1: Ruta al primer archivo
            file2: Ruta al segundo archivo
            mode: Modo de comparación (full, summary, percent)
            
        Returns:
            Resultado de la comparación en el formato especificado
        """
        # Verificar que los archivos existen
        if not os.path.exists(file1):
            return f"Error: El archivo '{file1}' no existe"
        if not os.path.exists(file2):
            return f"Error: El archivo '{file2}' no existe"
        
        # Verificar que son archivos (no directorios)
        if not os.path.isfile(file1):
            return f"Error: '{file1}' no es un archivo"
        if not os.path.isfile(file2):
            return f"Error: '{file2}' no es un archivo"
        
        try:
            # Leer el contenido de los archivos
            with open(file1, 'r', encoding='utf-8', errors='replace') as f:
                content1 = f.readlines()
            
            with open(file2, 'r', encoding='utf-8', errors='replace') as f:
                content2 = f.readlines()
            
            # Determinar qué tipo de comparación hacer basado en el modo
            if mode.lower() == 'full':
                return self._compare_full(file1, file2, content1, content2)
            elif mode.lower() == 'summary':
                return self._compare_summary(file1, file2, content1, content2)
            elif mode.lower() == 'percent':
                return self._compare_percent(file1, file2, content1, content2)
            else:
                return f"Error: Modo de comparación '{mode}' no válido. Use 'full', 'summary' o 'percent'."
            
        except Exception as e:
            return f"Error comparando archivos: {str(e)}"
    
    def _compare_full(self, file1, file2, content1, content2):
        """
        Realiza una comparación completa línea por línea
        """
        diff = difflib.unified_diff(
            content1, content2,
            fromfile=file1, tofile=file2,
            lineterm=''
        )
        
        diff_text = list(diff)
        
        if not diff_text:
            return f"Los archivos '{file1}' y '{file2}' son idénticos."
        
        result = [f"Diferencias entre '{file1}' y '{file2}':"]
        result.extend(diff_text)
        
        # Estadísticas
        result.append("\nEstadísticas:")
        added, removed = 0, 0
        for line in diff_text:
            if line.startswith('+') and not line.startswith('+++'):
                added += 1
            elif line.startswith('-') and not line.startswith('---'):
                removed += 1
        
        result.append(f"- Líneas añadidas: {added}")
        result.append(f"- Líneas eliminadas: {removed}")
        result.append(f"- Cambios totales: {added + removed}")
        
        return "\n".join(result)
    
    def _compare_summary(self, file1, file2, content1, content2):
        """
        Realiza una comparación resumida mostrando solo la cantidad de diferencias
        """
        matcher = difflib.SequenceMatcher(None, content1, content2)
        
        # Obtener los bloques que coinciden
        blocks = matcher.get_matching_blocks()
        
        # Calcular estadísticas
        similarity = matcher.ratio() * 100
        total_lines1 = len(content1)
        total_lines2 = len(content2)
        
        # Contar líneas idénticas
        identical_lines = sum(block.size for block in blocks if block.size > 0)
        
        # Contar cambios
        changes = max(total_lines1, total_lines2) - identical_lines
        
        result = [
            f"Resumen de comparación entre '{file1}' y '{file2}':",
            f"- Similitud: {similarity:.2f}%",
            f"- Líneas en archivo 1: {total_lines1}",
            f"- Líneas en archivo 2: {total_lines2}",
            f"- Líneas idénticas: {identical_lines}",
            f"- Cambios detectados: {changes}",
        ]
        
        # Mostrar los primeros 3 cambios como ejemplo
        diff = difflib.unified_diff(
            content1, content2,
            fromfile=file1, tofile=file2,
            lineterm=''
        )
        
        diff_text = list(diff)
        if diff_text:
            result.append("\nPrimeros cambios (muestra):")
            change_count = 0
            for line in diff_text:
                if line.startswith('+') and not line.startswith('+++') or line.startswith('-') and not line.startswith('---'):
                    result.append(f"  {line}")
                    change_count += 1
                    if change_count >= 6:  # Mostrar 3 pares de líneas modificadas
                        result.append("  ...")
                        break
        
        return "\n".join(result)
    
    def _compare_percent(self, file1, file2, content1, content2):
        """
        Calcula y muestra el porcentaje de similitud entre los archivos
        """
        # Comparar como líneas
        matcher_lines = difflib.SequenceMatcher(None, content1, content2)
        similarity_lines = matcher_lines.ratio() * 100
        
        # Comparar como texto completo
        text1 = ''.join(content1)
        text2 = ''.join(content2)
        matcher_text = difflib.SequenceMatcher(None, text1, text2)
        similarity_text = matcher_text.ratio() * 100
        
        # Tamaños de archivos
        size1 = os.path.getsize(file1)
        size2 = os.path.getsize(file2)
        size_diff = abs(size1 - size2)
        size_percent = 100 - (size_diff / max(size1, size2) * 100) if max(size1, size2) > 0 else 100
        
        result = [
            f"Porcentaje de similitud entre '{file1}' y '{file2}':",
            f"- Similitud de contenido: {similarity_text:.2f}%",
            f"- Similitud por líneas: {similarity_lines:.2f}%",
            f"- Similitud de tamaño: {size_percent:.2f}%",
            f"  Archivo 1: {size1} bytes",
            f"  Archivo 2: {size2} bytes",
            f"  Diferencia: {size_diff} bytes",
        ]
        
        # Conclusión
        avg_similarity = (similarity_text + similarity_lines + size_percent) / 3
        result.append(f"\nSimilitud promedio: {avg_similarity:.2f}%")
        
        if avg_similarity > 95:
            result.append("Los archivos son prácticamente idénticos.")
        elif avg_similarity > 80:
            result.append("Los archivos son muy similares con pequeñas diferencias.")
        elif avg_similarity > 50:
            result.append("Los archivos tienen similitudes significativas pero también diferencias importantes.")
        elif avg_similarity > 20:
            result.append("Los archivos son mayormente distintos con algunas similitudes.")
        else:
            result.append("Los archivos son completamente diferentes.")
        
        return "\n".join(result) 