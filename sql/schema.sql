USE streamtrack;

CREATE TABLE IF NOT EXISTS genero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS plataforma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS contenido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    sinopsis TEXT,
    anio_estreno INT NOT NULL,
    tipo ENUM('PELICULA', 'SERIE') NOT NULL,
    id_genero INT NOT NULL,
    id_plataforma INT NOT NULL,
    estado ENUM('PENDIENTE', 'VIENDO', 'VISTO', 'ABANDONADO') NOT NULL DEFAULT 'PENDIENTE',
    puntuacion INT DEFAULT 0,
    fecha_registro DATE NOT NULL,
    CONSTRAINT fk_contenido_genero FOREIGN KEY (id_genero) REFERENCES genero(id),
    CONSTRAINT fk_contenido_plataforma FOREIGN KEY (id_plataforma) REFERENCES plataforma(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pelicula (
    id_contenido INT PRIMARY KEY,
    duracion_minutos INT NOT NULL,
    CONSTRAINT fk_pelicula_contenido FOREIGN KEY (id_contenido) 
        REFERENCES contenido(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS serie (
    id_contenido INT PRIMARY KEY,
    total_temporadas INT NOT NULL DEFAULT 1,
    capitulos_totales INT NOT NULL,
    capitulos_vistos INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_serie_contenido FOREIGN KEY (id_contenido) 
        REFERENCES contenido(id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT IGNORE INTO genero (nombre) VALUES 
('Acción'), ('Comedia'), ('Drama'), ('Ciencia Ficción'), ('Terror'), ('Documental'), ('Animación');

INSERT IGNORE INTO plataforma (nombre) VALUES 
('Netflix'), ('Max'), ('Prime Video'), ('Disney+'), ('Apple TV+'), ('Paramount+');
