"""Person model and related operations."""
from typing import Dict, List, Optional

class Person:
    """Represents a person in the genealogy tree."""
    
    def __init__(self, db):
        self.db = db
    
    def add(self, names: str, last_names: str, gender: str, 
           birth_date: Optional[str] = None, birth_place: Optional[str] = None) -> int:
        """Add a new person to the database."""
        query = """
        INSERT INTO Personas (Nombres, Apellidos, Genero, Fecha_Nacimiento, Lugar_Nacimiento, Visibilidad)
        VALUES (%s, %s, %s, %s, %s, 'publico')
        """
        params = (names, last_names, gender.upper(), birth_date, birth_place)
        
        if self.db.execute_query(query, params, fetch=False):
            return self.db.cursor.lastrowid
        return None
    
    def search(self, search_term: str, limit: int = 20) -> List[Dict]:
        """Search for people by name."""
        query = """
        SELECT ID_Persona, Nombres, Apellidos, 
               Fecha_Nacimiento, Lugar_Nacimiento
        FROM Personas
        WHERE CONCAT(Nombres, ' ', Apellidos) LIKE %s
        LIMIT %s
        """
        return self.db.execute_query(query, (f'%{search_term}%', limit))
    
    def get_by_id(self, person_id: int) -> Optional[Dict]:
        """Get a person by ID."""
        query = """
        SELECT * FROM Personas 
        WHERE ID_Persona = %s
        """
        result = self.db.execute_query(query, (person_id,))
        return result[0] if result else None
    
    def get_family_members(self, person_id: int, relationship_type: str = None) -> List[Dict]:
        """Get family members of a person, optionally filtered by relationship type."""
        query = """
        SELECT p.ID_Persona, p.Nombres, p.Apellidos, rf.Tipo_Relacion
        FROM Personas p
        JOIN Relaciones_Familiares rf ON p.ID_Persona = rf.ID_Persona1
        WHERE rf.ID_Persona2 = %s
        """
        
        if relationship_type:
            query += " AND rf.Tipo_Relacion = %s"
            return self.db.execute_query(query, (person_id, relationship_type))
        
        return self.db.execute_query(query, (person_id,))
    
    def get_children(self, person_id: int) -> List[Dict]:
        """Get all children of a person."""
        return self.get_family_members(person_id, 'hijo')
    
    def get_parents(self, person_id: int) -> List[Dict]:
        """Get all parents of a person."""
        query = """
        SELECT p.ID_Persona, p.Nombres, p.Apellidos, 
               rf.Tipo_Relacion as Relacion
        FROM Personas p
        JOIN Relaciones_Familiares rf ON p.ID_Persona = rf.ID_Persona1
        WHERE rf.ID_Persona2 = %s 
        AND rf.Tipo_Relacion IN ('padre', 'madre')
        """
        return self.db.execute_query(query, (person_id,))
    
    def get_spouses(self, person_id: int) -> List[Dict]:
        """Get all spouses of a person."""
        query = """
        SELECT p.ID_Persona, p.Nombres, p.Apellidos, 
               CASE 
                   WHEN rf.Tipo_Relacion = 'esposo' THEN 'spouse'
                   WHEN rf.Tipo_Relacion = 'esposa' THEN 'spouse'
               END as Relacion
        FROM Personas p
        JOIN Relaciones_Familiares rf ON p.ID_Persona = rf.ID_Persona1
        WHERE rf.ID_Persona2 = %s 
        AND rf.Tipo_Relacion IN ('esposo', 'esposa')
        """
        return self.db.execute_query(query, (person_id,))
