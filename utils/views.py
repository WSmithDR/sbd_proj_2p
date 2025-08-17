"""Command-line interface views and display utilities."""
from typing import List, Dict, Any, Optional
from colorama import Fore, Style
from tabulate import tabulate

class PersonView:
    """Handles display of person-related information."""
    
    @staticmethod
    def display_person(person: Dict[str, Any]) -> None:
        """Display a single person's details."""
        if not person:
            print(f"{Fore.RED}No se encontró la persona.{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}=== Información de la Persona ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}ID:{Style.RESET_ALL} {person.get('ID_Persona', 'N/A')}")
        print(f"{Fore.YELLOW}Nombre:{Style.RESET_ALL} {person.get('Nombres', '')} {person.get('Apellidos', '')}")
        
        if 'Genero' in person:
            gender_map = {'M': 'Masculino', 'F': 'Femenino', 'O': 'Otro'}
            print(f"{Fore.YELLOW}Género:{Style.RESET_ALL} {gender_map.get(person['Genero'], person['Genero'])}")
        
        if 'Fecha_Nacimiento' in person and person['Fecha_Nacimiento']:
            print(f"{Fore.YELLOW}Fecha de Nacimiento:{Style.RESET_ALL} {person['Fecha_Nacimiento']}")
        
        if 'Lugar_Nacimiento' in person and person['Lugar_Nacimiento']:
            print(f"{Fore.YELLOW}Lugar de Nacimiento:{Style.RESET_ALL} {person['Lugar_Nacimiento']}")
    
    @staticmethod
    def display_people_list(people: List[Dict[str, Any]], title: str = "Personas") -> None:
        """Display a list of people in a table format."""
        if not people:
            print(f"{Fore.YELLOW}No se encontraron personas.{Style.RESET_ALL}")
            return
            
        headers = ["ID", "Nombre", "Apellido", "Nacimiento", "Lugar"]
        rows = [
            [
                p.get('ID_Persona', ''),
                p.get('Nombres', ''),
                p.get('Apellidos', ''),
                p.get('Fecha_Nacimiento', 'Desconocida'),
                p.get('Lugar_Nacimiento', 'Desconocido')
            ]
            for p in people
        ]
        
        print(f"\n{Fore.CYAN}=== {title} ==={Style.RESET_ALL}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

class RelationshipView:
    """Handles display of relationship information."""
    
    @staticmethod
    def display_relationships(relationships: List[Dict[str, Any]]) -> None:
        """Display a list of relationships."""
        if not relationships:
            print(f"{Fore.YELLOW}No se encontraron relaciones.{Style.RESET_ALL}")
            return
            
        # Mapeo de tipos de relación a español
        rel_map = {
            'padre': 'es padre de',
            'madre': 'es madre de',
            'hijo': 'es hijo de',
            'hija': 'es hija de',
            'esposo': 'está casado con',
            'esposa': 'está casada con',
            'hermano': 'es hermano de',
            'hermana': 'es hermana de'
        }
        
        print(f"\n{Fore.CYAN}=== Relaciones Familiares ==={Style.RESET_ALL}")
        
        for rel in relationships:
            rel_type = rel_map.get(rel['relacion'].lower(), rel['relacion'])
            print(f"{Fore.YELLOW}{rel['persona1']}{Style.RESET_ALL} {rel_type} {Fore.YELLOW}{rel['persona2']}{Style.RESET_ALL}")
    
    @staticmethod
    def display_family_tree(person: Dict[str, Any], relationships: Dict[str, List[Dict]]):
        """Display a simple family tree for a person."""
        if not person:
            print(f"{Fore.RED}No se encontró la persona.{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}=== Árbol Familiar de {person.get('Nombres', '')} {person.get('Apellidos', '')} ==={Style.RESET_ALL}")
        
        # Mostrar padres
        if 'padres' in relationships and relationships['padres']:
            print(f"\n{Fore.YELLOW}Padres:{Style.RESET_ALL}")
            for parent in relationships['padres']:
                rel = "Padre" if parent['Tipo_Relacion'] == 'padre' else "Madre"
                print(f"- {rel}: {parent['Nombres']} {parent['Apellidos']} (ID: {parent['ID_Persona']})")
        
        # Mostrar cónyuges
        if 'esposos' in relationships and relationships['esposos']:
            print(f"\n{Fore.YELLOW}Cónyuges:{Style.RESET_ALL}")
            for spouse in relationships['esposos']:
                print(f"- Cónyuge: {spouse['Nombres']} {spouse['Apellidos']} (ID: {spouse['ID_Persona']})")
        
        # Mostrar hijos
        if 'hijos' in relationships and relationships['hijos']:
            print(f"\n{Fore.YELLOW}Hijos:{Style.RESET_ALL}")
            for child in relationships['hijos']:
                gender = "hijo" if child.get('Genero') == 'M' else "hija"
                print(f"- {gender.capitalize()}: {child['Nombres']} {child['Apellidos']} (ID: {child['ID_Persona']})")

class ReportView:
    """Handles display of reports."""
    
    @staticmethod
    def display_location_report(data: List[Dict[str, Any]]) -> None:
        """Display a report of people by location."""
        if not data:
            print(f"{Fore.YELLOW}No hay datos de ubicación disponibles.{Style.RESET_ALL}")
            return
            
        headers = ["Ubicación", "Total Personas", "Fecha Más Antigua", "Fecha Más Reciente"]
        rows = [
            [
                d['ubicacion'],
                d['total_personas'],
                d.get('fecha_mas_antigua', 'Desconocida'),
                d.get('fecha_mas_reciente', 'Desconocida')
            ]
            for d in data
        ]
        
        print(f"\n{Fore.CYAN}=== Personas por Ubicación ==={Style.RESET_ALL}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
