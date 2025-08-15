-- Creación de la base de datos para el árbol genealógico
CREATE DATABASE IF NOT EXISTS familysearch;
USE familysearch;

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Contrasena_Hash VARCHAR(255) NOT NULL,
    Fecha_Registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Ultimo_Acceso TIMESTAMP NULL,
    Visibilidad_Perfil ENUM('publico', 'privado') DEFAULT 'privado',
    Visibilidad_Arbol ENUM('publico', 'privado') DEFAULT 'privado',
    Biografia TEXT,
    Ubicacion VARCHAR(255)
);

-- Tabla de Personas (individuos en el árbol genealógico)
CREATE TABLE Personas (
    ID_Persona INT AUTO_INCREMENT PRIMARY KEY,
    Nombres VARCHAR(100) NOT NULL,
    Apellidos VARCHAR(100) NOT NULL,
    Genero ENUM('M', 'F', 'Otro') NULL,
    Fecha_Nacimiento DATE,
    Lugar_Nacimiento VARCHAR(255),
    Fecha_Bautismo DATE,
    Lugar_Bautismo VARCHAR(255),
    Fecha_Defuncion DATE,
    Lugar_Defuncion VARCHAR(255),
    Fecha_Entierro DATE,
    Lugar_Entierro VARCHAR(255),
    Biografia TEXT,
    Es_Usuario BOOLEAN DEFAULT FALSE,
    ID_Usuario INT NULL,
    Visibilidad ENUM('publico', 'privado') DEFAULT 'publico',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- Tabla de Relaciones Familiares
CREATE TABLE Relaciones_Familiares (
    ID_Relacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_Persona1 INT NOT NULL,
    ID_Persona2 INT NOT NULL,
    Tipo_Relacion ENUM('padre', 'madre', 'hijo', 'hija', 'esposo', 'esposa', 'hermano', 'hermana') NOT NULL,
    Fecha_Evento DATE,
    Lugar_Evento VARCHAR(255),
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ID_Usuario_Creacion INT,
    FOREIGN KEY (ID_Persona1) REFERENCES Personas(ID_Persona) ON DELETE CASCADE,
    FOREIGN KEY (ID_Persona2) REFERENCES Personas(ID_Persona) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario_Creacion) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- Tabla de Registros Históricos
CREATE TABLE Registros_Historicos (
    ID_Registro INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Tipo_Documento VARCHAR(100) NOT NULL,
    Fecha_Documento DATE,
    Lugar_Documento VARCHAR(255),
    Descripcion TEXT,
    URL_Digitalizacion TEXT,
    Coleccion VARCHAR(100),
    Fecha_Subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ID_Usuario_Subida INT,
    Estado_Revision ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
    FOREIGN KEY (ID_Usuario_Subida) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- Tabla de Fuentes (relación entre Personas y Registros Históricos)
CREATE TABLE Fuentes (
    ID_Fuente INT AUTO_INCREMENT PRIMARY KEY,
    ID_Persona INT NOT NULL,
    ID_Registro INT NOT NULL,
    Tipo_Informacion ENUM('nacimiento', 'bautismo', 'matrimonio', 'defuncion', 'censo', 'otro') NOT NULL,
    Detalle_Informacion TEXT,
    Pagina VARCHAR(50),
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ID_Usuario_Creacion INT,
    FOREIGN KEY (ID_Persona) REFERENCES Personas(ID_Persona) ON DELETE CASCADE,
    FOREIGN KEY (ID_Registro) REFERENCES Registros_Historicos(ID_Registro) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario_Creacion) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- Tabla de Recuerdos (fotos, documentos, audio, etc.)
CREATE TABLE Recuerdos (
    ID_Recuerdo INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Tipo_Archivo ENUM('foto', 'documento', 'audio', 'video', 'otro') NOT NULL,
    URL_Archivo TEXT NOT NULL,
    Fecha_Subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ID_Usuario_Subida INT NOT NULL,
    Visibilidad ENUM('publico', 'privado') DEFAULT 'publico',
    FOREIGN KEY (ID_Usuario_Subida) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE
);

-- Tabla de relación entre Personas y Recuerdos
CREATE TABLE Personas_Recuerdos (
    ID_Persona INT NOT NULL,
    ID_Recuerdo INT NOT NULL,
    Tipo_Relacion VARCHAR(100),
    Etiqueta VARCHAR(100),
    Fecha_Asociacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ID_Persona, ID_Recuerdo),
    FOREIGN KEY (ID_Persona) REFERENCES Personas(ID_Persona) ON DELETE CASCADE,
    FOREIGN KEY (ID_Recuerdo) REFERENCES Recuerdos(ID_Recuerdo) ON DELETE CASCADE
);

-- Tabla de Actividades de Indexación
CREATE TABLE Actividades_Indexacion (
    ID_Actividad INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Estado ENUM('activa', 'pausada', 'completada') DEFAULT 'activa',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Limite DATE,
    ID_Usuario_Creacion INT,
    FOREIGN KEY (ID_Usuario_Creacion) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- Tabla de Tareas de Indexación
CREATE TABLE Tareas_Indexacion (
    ID_Tarea INT AUTO_INCREMENT PRIMARY KEY,
    ID_Actividad INT NOT NULL,
    ID_Registro INT NOT NULL,
    ID_Usuario_Asignado INT,
    Estado ENUM('pendiente', 'en_progreso', 'completada', 'revisada') DEFAULT 'pendiente',
    Fecha_Asignacion TIMESTAMP NULL,
    Fecha_Completada TIMESTAMP NULL,
    Comentarios TEXT,
    FOREIGN KEY (ID_Actividad) REFERENCES Actividades_Indexacion(ID_Actividad) ON DELETE CASCADE,
    FOREIGN KEY (ID_Registro) REFERENCES Registros_Historicos(ID_Registro) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario_Asignado) REFERENCES Usuarios(ID_Usuario) ON DELETE SET NULL
);

-- Tabla de Mensajes entre Usuarios
CREATE TABLE Mensajes (
    ID_Mensaje INT AUTO_INCREMENT PRIMARY KEY,
    ID_Remitente INT NOT NULL,
    ID_Destinatario INT NOT NULL,
    Asunto VARCHAR(255),
    Contenido TEXT NOT NULL,
    Fecha_Envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Leido BOOLEAN DEFAULT FALSE,
    Fecha_Lectura TIMESTAMP NULL,
    FOREIGN KEY (ID_Remitente) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE,
    FOREIGN KEY (ID_Destinatario) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE
);

-- Tabla de Historial de Cambios
CREATE TABLE Historial_Cambios (
    ID_Cambio INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT NOT NULL,
    ID_Persona INT,
    ID_Registro INT,
    ID_Recuerdo INT,
    Tipo_Entidad ENUM('persona', 'registro', 'recuerdo', 'relacion') NOT NULL,
    Tipo_Cambio VARCHAR(100) NOT NULL,
    Detalle_Anterior TEXT,
    Detalle_Nuevo TEXT,
    Fecha_Cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE,
    FOREIGN KEY (ID_Persona) REFERENCES Personas(ID_Persona) ON DELETE SET NULL,
    FOREIGN KEY (ID_Registro) REFERENCES Registros_Historicos(ID_Registro) ON DELETE SET NULL,
    FOREIGN KEY (ID_Recuerdo) REFERENCES Recuerdos(ID_Recuerdo) ON DELETE SET NULL
);

-- Tabla de Fusiones de Perfiles
CREATE TABLE Fusiones (
    ID_Fusion INT AUTO_INCREMENT PRIMARY KEY,
    ID_Persona_Mantener INT NOT NULL,
    ID_Persona_Fusionar INT NOT NULL,
    ID_Usuario INT NOT NULL,
    Fecha_Fusion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Razon TEXT,
    FOREIGN KEY (ID_Persona_Mantener) REFERENCES Personas(ID_Persona) ON DELETE CASCADE,
    FOREIGN KEY (ID_Persona_Fusionar) REFERENCES Personas(ID_Persona) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE
);

-- Índices para mejorar el rendimiento de las consultas
-- Tabla de Amistades entre Usuarios
CREATE TABLE Amistades (
    ID_Amistad INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario1 INT NOT NULL,
    ID_Usuario2 INT NOT NULL,
    Fecha_Amistad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Estado ENUM('pendiente', 'aceptada', 'rechazada') DEFAULT 'pendiente',
    Fecha_Estado TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_amistad (LEAST(ID_Usuario1, ID_Usuario2), GREATEST(ID_Usuario1, ID_Usuario2)),
    FOREIGN KEY (ID_Usuario1) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE,
    FOREIGN KEY (ID_Usuario2) REFERENCES Usuarios(ID_Usuario) ON DELETE CASCADE,
    CHECK (ID_Usuario1 != ID_Usuario2)
);

-- Índices para mejorar el rendimiento de las consultas
CREATE INDEX idx_personas_nombre_apellido ON Personas(Nombres, Apellidos);
CREATE INDEX idx_personas_fechas ON Personas(Fecha_Nacimiento, Fecha_Defuncion);
CREATE INDEX idx_usuarios_email ON Usuarios(Email);
CREATE INDEX idx_registros_titulo ON Registros_Historicos(Titulo);
CREATE INDEX idx_registros_tipo_fecha ON Registros_Historicos(Tipo_Documento, Fecha_Documento);
CREATE INDEX idx_recuerdos_tipo_fecha ON Recuerdos(Tipo_Archivo, Fecha_Subida);
CREATE INDEX idx_amistades_estado ON Amistades(Estado, Fecha_Estado);
CREATE INDEX idx_amistades_usuarios ON Amistades(LEAST(ID_Usuario1, ID_Usuario2), GREATEST(ID_Usuario1, ID_Usuario2));