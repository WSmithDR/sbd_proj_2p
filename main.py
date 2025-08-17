#!/usr/bin/env python3
"""
Genealogy Application - Main Module

A command-line interface for managing family trees.
"""
import sys
import os
from colorama import init, Fore, Style

# Añadir el directorio actual al path para que Python encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from models.database import DatabaseConnection
from models.person import Person
from models.relationship import Relationship
from utils.views import PersonView, RelationshipView, ReportView

# Initialize colorama
init(autoreset=True)

class GenealogyApp:
    """Main application class for the genealogy system."""
    
    def __init__(self):
        """Initialize the application with database connection and models."""
        try:
            self.db = DatabaseConnection()
            self.person_model = Person(self.db)
            self.relationship_model = Relationship(self.db)
            self.person_view = PersonView()
            self.relationship_view = RelationshipView()
            self.report_view = ReportView()
        except Exception as e:
            print(f"{Fore.RED}Error initializing application: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the main application loop."""
        while True:
            self._display_main_menu()
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self._add_person()
            elif choice == '2':
                self._add_relationship()
            elif choice == '3':
                self._search_people()
            elif choice == '4':
                self._view_family_tree()
            elif choice == '5':
                self._view_relationships_report()
            elif choice == '6':
                self._view_people_by_location()
            elif choice == '0':
                print(f"{Fore.GREEN}¡Hasta luego!")
                break
            else:
                print(f"{Fore.RED}Opción no válida. Por favor, intente de nuevo.")
    
    def _display_main_menu(self):
        """Display the main menu."""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{'SISTEMA DE GENEALOGÍA':^50}")
        print(f"{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Agregar persona")
        print("2. Agregar relación familiar")
        print("3. Buscar personas")
        print("4. Ver árbol familiar")
        print("5. Ver reporte de relaciones")
        print("6. Ver personas por ubicación")
        print(f"{Fore.RED}0. Salir{Style.RESET_ALL}")
    
    def _add_person(self):
        """Handle adding a new person."""
        print(f"\n{Fore.CYAN}=== Agregar Nueva Persona ==={Style.RESET_ALL}")
        
        # Get person details
        names = input("Nombres: ").strip()
        last_names = input("Apellidos: ").strip()
        
        while True:
            gender = input("Género (M/F/O): ").strip().upper()
            if gender in ['M', 'F', 'O']:
                break
            print(f"{Fore.RED}Por favor ingrese M, F u O para otro.{Style.RESET_ALL}")
        
        birth_date = input("Fecha de nacimiento (YYYY-MM-DD, opcional): ").strip() or None
        birth_place = input("Lugar de nacimiento (opcional): ").strip() or None
        
        # Add person to database
        person_id = self.person_model.add(names, last_names, gender, birth_date, birth_place)
        
        if person_id:
            print(f"\n{Fore.GREEN}✓ Persona agregada exitosamente con ID: {person_id}")
            
            # Show the added person
            person = self.person_model.get_by_id(person_id)
            if person:
                self.person_view.display_person(person)
    
    def _add_relationship(self):
        """Handle adding a new relationship."""
        print(f"\n{Fore.CYAN}=== Agregar Relación Familiar ==={Style.RESET_ALL}")
        
        # Get person IDs
        person1_id = input("ID de la primera persona: ").strip()
        person2_id = input("ID de la segunda persona: ").strip()
        
        # Validate person IDs
        try:
            person1_id = int(person1_id)
            person2_id = int(person2_id)
        except ValueError:
            print(f"{Fore.RED}Error: Los IDs deben ser números.{Style.RESET_ALL}")
            return
        
        # Get relationship type
        print("\nTipos de relación:")
        print("1. Padre/Madre - Hijo(a)")
        print("2. Esposos")
        print("3. Hermanos")
        rel_choice = input("Seleccione el tipo de relación (1-3): ").strip()
        
        if rel_choice == '1':
            # Parent-Child relationship
            print("\n¿Quién es el padre/madre?")
            print(f"1. Persona {person1_id}")
            print(f"2. Persona {person2_id}")
            parent_choice = input("Seleccione (1-2): ").strip()
            
            if parent_choice == '1':
                parent_id, child_id = person1_id, person2_id
            elif parent_choice == '2':
                parent_id, child_id = person2_id, person1_id
            else:
                print(f"{Fore.RED}Opción no válida.{Style.RESET_ALL}")
                return
            
            # Get parent's gender for relationship type
            parent = self.person_model.get_by_id(parent_id)
            if not parent:
                print(f"{Fore.RED}No se encontró a la persona con ID {parent_id}.{Style.RESET_ALL}")
                return
                
            rel_type = 'padre' if parent.get('Genero') == 'M' else 'madre'
            
            # Add the relationship
            if self.relationship_model.add_relationship(parent_id, child_id, rel_type):
                print(f"{Fore.GREEN}✓ Relación agregada exitosamente!{Style.RESET_ALL}")
        
        elif rel_choice in ['2', '3']:
            # Spouse or sibling relationship
            rel_type = 'esposo' if rel_choice == '2' else 'hermano'
            
            if self.relationship_model.add_relationship(person1_id, person2_id, rel_type):
                print(f"{Fore.GREEN}✓ Relación agregada exitosamente!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Opción no válida.{Style.RESET_ALL}")
    
    def _search_people(self):
        """Handle searching for people."""
        print(f"\n{Fore.CYAN}=== Buscar Personas ==={Style.RESET_ALL}")
        
        search_term = input("Ingrese nombre o apellido a buscar: ").strip()
        
        if not search_term:
            print(f"{Fore.YELLOW}Por favor ingrese un término de búsqueda.{Style.RESET_ALL}")
            return
        
        results = self.person_model.search(search_term)
        self.person_view.display_people_list(results, "Resultados de Búsqueda")
    
    def _view_family_tree(self):
        """Display a person's family tree."""
        print(f"\n{Fore.CYAN}=== Árbol Familiar ==={Style.RESET_ALL}")
        
        person_id = input("Ingrese el ID de la persona: ").strip()
        
        try:
            person_id = int(person_id)
        except ValueError:
            print(f"{Fore.RED}Error: El ID debe ser un número.{Style.RESET_ALL}")
            return
        
        # Get person details
        person = self.person_model.get_by_id(person_id)
        if not person:
            print(f"{Fore.RED}No se encontró a la persona con ID {person_id}.{Style.RESET_ALL}")
            return
        
        # Get family relationships
        parents = self.person_model.get_parents(person_id)
        spouses = self.person_model.get_spouses(person_id)
        children = self.person_model.get_children(person_id)
        
        # Display the family tree
        self.relationship_view.display_family_tree(
            person,
            {
                'padres': parents,
                'esposos': spouses,
                'hijos': children
            }
        )
    
    def _view_relationships_report(self):
        """Display relationships report."""
        print(f"\n{Fore.CYAN}=== Reporte de Relaciones ==={Style.RESET_ALL}")
        
        limit = input("Número máximo de relaciones a mostrar (deje en blanco para 50): ").strip()
        limit = int(limit) if limit.isdigit() else 50
        
        relationships = self.relationship_model.get_relationships_report(limit)
        self.relationship_view.display_relationships(relationships)
    
    def _view_people_by_location(self):
        """Display people grouped by location."""
        print(f"\n{Fore.CYAN}=== Personas por Ubicación ==={Style.RESET_ALL}")
        
        location_data = self.relationship_model.get_people_by_location()
        self.report_view.display_location_report(location_data)

def main():
    """Main entry point for the application."""
    try:
        app = GenealogyApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operación cancelada por el usuario.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Ocurrió un error: {e}{Style.RESET_ALL}")
    finally:
        if 'app' in locals():
            app.db.close()

if __name__ == "__main__":
    main()
