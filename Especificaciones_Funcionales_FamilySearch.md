# Requerimientos del Sistema: familysearch.org

## Introducción

En este proyecto, se diseñará e implementará un sistema de base de datos relacional para soportar las operaciones de **FamilySearch.org**, una plataforma en línea para la investigación de la historia familiar. Este documento detalla sus funcionalidades principales y los requerimientos para su funcionamiento.

## Especificación del Proyecto

El producto central de FamilySearch es la capacidad que ofrece al usuario de encontrar registros de sus antepasados y, a partir de ellos, colaborar en la construcción de un árbol genealógico mundial. Este proceso implica tareas como la indexación de documentos, donde se asocian los nombres encontrados en registros históricos con personas, permitiendo así armar de a poco y de forma colaborativa un gran árbol familiar compartido por todos. En el caso de Ecuador, gran parte de los registros históricos han sido provistos por la Iglesia Católica en Ecuador a través de sus diversas diócesis.

FamilySearch es una organización sin fines de lucro, lo que permite que todos sus recursos se ofrezcan de forma gratuita. Esta combinación de colaboración masiva y acceso libre fomenta que, a medida que más usuarios contribuyen, la base de datos se enriquezca y sea más útil para todos.

## 1. Tipos de Usuarios del Sistema

Los usuarios del sistema se clasifican en dos roles principales:

*   **Usuario Registrado (Investigador/Colaborador):** Cualquier persona que crea una cuenta para descubrir su historia familiar, construir el árbol y preservar recuerdos. Cualquier usuario registrado puede optar por participar en actividades de contribución (como la indexación de registros) para enriquecer la base de datos comunitaria.

## 2. Requerimientos Funcionales

Los datos requeridos para la base de datos genealógica se pueden clasificar en las siguientes categorías principales: **Personas (Individuos)**, **Familias**, **Registros Históricos**, **Fuentes**, **Recuerdos**, **Usuarios**, **Contribuciones/Cambios** y **Fusiones**.

*   **Personas (Individuos):** Almacena información sobre cada individuo (nombres, fechas y lugares de eventos vitales, etc.). Incluye un historial detallado de cambios y fusiones para rastrear la colaboración.
*   **Familias:** Define las relaciones entre individuos (padres, hijos, cónyuges), formando la estructura del árbol genealógico.
*   **Registros Históricos:** Son colecciones de documentos digitalizados como censos, certificados de nacimiento, actas de matrimonio y registros militares. El sistema alberga miles de millones de estos registros.
*   **Fuentes:** Vínculos que conectan la información de un individuo en el árbol genealógico con un registro histórico que la respalda, proporcionando evidencia para los datos.
*   **Recuerdos:** Archivos multimedia (fotos, historias escritas, documentos, grabaciones de audio) aportados por los usuarios y asociados a un antepasado para enriquecer la historia de su vida.
*   **Usuarios:** Información sobre las cuentas de usuario registradas en la plataforma. Al crear una cuenta, el sistema genera automáticamente una entidad "Persona" asociada. Por defecto, este nuevo perfil de persona y su árbol genealógico inicial tienen la visibilidad deshabilitada para otros usuarios en los resultados de búsqueda. El usuario tiene control total para habilitar estas funcionalidades de privacidad desde la configuración de su cuenta.
*   **Contribuciones y Cambios:** Un registro detallado de todas las modificaciones realizadas por un usuario en los perfiles de los individuos. Esto incluye qué campo se cambió, el valor anterior y el nuevo, la fecha y el usuario que hizo el cambio, permitiendo la trazabilidad y la resolución de conflictos.
*   **Fusiones:** Un registro de los eventos de fusión entre dos perfiles de personas, especificando el perfil que se mantiene, el que se descarta y el usuario que realizó la operación.

El sistema debe soportar un entorno colaborativo donde múltiples usuarios puedan contribuir a los mismos perfiles de individuos fallecidos, gestionar conflictos y fusionar entradas duplicadas para mejorar la precisión y completitud del árbol global.

## Tareas de los Usuarios

### **Funcionalidades de Nivel Usuario Registrado**

Los Usuarios Registrados realizan tanto la investigación de su historia familiar como actividades de voluntariado. Deben poder:

*   **Gestión del Árbol Familiar Colaborativo:**
    *   Crear, ver y expandir el árbol genealógico. El sistema puede autocompletar ramas familiares si encuentra coincidencias en el árbol comunitario.
    *   Añadir y editar información sobre personas, adjuntando fuentes para validar los datos.
    *   Resolver discrepancias de datos y fusionar perfiles duplicados. Esto incluye tanto la revisión de duplicados sugeridos por el sistema como la capacidad de iniciar una fusión manual entre dos perfiles que el usuario identifique como la misma persona.
    *   Imprimir gráficos del árbol (por ejemplo, gráficos de abanico) para compartir.
*   **Búsqueda y Acceso a Registros Históricos:**
    *   Buscar en miles de millones de registros históricos por nombre, lugar, colección, etc.
    *   Recibir "sugerencias de registros" automáticas que el sistema encuentra y asocia a personas del árbol.
    *   Anexar los registros históricos encontrados como fuentes a los perfiles de sus antepasados.
*   **Preservación de Recuerdos:**
    *   Subir, etiquetar y gestionar "recuerdos" (fotos, historias, documentos, audio) y asociarlos a antepasados.
*   **Colaboración y Aprendizaje:**
    *   Comunicarse con otros usuarios a través de un sistema de mensajería o chat para colaborar en la resolución de discrepancias.
*   **Actividades de Voluntariado (Indexación):**
    *   Participar en proyectos para transcribir (indexar) información de registros históricos digitalizados, haciéndolos más fáciles de buscar.
    *   Revisar las indexaciones de otros voluntarios para garantizar su precisión.