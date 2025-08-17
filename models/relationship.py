"""Relationship model and operations."""
from typing import Dict, List, Optional, Tuple

class Relationship:
    """Handles family relationships between people."""
    
    def __init__(self, db):
        self.db = db
    
    def add_relationship(self, person1_id: int, person2_id: int, 
                        relationship_type: str) -> bool:
        """Add a relationship between two people."""
        # Map relationship types to their reverse
        reverse_relationships = {
            'padre': 'hijo',
            'madre': 'hijo',
            'hijo': 'padre',  # Will be adjusted based on gender
            'esposo': 'esposa',
            'esposa': 'esposo',
            'hermano': 'hermano',
            'hermana': 'hermana'
        }
        
        # Get the reverse relationship
        reverse_rel = reverse_relationships.get(relationship_type)
        if not reverse_rel:
            print(f"✗ Invalid relationship type: {relationship_type}")
            return False
        
        # Special case for parent-child relationships
        if relationship_type in ['padre', 'madre']:
            return self._add_parent_child_relationship(
                person1_id, person2_id, relationship_type
            )
        
        # For bidirectional relationships (spouse, sibling)
        query = """
        INSERT INTO Relaciones_Familiares 
        (ID_Persona1, ID_Persona2, Tipo_Relacion)
        VALUES (%s, %s, %s), (%s, %s, %s)
        """
        params = (
            person1_id, person2_id, relationship_type,
            person2_id, person1_id, reverse_rel
        )
        
        return self.db.execute_query(query, params, fetch=False)
    
    def _add_parent_child_relationship(self, parent_id: int, child_id: int, 
                                     relationship_type: str) -> bool:
        """Helper method to add parent-child relationship."""
        query = """
        INSERT INTO Relaciones_Familiares 
        (ID_Persona1, ID_Persona2, Tipo_Relacion)
        VALUES (%s, %s, %s)
        """
        params = (parent_id, child_id, relationship_type)
        return self.db.execute_query(query, params, fetch=False)
    
    def get_relationships_report(self, limit: int = 50) -> List[Dict]:
        """Generate a report of all relationships."""
        query = """
        SELECT 
            p1.ID_Persona as id1,
            CONCAT(p1.Nombres, ' ', p1.Apellidos) as persona1,
            rf.Tipo_Relacion as relacion,
            p2.ID_Persona as id2,
            CONCAT(p2.Nombres, ' ', p2.Apellidos) as persona2
        FROM Relaciones_Familiares rf
        JOIN Personas p1 ON rf.ID_Persona1 = p1.ID_Persona
        JOIN Personas p2 ON rf.ID_Persona2 = p2.ID_Persona
        ORDER BY p1.Apellidos, p1.Nombres, rf.Tipo_Relacion
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    def get_people_by_location(self) -> List[Dict]:
        """Get people grouped by birth location."""
        query = """
        SELECT 
            COALESCE(Lugar_Nacimiento, 'Desconocido') as ubicacion,
            COUNT(*) as total_personas,
            MIN(Fecha_Nacimiento) as fecha_mas_antigua,
            MAX(Fecha_Nacimiento) as fecha_mas_reciente
        FROM Personas
        GROUP BY Lugar_Nacimiento
        HAVING COUNT(*) > 0
        ORDER BY COUNT(*) DESC, Lugar_Nacimiento
        """
        return self.db.execute_query(query)
