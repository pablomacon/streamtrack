import os
import subprocess

BASE_DIR = r"C:\Users\profe\streamtrack"

FILES = {}

FILES["pom.xml"] = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.streamtrack</groupId>
    <artifactId>streamtrack</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>StreamTrack</name>
    <description>Aplicacion de escritorio para seguimiento de peliculas y series</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <flatlaf.version>3.4.1</flatlaf.version>
        <mysql.version>8.3.0</mysql.version>
        <junit.version>5.10.2</junit.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <version>${mysql.version}</version>
        </dependency>

        <dependency>
            <groupId>com.formdev</groupId>
            <artifactId>flatlaf</artifactId>
            <version>${flatlaf.version}</version>
        </dependency>

        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.2.0</version>
                <configuration>
                    <mainClass>com.streamtrack.Main</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""

FILES["src/main/resources/db.properties"] = """db.url=jdbc:mysql://localhost:3306/streamtrack?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true
db.user=root
db.password=
"""

FILES["sql/schema.sql"] = """USE streamtrack;

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
"""

FILES["src/main/java/com/streamtrack/config/DatabaseConnection.java"] = """package com.streamtrack.config;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class DatabaseConnection {

    private static final String CONFIG_FILE = "db.properties";
    private static String url;
    private static String user;
    private static String password;

    static {
        loadConfiguration();
    }

    private DatabaseConnection() {
    }

    private static void loadConfiguration() {
        Properties props = new Properties();
        try (InputStream input = DatabaseConnection.class.getClassLoader().getResourceAsStream(CONFIG_FILE)) {
            if (input == null) {
                throw new RuntimeException("No se encontró el archivo de configuración: " + CONFIG_FILE);
            }
            props.load(input);
            url = props.getProperty("db.url");
            user = props.getProperty("db.user");
            password = props.getProperty("db.password", "");
        } catch (IOException e) {
            throw new RuntimeException("Error al cargar la configuración de la base de datos: " + e.getMessage(), e);
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
"""

FILES["src/main/java/com/streamtrack/model/enums/EstadoContenido.java"] = """package com.streamtrack.model.enums;

public enum EstadoContenido {
    PENDIENTE("Pendiente"),
    VIENDO("Viendo"),
    VISTO("Visto"),
    ABANDONADO("Abandonado");

    private final String etiqueta;

    EstadoContenido(String etiqueta) {
        this.etiqueta = etiqueta;
    }

    public String getEtiqueta() {
        return etiqueta;
    }

    @Override
    public String toString() {
        return etiqueta;
    }
}
"""

FILES["src/main/java/com/streamtrack/model/enums/TipoContenido.java"] = """package com.streamtrack.model.enums;

public enum TipoContenido {
    PELICULA("Película"),
    SERIE("Serie");

    private final String etiqueta;

    TipoContenido(String etiqueta) {
        this.etiqueta = etiqueta;
    }

    public String getEtiqueta() {
        return etiqueta;
    }

    @Override
    public String toString() {
        return etiqueta;
    }
}
"""

FILES["src/main/java/com/streamtrack/model/Genero.java"] = """package com.streamtrack.model;

import java.util.Objects;

public class Genero {

    private Integer id;
    private String nombre;

    public Genero() {
    }

    public Genero(Integer id, String nombre) {
        this.id = id;
        this.nombre = nombre;
    }

    public Genero(String nombre) {
        this(null, nombre);
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Genero genero = (Genero) o;
        return Objects.equals(id, genero.id) || Objects.equals(nombre, genero.nombre);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, nombre);
    }

    @Override
    public String toString() {
        return nombre != null ? nombre : "";
    }
}
"""

FILES["src/main/java/com/streamtrack/model/Plataforma.java"] = """package com.streamtrack.model;

import java.util.Objects;

public class Plataforma {

    private Integer id;
    private String nombre;

    public Plataforma() {
    }

    public Plataforma(Integer id, String nombre) {
        this.id = id;
        this.nombre = nombre;
    }

    public Plataforma(String nombre) {
        this(null, nombre);
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Plataforma that = (Plataforma) o;
        return Objects.equals(id, that.id) || Objects.equals(nombre, that.nombre);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, nombre);
    }

    @Override
    public String toString() {
        return nombre != null ? nombre : "";
    }
}
"""

FILES["src/main/java/com/streamtrack/model/Contenido.java"] = """package com.streamtrack.model;

import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.time.LocalDate;
import java.util.Objects;

public abstract class Contenido {

    private Integer id;
    private String titulo;
    private String sinopsis;
    private int anioEstreno;
    private Genero genero;
    private Plataforma plataforma;
    private EstadoContenido estado;
    private int puntuacion;
    private LocalDate fechaRegistro;

    public Contenido() {
        this.estado = EstadoContenido.PENDIENTE;
        this.puntuacion = 0;
        this.fechaRegistro = LocalDate.now();
    }

    public Contenido(Integer id, String titulo, String sinopsis, int anioEstreno,
                     Genero genero, Plataforma plataforma, EstadoContenido estado,
                     int puntuacion, LocalDate fechaRegistro) {
        this.id = id;
        this.titulo = titulo;
        this.sinopsis = sinopsis;
        this.anioEstreno = anioEstreno;
        this.genero = genero;
        this.plataforma = plataforma;
        this.estado = (estado != null) ? estado : EstadoContenido.PENDIENTE;
        this.puntuacion = puntuacion;
        this.fechaRegistro = (fechaRegistro != null) ? fechaRegistro : LocalDate.now();
    }

    public abstract TipoContenido getTipo();
    public abstract String getProgresoVisual();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public String getSinopsis() {
        return sinopsis;
    }

    public void setSinopsis(String sinopsis) {
        this.sinopsis = sinopsis;
    }

    public int getAnioEstreno() {
        return anioEstreno;
    }

    public void setAnioEstreno(int anioEstreno) {
        this.anioEstreno = anioEstreno;
    }

    public Genero getGenero() {
        return genero;
    }

    public void setGenero(Genero genero) {
        this.genero = genero;
    }

    public Plataforma getPlataforma() {
        return plataforma;
    }

    public void setPlataforma(Plataforma plataforma) {
        this.plataforma = plataforma;
    }

    public EstadoContenido getEstado() {
        return estado;
    }

    public void setEstado(EstadoContenido estado) {
        this.estado = estado;
    }

    public int getPuntuacion() {
        return puntuacion;
    }

    public void setPuntuacion(int puntuacion) {
        this.puntuacion = puntuacion;
    }

    public LocalDate getFechaRegistro() {
        return fechaRegistro;
    }

    public void setFechaRegistro(LocalDate fechaRegistro) {
        this.fechaRegistro = fechaRegistro;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Contenido contenido = (Contenido) o;
        return Objects.equals(id, contenido.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return getTipo().getEtiqueta() + ": " + titulo + " (" + anioEstreno + ")";
    }
}
"""

FILES["src/main/java/com/streamtrack/model/Pelicula.java"] = """package com.streamtrack.model;

import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.time.LocalDate;

public class Pelicula extends Contenido {

    private int duracionMinutos;

    public Pelicula() {
        super();
    }

    public Pelicula(Integer id, String titulo, String sinopsis, int anioEstreno,
                    Genero genero, Plataforma plataforma, EstadoContenido estado,
                    int puntuacion, LocalDate fechaRegistro, int duracionMinutos) {
        super(id, titulo, sinopsis, anioEstreno, genero, plataforma, estado, puntuacion, fechaRegistro);
        this.duracionMinutos = duracionMinutos;
    }

    public Pelicula(String titulo, String sinopsis, int anioEstreno,
                    Genero genero, Plataforma plataforma, int duracionMinutos) {
        super(null, titulo, sinopsis, anioEstreno, genero, plataforma, EstadoContenido.PENDIENTE, 0, LocalDate.now());
        this.duracionMinutos = duracionMinutos;
    }

    @Override
    public TipoContenido getTipo() {
        return TipoContenido.PELICULA;
    }

    @Override
    public String getProgresoVisual() {
        return duracionMinutos + " min";
    }

    public int getDuracionMinutos() {
        return duracionMinutos;
    }

    public void setDuracionMinutos(int duracionMinutos) {
        this.duracionMinutos = duracionMinutos;
    }
}
"""

FILES["src/main/java/com/streamtrack/model/Serie.java"] = """package com.streamtrack.model;

import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.time.LocalDate;

public class Serie extends Contenido {

    private int totalTemporadas;
    private int capitulosTotales;
    private int capitulosVistos;

    public Serie() {
        super();
        this.totalTemporadas = 1;
        this.capitulosVistos = 0;
    }

    public Serie(Integer id, String titulo, String sinopsis, int anioEstreno,
                 Genero genero, Plataforma plataforma, EstadoContenido estado,
                 int puntuacion, LocalDate fechaRegistro,
                 int totalTemporadas, int capitulosTotales, int capitulosVistos) {
        super(id, titulo, sinopsis, anioEstreno, genero, plataforma, estado, puntuacion, fechaRegistro);
        this.totalTemporadas = totalTemporadas;
        this.capitulosTotales = capitulosTotales;
        this.capitulosVistos = capitulosVistos;
    }

    public Serie(String titulo, String sinopsis, int anioEstreno,
                 Genero genero, Plataforma plataforma,
                 int totalTemporadas, int capitulosTotales) {
        super(null, titulo, sinopsis, anioEstreno, genero, plataforma, EstadoContenido.PENDIENTE, 0, LocalDate.now());
        this.totalTemporadas = totalTemporadas;
        this.capitulosTotales = capitulosTotales;
        this.capitulosVistos = 0;
    }

    @Override
    public TipoContenido getTipo() {
        return TipoContenido.SERIE;
    }

    @Override
    public String getProgresoVisual() {
        return "Cap. " + capitulosVistos + "/" + capitulosTotales + " (T" + totalTemporadas + ")";
    }

    public int getTotalTemporadas() {
        return totalTemporadas;
    }

    public void setTotalTemporadas(int totalTemporadas) {
        this.totalTemporadas = totalTemporadas;
    }

    public int getCapitulosTotales() {
        return capitulosTotales;
    }

    public void setCapitulosTotales(int capitulosTotales) {
        this.capitulosTotales = capitulosTotales;
    }

    public int getCapitulosVistos() {
        return capitulosVistos;
    }

    public void setCapitulosVistos(int capitulosVistos) {
        this.capitulosVistos = capitulosVistos;
    }
}
"""

FILES["src/main/java/com/streamtrack/util/ValidationException.java"] = """package com.streamtrack.util;

public class ValidationException extends Exception {

    public ValidationException(String message) {
        super(message);
    }

    public ValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}
"""

FILES["src/main/java/com/streamtrack/dao/GeneroDAO.java"] = """package com.streamtrack.dao;

import com.streamtrack.model.Genero;

import java.sql.SQLException;
import java.util.List;

public interface GeneroDAO {

    List<Genero> listarTodos() throws SQLException;

    Genero buscarPorId(int id) throws SQLException;

    Genero guardar(Genero genero) throws SQLException;
}
"""

FILES["src/main/java/com/streamtrack/dao/PlataformaDAO.java"] = """package com.streamtrack.dao;

import com.streamtrack.model.Plataforma;

import java.sql.SQLException;
import java.util.List;

public interface PlataformaDAO {

    List<Plataforma> listarTodos() throws SQLException;

    Plataforma buscarPorId(int id) throws SQLException;

    Plataforma guardar(Plataforma plataforma) throws SQLException;
}
"""

FILES["src/main/java/com/streamtrack/dao/ContenidoDAO.java"] = """package com.streamtrack.dao;

import com.streamtrack.model.Contenido;
import com.streamtrack.model.Pelicula;
import com.streamtrack.model.Serie;
import com.streamtrack.model.enums.EstadoContenido;

import java.sql.SQLException;
import java.util.List;

public interface ContenidoDAO {

    List<Contenido> listarTodos() throws SQLException;

    Contenido buscarPorId(int id) throws SQLException;

    Pelicula guardarPelicula(Pelicula pelicula) throws SQLException;

    Serie guardarSerie(Serie serie) throws SQLException;

    void actualizar(Contenido contenido) throws SQLException;

    void eliminar(int id) throws SQLException;

    void actualizarEstado(int id, EstadoContenido nuevoEstado) throws SQLException;

    boolean existePorTituloYAnio(String titulo, int anio, Integer idExcluir) throws SQLException;
}
"""

FILES["src/main/java/com/streamtrack/dao/mysql/MySQLGeneroDAO.java"] = """package com.streamtrack.dao.mysql;

import com.streamtrack.config.DatabaseConnection;
import com.streamtrack.dao.GeneroDAO;
import com.streamtrack.model.Genero;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class MySQLGeneroDAO implements GeneroDAO {

    @Override
    public List<Genero> listarTodos() throws SQLException {
        String sql = "SELECT id, nombre FROM genero ORDER BY nombre ASC";
        List<Genero> generos = new ArrayList<>();

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                Genero g = new Genero(
                        rs.getInt("id"),
                        rs.getString("nombre")
                );
                generos.add(g);
            }
        }
        return generos;
    }

    @Override
    public Genero buscarPorId(int id) throws SQLException {
        String sql = "SELECT id, nombre FROM genero WHERE id = ?";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, id);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Genero(
                            rs.getInt("id"),
                            rs.getString("nombre")
                    );
                }
            }
        }
        return null;
    }

    @Override
    public Genero guardar(Genero genero) throws SQLException {
        String sql = "INSERT INTO genero (nombre) VALUES (?)";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {

            ps.setString(1, genero.getNombre());
            ps.executeUpdate();

            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    genero.setId(rs.getInt(1));
                }
            }
        }
        return genero;
    }
}
"""

FILES["src/main/java/com/streamtrack/dao/mysql/MySQLPlataformaDAO.java"] = """package com.streamtrack.dao.mysql;

import com.streamtrack.config.DatabaseConnection;
import com.streamtrack.dao.PlataformaDAO;
import com.streamtrack.model.Plataforma;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class MySQLPlataformaDAO implements PlataformaDAO {

    @Override
    public List<Plataforma> listarTodos() throws SQLException {
        String sql = "SELECT id, nombre FROM plataforma ORDER BY nombre ASC";
        List<Plataforma> plataformas = new ArrayList<>();

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                Plataforma p = new Plataforma(
                        rs.getInt("id"),
                        rs.getString("nombre")
                );
                plataformas.add(p);
            }
        }
        return plataformas;
    }

    @Override
    public Plataforma buscarPorId(int id) throws SQLException {
        String sql = "SELECT id, nombre FROM plataforma WHERE id = ?";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, id);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Plataforma(
                            rs.getInt("id"),
                            rs.getString("nombre")
                    );
                }
            }
        }
        return null;
    }

    @Override
    public Plataforma guardar(Plataforma plataforma) throws SQLException {
        String sql = "INSERT INTO plataforma (nombre) VALUES (?)";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {

            ps.setString(1, plataforma.getNombre());
            ps.executeUpdate();

            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    plataforma.setId(rs.getInt(1));
                }
            }
        }
        return plataforma;
    }
}
"""

FILES["src/main/java/com/streamtrack/dao/mysql/MySQLContenidoDAO.java"] = """package com.streamtrack.dao.mysql;

import com.streamtrack.config.DatabaseConnection;
import com.streamtrack.dao.ContenidoDAO;
import com.streamtrack.model.*;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class MySQLContenidoDAO implements ContenidoDAO {

    private static final String BASE_SELECT = \"\"\"
            SELECT 
                c.id, c.titulo, c.sinopsis, c.anio_estreno, c.tipo, c.estado, c.puntuacion, c.fecha_registro,
                g.id AS genero_id, g.nombre AS genero_nombre,
                pl.id AS plataforma_id, pl.nombre AS plataforma_nombre,
                pel.duracion_minutos,
                ser.total_temporadas, ser.capitulos_totales, ser.capitulos_vistos
            FROM contenido c
            INNER JOIN genero g ON c.id_genero = g.id
            INNER JOIN plataforma pl ON c.id_plataforma = pl.id
            LEFT JOIN pelicula pel ON c.id = pel.id_contenido
            LEFT JOIN serie ser ON c.id = ser.id_contenido
            \"\"\";

    @Override
    public List<Contenido> listarTodos() throws SQLException {
        String sql = BASE_SELECT + " ORDER BY c.fecha_registro DESC, c.id DESC";
        List<Contenido> lista = new ArrayList<>();

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                lista.add(mapearFila(rs));
            }
        }
        return lista;
    }

    @Override
    public Contenido buscarPorId(int id) throws SQLException {
        String sql = BASE_SELECT + " WHERE c.id = ?";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, id);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return mapearFila(rs);
                }
            }
        }
        return null;
    }

    @Override
    public Pelicula guardarPelicula(Pelicula pelicula) throws SQLException {
        String sqlContenido = \"\"\"
                INSERT INTO contenido (titulo, sinopsis, anio_estreno, tipo, id_genero, id_plataforma, estado, puntuacion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                \"\"\";
        String sqlPelicula = "INSERT INTO pelicula (id_contenido, duracion_minutos) VALUES (?, ?)";

        try (Connection conn = DatabaseConnection.getConnection()) {
            conn.setAutoCommit(false);
            try {
                int idContenido;
                try (PreparedStatement psContenido = conn.prepareStatement(sqlContenido, Statement.RETURN_GENERATED_KEYS)) {
                    psContenido.setString(1, pelicula.getTitulo());
                    psContenido.setString(2, pelicula.getSinopsis());
                    psContenido.setInt(3, pelicula.getAnioEstreno());
                    psContenido.setString(4, TipoContenido.PELICULA.name());
                    psContenido.setInt(5, pelicula.getGenero().getId());
                    psContenido.setInt(6, pelicula.getPlataforma().getId());
                    psContenido.setString(7, pelicula.getEstado().name());
                    psContenido.setInt(8, pelicula.getPuntuacion());
                    psContenido.setDate(9, Date.valueOf(pelicula.getFechaRegistro() != null ? pelicula.getFechaRegistro() : LocalDate.now()));
                    psContenido.executeUpdate();

                    try (ResultSet rs = psContenido.getGeneratedKeys()) {
                        if (rs.next()) {
                            idContenido = rs.getInt(1);
                            pelicula.setId(idContenido);
                        } else {
                            throw new SQLException("No se pudo obtener el ID generado para la película");
                        }
                    }
                }

                try (PreparedStatement psPelicula = conn.prepareStatement(sqlPelicula)) {
                    psPelicula.setInt(1, idContenido);
                    psPelicula.setInt(2, pelicula.getDuracionMinutos());
                    psPelicula.executeUpdate();
                }

                conn.commit();
                return pelicula;
            } catch (SQLException ex) {
                conn.rollback();
                throw ex;
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }

    @Override
    public Serie guardarSerie(Serie serie) throws SQLException {
        String sqlContenido = \"\"\"
                INSERT INTO contenido (titulo, sinopsis, anio_estreno, tipo, id_genero, id_plataforma, estado, puntuacion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                \"\"\";
        String sqlSerie = \"\"\"
                INSERT INTO serie (id_contenido, total_temporadas, capitulos_totales, capitulos_vistos)
                VALUES (?, ?, ?, ?)
                \"\"\";

        try (Connection conn = DatabaseConnection.getConnection()) {
            conn.setAutoCommit(false);
            try {
                int idContenido;
                try (PreparedStatement psContenido = conn.prepareStatement(sqlContenido, Statement.RETURN_GENERATED_KEYS)) {
                    psContenido.setString(1, serie.getTitulo());
                    psContenido.setString(2, serie.getSinopsis());
                    psContenido.setInt(3, serie.getAnioEstreno());
                    psContenido.setString(4, TipoContenido.SERIE.name());
                    psContenido.setInt(5, serie.getGenero().getId());
                    psContenido.setInt(6, serie.getPlataforma().getId());
                    psContenido.setString(7, serie.getEstado().name());
                    psContenido.setInt(8, serie.getPuntuacion());
                    psContenido.setDate(9, Date.valueOf(serie.getFechaRegistro() != null ? serie.getFechaRegistro() : LocalDate.now()));
                    psContenido.executeUpdate();

                    try (ResultSet rs = psContenido.getGeneratedKeys()) {
                        if (rs.next()) {
                            idContenido = rs.getInt(1);
                            serie.setId(idContenido);
                        } else {
                            throw new SQLException("No se pudo obtener el ID generado para la serie");
                        }
                    }
                }

                try (PreparedStatement psSerie = conn.prepareStatement(sqlSerie)) {
                    psSerie.setInt(1, idContenido);
                    psSerie.setInt(2, serie.getTotalTemporadas());
                    psSerie.setInt(3, serie.getCapitulosTotales());
                    psSerie.setInt(4, serie.getCapitulosVistos());
                    psSerie.executeUpdate();
                }

                conn.commit();
                return serie;
            } catch (SQLException ex) {
                conn.rollback();
                throw ex;
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }

    @Override
    public void actualizar(Contenido contenido) throws SQLException {
        String sqlContenido = \"\"\"
                UPDATE contenido 
                SET titulo = ?, sinopsis = ?, anio_estreno = ?, id_genero = ?, id_plataforma = ?, estado = ?, puntuacion = ?
                WHERE id = ?
                \"\"\";

        try (Connection conn = DatabaseConnection.getConnection()) {
            conn.setAutoCommit(false);
            try {
                try (PreparedStatement ps = conn.prepareStatement(sqlContenido)) {
                    ps.setString(1, contenido.getTitulo());
                    ps.setString(2, contenido.getSinopsis());
                    ps.setInt(3, contenido.getAnioEstreno());
                    ps.setInt(4, contenido.getGenero().getId());
                    ps.setInt(5, contenido.getPlataforma().getId());
                    ps.setString(6, contenido.getEstado().name());
                    ps.setInt(7, contenido.getPuntuacion());
                    ps.setInt(8, contenido.getId());
                    ps.executeUpdate();
                }

                if (contenido instanceof Pelicula pelicula) {
                    String sqlPelicula = "UPDATE pelicula SET duracion_minutos = ? WHERE id_contenido = ?";
                    try (PreparedStatement ps = conn.prepareStatement(sqlPelicula)) {
                        ps.setInt(1, pelicula.getDuracionMinutos());
                        ps.setInt(2, pelicula.getId());
                        ps.executeUpdate();
                    }
                } else if (contenido instanceof Serie serie) {
                    String sqlSerie = \"\"\"
                            UPDATE serie 
                            SET total_temporadas = ?, capitulos_totales = ?, capitulos_vistos = ?
                            WHERE id_contenido = ?
                            \"\"\";
                    try (PreparedStatement ps = conn.prepareStatement(sqlSerie)) {
                        ps.setInt(1, serie.getTotalTemporadas());
                        ps.setInt(2, serie.getCapitulosTotales());
                        ps.setInt(3, serie.getCapitulosVistos());
                        ps.setInt(4, serie.getId());
                        ps.executeUpdate();
                    }
                }

                conn.commit();
            } catch (SQLException ex) {
                conn.rollback();
                throw ex;
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }

    @Override
    public void eliminar(int id) throws SQLException {
        String sql = "DELETE FROM contenido WHERE id = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            ps.executeUpdate();
        }
    }

    @Override
    public void actualizarEstado(int id, EstadoContenido nuevoEstado) throws SQLException {
        String sql = "UPDATE contenido SET estado = ? WHERE id = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, nuevoEstado.name());
            ps.setInt(2, id);
            ps.executeUpdate();
        }
    }

    @Override
    public boolean existePorTituloYAnio(String titulo, int anio, Integer idExcluir) throws SQLException {
        StringBuilder sql = new StringBuilder("SELECT COUNT(*) FROM contenido WHERE LOWER(titulo) = LOWER(?) AND anio_estreno = ?");
        if (idExcluir != null) {
            sql.append(" AND id != ?");
        }

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql.toString())) {

            ps.setString(1, titulo.trim());
            ps.setInt(2, anio);
            if (idExcluir != null) {
                ps.setInt(3, idExcluir);
            }

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1) > 0;
                }
            }
        }
        return false;
    }

    private Contenido mapearFila(ResultSet rs) throws SQLException {
        int id = rs.getInt("id");
        String titulo = rs.getString("titulo");
        String sinopsis = rs.getString("sinopsis");
        int anio = rs.getInt("anio_estreno");
        String tipoStr = rs.getString("tipo");
        String estadoStr = rs.getString("estado");
        int puntuacion = rs.getInt("puntuacion");
        Date fechaReg = rs.getDate("fecha_registro");
        LocalDate fecha = (fechaReg != null) ? fechaReg.toLocalDate() : LocalDate.now();

        Genero genero = new Genero(rs.getInt("genero_id"), rs.getString("genero_nombre"));
        Plataforma plataforma = new Plataforma(rs.getInt("plataforma_id"), rs.getString("plataforma_nombre"));
        EstadoContenido estado = EstadoContenido.valueOf(estadoStr);

        if (TipoContenido.PELICULA.name().equalsIgnoreCase(tipoStr)) {
            int duracion = rs.getInt("duracion_minutos");
            return new Pelicula(id, titulo, sinopsis, anio, genero, plataforma, estado, puntuacion, fecha, duracion);
        } else {
            int temporadas = rs.getInt("total_temporadas");
            int capitulosTotales = rs.getInt("capitulos_totales");
            int capitulosVistos = rs.getInt("capitulos_vistos");
            return new Serie(id, titulo, sinopsis, anio, genero, plataforma, estado, puntuacion, fecha,
                    temporadas, capitulosTotales, capitulosVistos);
        }
    }
}
"""

FILES["src/main/java/com/streamtrack/service/GeneroService.java"] = """package com.streamtrack.service;

import com.streamtrack.dao.GeneroDAO;
import com.streamtrack.model.Genero;

import java.sql.SQLException;
import java.util.List;

public class GeneroService {

    private final GeneroDAO generoDAO;

    public GeneroService(GeneroDAO generoDAO) {
        this.generoDAO = generoDAO;
    }

    public List<Genero> listarTodos() throws SQLException {
        return generoDAO.listarTodos();
    }

    public Genero buscarPorId(int id) throws SQLException {
        return generoDAO.buscarPorId(id);
    }
}
"""

FILES["src/main/java/com/streamtrack/service/PlataformaService.java"] = """package com.streamtrack.service;

import com.streamtrack.dao.PlataformaDAO;
import com.streamtrack.model.Plataforma;

import java.sql.SQLException;
import java.util.List;

public class PlataformaService {

    private final PlataformaDAO plataformaDAO;

    public PlataformaService(PlataformaDAO plataformaDAO) {
        this.plataformaDAO = plataformaDAO;
    }

    public List<Plataforma> listarTodas() throws SQLException {
        return plataformaDAO.listarTodos();
    }

    public Plataforma buscarPorId(int id) throws SQLException {
        return plataformaDAO.buscarPorId(id);
    }
}
"""

FILES["src/main/java/com/streamtrack/service/ContenidoService.java"] = """package com.streamtrack.service;

import com.streamtrack.dao.ContenidoDAO;
import com.streamtrack.model.*;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.util.ValidationException;

import java.sql.SQLException;
import java.time.LocalDate;
import java.util.List;

public class ContenidoService {

    private final ContenidoDAO contenidoDAO;

    public ContenidoService(ContenidoDAO contenidoDAO) {
        this.contenidoDAO = contenidoDAO;
    }

    public List<Contenido> listarCatalogo() throws SQLException {
        return contenidoDAO.listarTodos();
    }

    public Contenido buscarPorId(int id) throws SQLException {
        return contenidoDAO.buscarPorId(id);
    }

    public Pelicula registrarPelicula(String titulo, String sinopsis, int anio,
                                     Genero genero, Plataforma plataforma,
                                     int duracionMinutos) throws ValidationException, SQLException {
        validarCamposComunes(titulo, anio, genero, plataforma, null);

        if (duracionMinutos <= 0) {
            throw new ValidationException("La duración de la película debe ser mayor a 0 minutos.");
        }

        Pelicula pelicula = new Pelicula(titulo.trim(), sinopsis != null ? sinopsis.trim() : "",
                anio, genero, plataforma, duracionMinutos);
        return contenidoDAO.guardarPelicula(pelicula);
    }

    public Serie registrarSerie(String titulo, String sinopsis, int anio,
                                Genero genero, Plataforma plataforma,
                                int totalTemporadas, int capitulosTotales) throws ValidationException, SQLException {
        validarCamposComunes(titulo, anio, genero, plataforma, null);

        if (totalTemporadas <= 0) {
            throw new ValidationException("La serie debe tener al menos 1 temporada.");
        }
        if (capitulosTotales <= 0) {
            throw new ValidationException("La serie debe tener al menos 1 capítulo en total.");
        }

        Serie serie = new Serie(titulo.trim(), sinopsis != null ? sinopsis.trim() : "",
                anio, genero, plataforma, totalTemporadas, capitulosTotales);
        return contenidoDAO.guardarSerie(serie);
    }

    public void cambiarEstado(int idContenido, EstadoContenido nuevoEstado) throws ValidationException, SQLException {
        Contenido contenido = contenidoDAO.buscarPorId(idContenido);
        if (contenido == null) {
            throw new ValidationException("El contenido que intentas actualizar no existe.");
        }
        if (nuevoEstado == null) {
            throw new ValidationException("Debes seleccionar un estado válido.");
        }

        contenidoDAO.actualizarEstado(idContenido, nuevoEstado);
    }

    public void registrarProgresoSerie(int idSerie, int nuevosCapitulosVistos) throws ValidationException, SQLException {
        Contenido contenido = contenidoDAO.buscarPorId(idSerie);
        if (!(contenido instanceof Serie serie)) {
            throw new ValidationException("El contenido no existe o no corresponde a una serie.");
        }

        if (nuevosCapitulosVistos < 0) {
            throw new ValidationException("Los capítulos vistos no pueden ser negativos.");
        }
        if (nuevosCapitulosVistos > serie.getCapitulosTotales()) {
            throw new ValidationException("Los capítulos vistos (" + nuevosCapitulosVistos + 
                    ") no pueden superar el total (" + serie.getCapitulosTotales() + ").");
        }

        serie.setCapitulosVistos(nuevosCapitulosVistos);

        if (nuevosCapitulosVistos == serie.getCapitulosTotales()) {
            serie.setEstado(EstadoContenido.VISTO);
        } else if (nuevosCapitulosVistos > 0 && serie.getEstado() == EstadoContenido.PENDIENTE) {
            serie.setEstado(EstadoContenido.VIENDO);
        }

        contenidoDAO.actualizar(serie);
    }

    public void calificarContenido(int idContenido, int puntuacion) throws ValidationException, SQLException {
        if (puntuacion < 1 || puntuacion > 10) {
            throw new ValidationException("La puntuación debe estar comprendida entre 1 y 10.");
        }

        Contenido contenido = contenidoDAO.buscarPorId(idContenido);
        if (contenido == null) {
            throw new ValidationException("El contenido no existe.");
        }

        if (contenido.getEstado() == EstadoContenido.PENDIENTE) {
            throw new ValidationException("No puedes calificar una obra en estado 'Pendiente'. Debes haber comenzado a verla.");
        }

        contenido.setPuntuacion(puntuacion);
        contenidoDAO.actualizar(contenido);
    }

    public void eliminarContenido(int idContenido) throws ValidationException, SQLException {
        Contenido contenido = contenidoDAO.buscarPorId(idContenido);
        if (contenido == null) {
            throw new ValidationException("El contenido seleccionado no existe.");
        }
        contenidoDAO.eliminar(idContenido);
    }

    private void validarCamposComunes(String titulo, int anio, Genero genero, Plataforma plataforma, Integer idExcluir)
            throws ValidationException, SQLException {
        if (titulo == null || titulo.trim().isEmpty()) {
            throw new ValidationException("El título de la obra no puede estar vacío.");
        }

        int anioActual = LocalDate.now().getYear();
        if (anio < 1895 || anio > anioActual + 2) {
            throw new ValidationException("El año de estreno (" + anio + ") debe estar entre 1895 y " + (anioActual + 2) + ".");
        }

        if (genero == null || genero.getId() == null) {
            throw new ValidationException("Debes asignar un género válido a la obra.");
        }

        if (plataforma == null || plataforma.getId() == null) {
            throw new ValidationException("Debes asignar una plataforma válida a la obra.");
        }

        if (contenidoDAO.existePorTituloYAnio(titulo, anio, idExcluir)) {
            throw new ValidationException("Ya existe una obra registrada con el título '" + titulo + "' y año " + anio + ".");
        }
    }
}
"""

FILES["src/main/java/com/streamtrack/view/panels/CatalogoPanel.java"] = """package com.streamtrack.view.panels;

import com.streamtrack.model.Contenido;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

public class CatalogoPanel extends JPanel {

    private final JTable tablaContenidos;
    private final DefaultTableModel tableModel;
    private final JComboBox<String> comboFiltroTipo;
    private final JComboBox<String> comboFiltroEstado;
    private final JButton btnCambiarEstado;
    private final JButton btnEliminar;
    private final JButton btnNuevo;
    private final JLabel lblContador;

    private final List<Contenido> listaVisible = new ArrayList<>();

    public CatalogoPanel() {
        setLayout(new BorderLayout(15, 15));
        setBorder(BorderFactory.createEmptyBorder(20, 25, 20, 25));

        JPanel topPanel = new JPanel(new BorderLayout(10, 10));

        JPanel leftToolbar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        JLabel lblFiltroTipo = new JLabel("Tipo:");
        comboFiltroTipo = new JComboBox<>(new String[]{"Todos", "Películas", "Series"});

        JLabel lblFiltroEstado = new JLabel("Estado:");
        comboFiltroEstado = new JComboBox<>(new String[]{"Todos", "Pendiente", "Viendo", "Visto", "Abandonado"});

        leftToolbar.add(lblFiltroTipo);
        leftToolbar.add(comboFiltroTipo);
        leftToolbar.add(Box.createHorizontalStrut(10));
        leftToolbar.add(lblFiltroEstado);
        leftToolbar.add(comboFiltroEstado);

        JPanel rightToolbar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        btnCambiarEstado = new JButton("Cambiar Estado");
        btnEliminar = new JButton("Eliminar");
        btnEliminar.setForeground(new Color(230, 80, 80));
        btnNuevo = new JButton("+ Nueva Obra");
        btnNuevo.putClientProperty("JButton.buttonType", "roundRect");

        rightToolbar.add(btnCambiarEstado);
        rightToolbar.add(btnEliminar);
        rightToolbar.add(btnNuevo);

        topPanel.add(leftToolbar, BorderLayout.WEST);
        topPanel.add(rightToolbar, BorderLayout.EAST);
        add(topPanel, BorderLayout.NORTH);

        String[] columnas = {"ID", "Título", "Tipo", "Género", "Plataforma", "Año", "Duración / Progreso", "Estado"};
        tableModel = new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        tablaContenidos = new JTable(tableModel);
        tablaContenidos.setRowHeight(32);
        tablaContenidos.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        tablaContenidos.getTableHeader().setReorderingAllowed(false);
        tablaContenidos.setShowVerticalLines(false);

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(SwingConstants.CENTER);
        tablaContenidos.getColumnModel().getColumn(0).setPreferredWidth(50);
        tablaContenidos.getColumnModel().getColumn(0).setCellRenderer(centerRenderer);
        tablaContenidos.getColumnModel().getColumn(1).setPreferredWidth(220);
        tablaContenidos.getColumnModel().getColumn(2).setPreferredWidth(80);
        tablaContenidos.getColumnModel().getColumn(2).setCellRenderer(centerRenderer);
        tablaContenidos.getColumnModel().getColumn(5).setPreferredWidth(60);
        tablaContenidos.getColumnModel().getColumn(5).setCellRenderer(centerRenderer);
        tablaContenidos.getColumnModel().getColumn(7).setPreferredWidth(100);
        tablaContenidos.getColumnModel().getColumn(7).setCellRenderer(centerRenderer);

        JScrollPane scrollPane = new JScrollPane(tablaContenidos);
        add(scrollPane, BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout());
        lblContador = new JLabel("Mostrando 0 obras");
        lblContador.setForeground(Color.GRAY);
        bottomPanel.add(lblContador, BorderLayout.WEST);
        add(bottomPanel, BorderLayout.SOUTH);
    }

    public void actualizarContenidos(List<Contenido> contenidos) {
        listaVisible.clear();
        tableModel.setRowCount(0);

        if (contenidos != null) {
            for (Contenido c : contenidos) {
                listaVisible.add(c);
                tableModel.addRow(new Object[]{
                        c.getId(),
                        c.getTitulo(),
                        c.getTipo().getEtiqueta(),
                        c.getGenero().getNombre(),
                        c.getPlataforma().getNombre(),
                        c.getAnioEstreno(),
                        c.getProgresoVisual(),
                        c.getEstado().getEtiqueta()
                });
            }
            lblContador.setText("Total de obras en catálogo: " + contenidos.size());
        } else {
            lblContador.setText("Total de obras en catálogo: 0");
        }
    }

    public Integer getContenidoSeleccionadoId() {
        int selectedRow = tablaContenidos.getSelectedRow();
        if (selectedRow >= 0 && selectedRow < listaVisible.size()) {
            return listaVisible.get(selectedRow).getId();
        }
        return null;
    }

    public Contenido getContenidoSeleccionado() {
        int selectedRow = tablaContenidos.getSelectedRow();
        if (selectedRow >= 0 && selectedRow < listaVisible.size()) {
            return listaVisible.get(selectedRow);
        }
        return null;
    }

    public String getFiltroTipo() {
        return (String) comboFiltroTipo.getSelectedItem();
    }

    public String getFiltroEstado() {
        return (String) comboFiltroEstado.getSelectedItem();
    }

    public void addFiltroTipoListener(ActionListener l) {
        comboFiltroTipo.addActionListener(l);
    }

    public void addFiltroEstadoListener(ActionListener l) {
        comboFiltroEstado.addActionListener(l);
    }

    public void addCambiarEstadoListener(ActionListener l) {
        btnCambiarEstado.addActionListener(l);
    }

    public void addEliminarListener(ActionListener l) {
        btnEliminar.addActionListener(l);
    }

    public void addNuevoContenidoListener(ActionListener l) {
        btnNuevo.addActionListener(l);
    }
}
"""

FILES["src/main/java/com/streamtrack/view/panels/FormularioPanel.java"] = """package com.streamtrack.view.panels;

import com.streamtrack.model.Genero;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.enums.TipoContenido;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.time.LocalDate;
import java.util.List;

public class FormularioPanel extends JPanel {

    private final JRadioButton radioPelicula;
    private final JRadioButton radioSerie;
    private final JTextField txtTitulo;
    private final JTextArea txtSinopsis;
    private final JSpinner spinAnio;
    private final JComboBox<Genero> comboGenero;
    private final JComboBox<Plataforma> comboPlataforma;

    private final JSpinner spinDuracion;
    private final JSpinner spinTemporadas;
    private final JSpinner spinCapitulos;

    private final JPanel cardsEspecificas;
    private final CardLayout cardLayoutEspecifico;

    private final JButton btnGuardar;
    private final JButton btnCancelar;

    public FormularioPanel() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createEmptyBorder(20, 40, 20, 40));

        JLabel lblTituloVista = new JLabel("Registrar Nuevo Contenido");
        lblTituloVista.setFont(lblTituloVista.getFont().deriveFont(Font.BOLD, 20f));
        lblTituloVista.setBorder(BorderFactory.createEmptyBorder(0, 0, 15, 0));
        add(lblTituloVista, BorderLayout.NORTH);

        JPanel formContent = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 8, 8, 8);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        int row = 0;

        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Tipo de Obra:"), gbc);

        JPanel tipoPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 15, 0));
        radioPelicula = new JRadioButton("Película", true);
        radioSerie = new JRadioButton("Serie");
        ButtonGroup bgTipo = new ButtonGroup();
        bgTipo.add(radioPelicula);
        bgTipo.add(radioSerie);
        tipoPanel.add(radioPelicula);
        tipoPanel.add(radioSerie);

        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(tipoPanel, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Título:"), gbc);
        txtTitulo = new JTextField();
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(txtTitulo, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Año de Estreno:"), gbc);
        int anioActual = LocalDate.now().getYear();
        spinAnio = new JSpinner(new SpinnerNumberModel(anioActual, 1895, anioActual + 2, 1));
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(spinAnio, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Género:"), gbc);
        comboGenero = new JComboBox<>();
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(comboGenero, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Plataforma:"), gbc);
        comboPlataforma = new JComboBox<>();
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(comboPlataforma, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Detalles específicos:"), gbc);

        cardLayoutEspecifico = new CardLayout();
        cardsEspecificas = new JPanel(cardLayoutEspecifico);

        JPanel panelPelicula = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        panelPelicula.add(new JLabel("Duración (minutos):"));
        spinDuracion = new JSpinner(new SpinnerNumberModel(120, 1, 999, 5));
        panelPelicula.add(spinDuracion);

        JPanel panelSerie = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        panelSerie.add(new JLabel("Temporadas:"));
        spinTemporadas = new JSpinner(new SpinnerNumberModel(1, 1, 99, 1));
        panelSerie.add(spinTemporadas);
        panelSerie.add(Box.createHorizontalStrut(15));
        panelSerie.add(new JLabel("Capítulos Totales:"));
        spinCapitulos = new JSpinner(new SpinnerNumberModel(10, 1, 9999, 1));
        panelSerie.add(spinCapitulos);

        cardsEspecificas.add(panelPelicula, TipoContenido.PELICULA.name());
        cardsEspecificas.add(panelSerie, TipoContenido.SERIE.name());

        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(cardsEspecificas, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        gbc.anchor = GridBagConstraints.NORTHWEST;
        formContent.add(new JLabel("Sinopsis:"), gbc);

        txtSinopsis = new JTextArea(4, 20);
        txtSinopsis.setLineWrap(true);
        txtSinopsis.setWrapStyleWord(true);
        JScrollPane scrollSinopsis = new JScrollPane(txtSinopsis);
        gbc.gridx = 1; gbc.weightx = 1.0;
        gbc.fill = GridBagConstraints.BOTH;
        formContent.add(scrollSinopsis, gbc);

        add(formContent, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 10));
        btnCancelar = new JButton("Cancelar");
        btnGuardar = new JButton("Guardar en Mi Catálogo");
        btnGuardar.putClientProperty("JButton.buttonType", "roundRect");

        buttonPanel.add(btnCancelar);
        buttonPanel.add(btnGuardar);
        add(buttonPanel, BorderLayout.SOUTH);

        radioPelicula.addActionListener(e -> cardLayoutEspecifico.show(cardsEspecificas, TipoContenido.PELICULA.name()));
        radioSerie.addActionListener(e -> cardLayoutEspecifico.show(cardsEspecificas, TipoContenido.SERIE.name()));
    }

    public void cargarGeneros(List<Genero> generos) {
        comboGenero.removeAllItems();
        if (generos != null) {
            for (Genero g : generos) {
                comboGenero.addItem(g);
            }
        }
    }

    public void cargarPlataformas(List<Plataforma> plataformas) {
        comboPlataforma.removeAllItems();
        if (plataformas != null) {
            for (Plataforma p : plataformas) {
                comboPlataforma.addItem(p);
            }
        }
    }

    public void limpiarCampos() {
        txtTitulo.setText("");
        txtSinopsis.setText("");
        spinAnio.setValue(LocalDate.now().getYear());
        radioPelicula.setSelected(true);
        cardLayoutEspecifico.show(cardsEspecificas, TipoContenido.PELICULA.name());
        spinDuracion.setValue(120);
        spinTemporadas.setValue(1);
        spinCapitulos.setValue(10);
        if (comboGenero.getItemCount() > 0) comboGenero.setSelectedIndex(0);
        if (comboPlataforma.getItemCount() > 0) comboPlataforma.setSelectedIndex(0);
    }

    public TipoContenido getTipoSeleccionado() {
        return radioPelicula.isSelected() ? TipoContenido.PELICULA : TipoContenido.SERIE;
    }

    public String getTitulo() {
        return txtTitulo.getText();
    }

    public String getSinopsis() {
        return txtSinopsis.getText();
    }

    public int getAnio() {
        return (Integer) spinAnio.getValue();
    }

    public Genero getGeneroSeleccionado() {
        return (Genero) comboGenero.getSelectedItem();
    }

    public Plataforma getPlataformaSeleccionada() {
        return (Plataforma) comboPlataforma.getSelectedItem();
    }

    public int getDuracionMinutos() {
        return (Integer) spinDuracion.getValue();
    }

    public int getTotalTemporadas() {
        return (Integer) spinTemporadas.getValue();
    }

    public int getCapitulosTotales() {
        return (Integer) spinCapitulos.getValue();
    }

    public void addGuardarListener(ActionListener l) {
        btnGuardar.addActionListener(l);
    }

    public void addCancelarListener(ActionListener l) {
        btnCancelar.addActionListener(l);
    }
}
"""

FILES["src/main/java/com/streamtrack/view/MainFrame.java"] = """package com.streamtrack.view;

import com.streamtrack.view.panels.CatalogoPanel;
import com.streamtrack.view.panels.FormularioPanel;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;

public class MainFrame extends JFrame {

    public static final String VISTA_CATALOGO = "CATALOGO";
    public static final String VISTA_FORMULARIO = "FORMULARIO";

    private final CardLayout cardLayout;
    private final JPanel panelContenedor;

    private final CatalogoPanel catalogoPanel;
    private final FormularioPanel formularioPanel;

    private final JButton btnNavCatalogo;
    private final JButton btnNavNuevo;

    public MainFrame() {
        setTitle("StreamTrack - Gestor Personal de Streaming");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 650);
        setMinimumSize(new Dimension(850, 500));
        setLocationRelativeTo(null);

        JPanel navbar = new JPanel(new BorderLayout(15, 0));
        navbar.setBorder(BorderFactory.createEmptyBorder(12, 25, 12, 25));

        JLabel lblLogo = new JLabel("STREAMTRACK");
        lblLogo.setFont(lblLogo.getFont().deriveFont(Font.BOLD, 18f));
        lblLogo.setForeground(new Color(229, 9, 20));

        JPanel navButtons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        btnNavCatalogo = new JButton("Catálogo");
        btnNavNuevo = new JButton("+ Agregar Obra");
        btnNavNuevo.putClientProperty("JButton.buttonType", "roundRect");

        navButtons.add(btnNavCatalogo);
        navButtons.add(btnNavNuevo);

        navbar.add(lblLogo, BorderLayout.WEST);
        navbar.add(navButtons, BorderLayout.EAST);
        add(navbar, BorderLayout.NORTH);

        cardLayout = new CardLayout();
        panelContenedor = new JPanel(cardLayout);

        catalogoPanel = new CatalogoPanel();
        formularioPanel = new FormularioPanel();

        panelContenedor.add(catalogoPanel, VISTA_CATALOGO);
        panelContenedor.add(formularioPanel, VISTA_FORMULARIO);

        add(panelContenedor, BorderLayout.CENTER);
    }

    public void mostrarVista(String nombreVista) {
        cardLayout.show(panelContenedor, nombreVista);
    }

    public CatalogoPanel getCatalogoPanel() {
        return catalogoPanel;
    }

    public FormularioPanel getFormularioPanel() {
        return formularioPanel;
    }

    public void addNavCatalogoListener(ActionListener l) {
        btnNavCatalogo.addActionListener(l);
    }

    public void addNavNuevoListener(ActionListener l) {
        btnNavNuevo.addActionListener(l);
    }
}
"""

FILES["src/main/java/com/streamtrack/controller/CatalogoController.java"] = """package com.streamtrack.controller;

import com.streamtrack.model.Contenido;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;
import com.streamtrack.service.ContenidoService;
import com.streamtrack.util.ValidationException;
import com.streamtrack.view.panels.CatalogoPanel;

import javax.swing.*;
import java.util.List;
import java.util.stream.Collectors;

public class CatalogoController {

    private final CatalogoPanel vista;
    private final ContenidoService contenidoService;
    private final MainController mainController;

    private List<Contenido> cacheCatalogoCompleto;

    public CatalogoController(CatalogoPanel vista, ContenidoService contenidoService, MainController mainController) {
        this.vista = vista;
        this.contenidoService = contenidoService;
        this.mainController = mainController;

        inicializarEventos();
    }

    private void inicializarEventos() {
        vista.addFiltroTipoListener(e -> aplicarFiltros());
        vista.addFiltroEstadoListener(e -> aplicarFiltros());

        vista.addCambiarEstadoListener(e -> onCambiarEstado());
        vista.addEliminarListener(e -> onEliminar());
        vista.addNuevoContenidoListener(e -> mainController.mostrarFormulario());
    }

    public void recargarCatalogo() {
        try {
            cacheCatalogoCompleto = contenidoService.listarCatalogo();
            aplicarFiltros();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista,
                    "Error al cargar el catálogo desde la base de datos: " + ex.getMessage(),
                    "Error de Datos", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void aplicarFiltros() {
        if (cacheCatalogoCompleto == null) {
            return;
        }

        String filtroTipo = vista.getFiltroTipo();
        String filtroEstado = vista.getFiltroEstado();

        List<Contenido> filtrados = cacheCatalogoCompleto.stream()
                .filter(c -> {
                    if ("Películas".equalsIgnoreCase(filtroTipo)) {
                        return c.getTipo() == TipoContenido.PELICULA;
                    } else if ("Series".equalsIgnoreCase(filtroTipo)) {
                        return c.getTipo() == TipoContenido.SERIE;
                    }
                    return true;
                })
                .filter(c -> {
                    if (!"Todos".equalsIgnoreCase(filtroEstado)) {
                        return c.getEstado().getEtiqueta().equalsIgnoreCase(filtroEstado);
                    }
                    return true;
                })
                .collect(Collectors.toList());

        vista.actualizarContenidos(filtrados);
    }

    private void onCambiarEstado() {
        Integer idSeleccionado = vista.getContenidoSeleccionadoId();
        if (idSeleccionado == null) {
            JOptionPane.showMessageDialog(vista,
                    "Por favor, selecciona una obra de la lista para cambiar su estado.",
                    "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        EstadoContenido[] opciones = EstadoContenido.values();
        EstadoContenido nuevoEstado = (EstadoContenido) JOptionPane.showInputDialog(
                vista,
                "Selecciona el nuevo estado:",
                "Actualizar Estado",
                JOptionPane.QUESTION_MESSAGE,
                null,
                opciones,
                vista.getContenidoSeleccionado().getEstado()
        );

        if (nuevoEstado != null) {
            try {
                contenidoService.cambiarEstado(idSeleccionado, nuevoEstado);
                recargarCatalogo();
                JOptionPane.showMessageDialog(vista,
                        "Estado actualizado a: " + nuevoEstado.getEtiqueta(),
                        "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } catch (ValidationException ve) {
                JOptionPane.showMessageDialog(vista, ve.getMessage(), "Regla de Negocio", JOptionPane.WARNING_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(vista, "Error al actualizar estado: " + ex.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void onEliminar() {
        Integer idSeleccionado = vista.getContenidoSeleccionadoId();
        if (idSeleccionado == null) {
            JOptionPane.showMessageDialog(vista,
                    "Por favor, selecciona una obra de la lista para eliminarla.",
                    "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Contenido seleccionado = vista.getContenidoSeleccionado();
        int confirm = JOptionPane.showConfirmDialog(
                vista,
                "¿Estás seguro de que deseas eliminar '" + seleccionado.getTitulo() + "' de tu catálogo?",
                "Confirmar Eliminación",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.WARNING_MESSAGE
        );

        if (confirm == JOptionPane.YES_OPTION) {
            try {
                contenidoService.eliminarContenido(idSeleccionado);
                recargarCatalogo();
                JOptionPane.showMessageDialog(vista,
                        "Obra eliminada correctamente.",
                        "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(vista,
                        "Error al eliminar la obra: " + ex.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}
"""

FILES["src/main/java/com/streamtrack/controller/FormularioController.java"] = """package com.streamtrack.controller;

import com.streamtrack.model.Genero;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.enums.TipoContenido;
import com.streamtrack.service.ContenidoService;
import com.streamtrack.service.GeneroService;
import com.streamtrack.service.PlataformaService;
import com.streamtrack.util.ValidationException;
import com.streamtrack.view.panels.FormularioPanel;

import javax.swing.*;
import java.util.List;

public class FormularioController {

    private final FormularioPanel vista;
    private final ContenidoService contenidoService;
    private final GeneroService generoService;
    private final PlataformaService plataformaService;
    private final MainController mainController;

    public FormularioController(FormularioPanel vista,
                                ContenidoService contenidoService,
                                GeneroService generoService,
                                PlataformaService plataformaService,
                                MainController mainController) {
        this.vista = vista;
        this.contenidoService = contenidoService;
        this.generoService = generoService;
        this.plataformaService = plataformaService;
        this.mainController = mainController;

        inicializarEventos();
    }

    private void inicializarEventos() {
        vista.addGuardarListener(e -> onGuardar());
        vista.addCancelarListener(e -> onCancelar());
    }

    public void prepararFormulario() {
        try {
            List<Genero> generos = generoService.listarTodos();
            List<Plataforma> plataformas = plataformaService.listarTodas();

            vista.cargarGeneros(generos);
            vista.cargarPlataformas(plataformas);
            vista.limpiarCampos();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista,
                    "Error al cargar catálogos de géneros y plataformas: " + ex.getMessage(),
                    "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void onGuardar() {
        TipoContenido tipo = vista.getTipoSeleccionado();
        String titulo = vista.getTitulo();
        String sinopsis = vista.getSinopsis();
        int anio = vista.getAnio();
        Genero genero = vista.getGeneroSeleccionado();
        Plataforma plataforma = vista.getPlataformaSeleccionada();

        try {
            if (tipo == TipoContenido.PELICULA) {
                int duracion = vista.getDuracionMinutos();
                contenidoService.registrarPelicula(titulo, sinopsis, anio, genero, plataforma, duracion);
            } else {
                int temporadas = vista.getTotalTemporadas();
                int capitulos = vista.getCapitulosTotales();
                contenidoService.registrarSerie(titulo, sinopsis, anio, genero, plataforma, temporadas, capitulos);
            }

            JOptionPane.showMessageDialog(vista,
                    "¡Obra registrada exitosamente en tu catálogo!",
                    "Guardado", JOptionPane.INFORMATION_MESSAGE);

            vista.limpiarCampos();
            mainController.mostrarCatalogo();

        } catch (ValidationException ve) {
            JOptionPane.showMessageDialog(vista,
                    ve.getMessage(),
                    "Validación", JOptionPane.WARNING_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista,
                    "Ocurrió un error inesperado al registrar la obra: " + ex.getMessage(),
                    "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void onCancelar() {
        vista.limpiarCampos();
        mainController.mostrarCatalogo();
    }
}
"""

FILES["src/main/java/com/streamtrack/controller/MainController.java"] = """package com.streamtrack.controller;

import com.streamtrack.service.ContenidoService;
import com.streamtrack.service.GeneroService;
import com.streamtrack.service.PlataformaService;
import com.streamtrack.view.MainFrame;

public class MainController {

    private final MainFrame mainFrame;
    private final CatalogoController catalogoController;
    private final FormularioController formularioController;

    public MainController(MainFrame mainFrame,
                          ContenidoService contenidoService,
                          GeneroService generoService,
                          PlataformaService plataformaService) {
        this.mainFrame = mainFrame;

        this.catalogoController = new CatalogoController(
                mainFrame.getCatalogoPanel(),
                contenidoService,
                this
        );

        this.formularioController = new FormularioController(
                mainFrame.getFormularioPanel(),
                contenidoService,
                generoService,
                plataformaService,
                this
        );

        inicializarNavegacion();
    }

    private void inicializarNavegacion() {
        mainFrame.addNavCatalogoListener(e -> mostrarCatalogo());
        mainFrame.addNavNuevoListener(e -> mostrarFormulario());
    }

    public void iniciar() {
        mostrarCatalogo();
        mainFrame.setVisible(true);
    }

    public void mostrarCatalogo() {
        catalogoController.recargarCatalogo();
        mainFrame.mostrarVista(MainFrame.VISTA_CATALOGO);
    }

    public void mostrarFormulario() {
        formularioController.prepararFormulario();
        mainFrame.mostrarVista(MainFrame.VISTA_FORMULARIO);
    }
}
"""

FILES["src/main/java/com/streamtrack/Main.java"] = """package com.streamtrack;

import com.formdev.flatlaf.FlatDarkLaf;
import com.streamtrack.controller.MainController;
import com.streamtrack.dao.ContenidoDAO;
import com.streamtrack.dao.GeneroDAO;
import com.streamtrack.dao.PlataformaDAO;
import com.streamtrack.dao.mysql.MySQLContenidoDAO;
import com.streamtrack.dao.mysql.MySQLGeneroDAO;
import com.streamtrack.dao.mysql.MySQLPlataformaDAO;
import com.streamtrack.service.ContenidoService;
import com.streamtrack.service.GeneroService;
import com.streamtrack.service.PlataformaService;
import com.streamtrack.view.MainFrame;

import javax.swing.*;

public class Main {

    public static void main(String[] args) {
        try {
            UIManager.put("Button.arc", 10);
            UIManager.put("Component.arc", 8);
            UIManager.put("ProgressBar.arc", 8);
            UIManager.put("TextComponent.arc", 8);
            FlatDarkLaf.setup();
        } catch (Exception ex) {
            System.err.println("No se pudo inicializar FlatLaf: " + ex.getMessage());
        }

        SwingUtilities.invokeLater(() -> {
            try {
                GeneroDAO generoDAO = new MySQLGeneroDAO();
                PlataformaDAO plataformaDAO = new MySQLPlataformaDAO();
                ContenidoDAO contenidoDAO = new MySQLContenidoDAO();

                GeneroService generoService = new GeneroService(generoDAO);
                PlataformaService plataformaService = new PlataformaService(plataformaDAO);
                ContenidoService contenidoService = new ContenidoService(contenidoDAO);

                MainFrame mainFrame = new MainFrame();

                MainController mainController = new MainController(
                        mainFrame,
                        contenidoService,
                        generoService,
                        plataformaService
                );

                mainController.iniciar();

            } catch (Exception e) {
                JOptionPane.showMessageDialog(null,
                        "Error crítico al iniciar la aplicación:\\n" + e.getMessage(),
                        "Error Fatal", JOptionPane.ERROR_MESSAGE);
                e.printStackTrace();
            }
        });
    }
}
"""

FILES["src/test/java/com/streamtrack/config/DatabaseConnectionTest.java"] = """package com.streamtrack.config;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.sql.Connection;

import static org.junit.jupiter.api.Assertions.*;

class DatabaseConnectionTest {

    @Test
    @DisplayName("Debe conectar exitosamente a la base de datos MySQL streamtrack")
    void testGetConnection() {
        assertDoesNotThrow(() -> {
            try (Connection conn = DatabaseConnection.getConnection()) {
                assertNotNull(conn, "La conexión no debe ser nula");
                assertFalse(conn.isClosed(), "La conexión debe estar abierta");
            }
        });
    }
}
"""

FILES["src/test/java/com/streamtrack/dao/DAOTest.java"] = """package com.streamtrack.dao;

import com.streamtrack.dao.mysql.MySQLContenidoDAO;
import com.streamtrack.dao.mysql.MySQLGeneroDAO;
import com.streamtrack.dao.mysql.MySQLPlataformaDAO;
import com.streamtrack.model.Contenido;
import com.streamtrack.model.Genero;
import com.streamtrack.model.Pelicula;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.Serie;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class DAOTest {

    private ContenidoDAO contenidoDAO;
    private GeneroDAO generoDAO;
    private PlataformaDAO plataformaDAO;

    @BeforeEach
    void setUp() {
        contenidoDAO = new MySQLContenidoDAO();
        generoDAO = new MySQLGeneroDAO();
        plataformaDAO = new MySQLPlataformaDAO();
    }

    @Test
    @DisplayName("Debe listar géneros y plataformas precargados")
    void testListarGenerosYPlataformas() throws Exception {
        List<Genero> generos = generoDAO.listarTodos();
        assertFalse(generos.isEmpty(), "Debe haber géneros registrados");

        List<Plataforma> plataformas = plataformaDAO.listarTodos();
        assertFalse(plataformas.isEmpty(), "Debe haber plataformas registradas");
    }

    @Test
    @DisplayName("Debe guardar, consultar y eliminar una Película polimórficamente")
    void testCrudPelicula() throws Exception {
        Genero genero = generoDAO.listarTodos().get(0);
        Plataforma plataforma = plataformaDAO.listarTodos().get(0);

        Pelicula pelicula = new Pelicula("Test Inception", "Sueños dentro de sueños", 2010, genero, plataforma, 148);
        Pelicula guardada = contenidoDAO.guardarPelicula(pelicula);

        assertNotNull(guardada.getId(), "El ID debe ser generado");

        Contenido encontrado = contenidoDAO.buscarPorId(guardada.getId());
        assertNotNull(encontrado);
        assertInstanceOf(Pelicula.class, encontrado);
        assertEquals(TipoContenido.PELICULA, encontrado.getTipo());
        assertEquals("148 min", encontrado.getProgresoVisual());

        contenidoDAO.eliminar(guardada.getId());
        assertNull(contenidoDAO.buscarPorId(guardada.getId()));
    }

    @Test
    @DisplayName("Debe guardar y actualizar estado de una Serie")
    void testCrudSerie() throws Exception {
        Genero genero = generoDAO.listarTodos().get(0);
        Plataforma plataforma = plataformaDAO.listarTodos().get(0);

        Serie serie = new Serie("Test Dark", "Viajes en el tiempo", 2017, genero, plataforma, 3, 26);
        Serie guardada = contenidoDAO.guardarSerie(serie);

        assertNotNull(guardada.getId());

        contenidoDAO.actualizarEstado(guardada.getId(), EstadoContenido.VIENDO);
        Contenido actualizada = contenidoDAO.buscarPorId(guardada.getId());
        assertEquals(EstadoContenido.VIENDO, actualizada.getEstado());

        contenidoDAO.eliminar(guardada.getId());
        assertNull(contenidoDAO.buscarPorId(guardada.getId()));
    }
}
"""

FILES["src/test/java/com/streamtrack/service/ContenidoServiceTest.java"] = """package com.streamtrack.service;

import com.streamtrack.dao.mysql.MySQLContenidoDAO;
import com.streamtrack.dao.mysql.MySQLGeneroDAO;
import com.streamtrack.dao.mysql.MySQLPlataformaDAO;
import com.streamtrack.model.Genero;
import com.streamtrack.model.Pelicula;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.Serie;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.util.ValidationException;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ContenidoServiceTest {

    private ContenidoService contenidoService;
    private Genero generoPrueba;
    private Plataforma plataformaPrueba;
    private final List<Integer> idsParaLimpiar = new ArrayList<>();

    @BeforeEach
    void setUp() throws Exception {
        contenidoService = new ContenidoService(new MySQLContenidoDAO());
        generoPrueba = new MySQLGeneroDAO().listarTodos().get(0);
        plataformaPrueba = new MySQLPlataformaDAO().listarTodos().get(0);
    }

    @AfterEach
    void tearDown() {
        for (Integer id : idsParaLimpiar) {
            try {
                contenidoService.eliminarContenido(id);
            } catch (Exception ignored) {
            }
        }
        idsParaLimpiar.clear();
    }

    @Test
    @DisplayName("Debe rechazar el registro de película con título vacío")
    void testValidacionTituloVacio() {
        ValidationException ex = assertThrows(ValidationException.class, () ->
                contenidoService.registrarPelicula("   ", "Sinopsis", 2020, generoPrueba, plataformaPrueba, 120));
        assertTrue(ex.getMessage().contains("título"));
    }

    @Test
    @DisplayName("Debe rechazar el registro de película con año inválido")
    void testValidacionAnioInvalido() {
        ValidationException ex = assertThrows(ValidationException.class, () ->
                contenidoService.registrarPelicula("Cine Antiguo", "Sinopsis", 1800, generoPrueba, plataformaPrueba, 120));
        assertTrue(ex.getMessage().contains("año"));
    }

    @Test
    @DisplayName("Debe rechazar calificar una obra en estado PENDIENTE")
    void testRechazoCalificarPendiente() throws Exception {
        Pelicula p = contenidoService.registrarPelicula("Interstellar Test", "Espacio", 2014, generoPrueba, plataformaPrueba, 169);
        idsParaLimpiar.add(p.getId());

        assertEquals(EstadoContenido.PENDIENTE, p.getEstado());

        ValidationException ex = assertThrows(ValidationException.class, () ->
                contenidoService.calificarContenido(p.getId(), 9));
        assertTrue(ex.getMessage().contains("Pendiente"));
    }

    @Test
    @DisplayName("Debe cambiar estado automáticamente a VISTO cuando la serie se completa")
    void testTransicionAutomaticaSerie() throws Exception {
        Serie s = contenidoService.registrarSerie("Chernobyl Test", "Drama nuclear", 2019, generoPrueba, plataformaPrueba, 1, 5);
        idsParaLimpiar.add(s.getId());

        contenidoService.registrarProgresoSerie(s.getId(), 5);

        Serie actualizada = (Serie) contenidoService.buscarPorId(s.getId());
        assertEquals(5, actualizada.getCapitulosVistos());
        assertEquals(EstadoContenido.VISTO, actualizada.getEstado());
    }
}
"""

FILES["README.md"] = """# StreamTrack 🎬

**StreamTrack** es una aplicación didáctica de escritorio desarrollada en **Java 17+**, **Swing**, **FlatLaf** y persistencia manual directa con **MySQL JDBC**.

## 🚀 Ejecución

En el directorio raíz del proyecto (`streamtrack`):
```bash
mvn compile exec:java
```
"""

def main():
    print("Iniciando restauración de archivos...")
    for rel_path, content in FILES.items():
        abs_path = os.path.join(BASE_DIR, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Escrito: {rel_path} ({len(content)} caracteres)")
    
    print("\\nInicializando Git para proteger el repositorio...")
    os.chdir(BASE_DIR)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.name", "StreamTrack Developer"], check=True)
    subprocess.run(["git", "config", "user.email", "developer@streamtrack.local"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "StreamTrack MVP commit inicial seguro"], check=True)
    print("Git inicializado y commit creado exitosamente.")

if __name__ == "__main__":
    main()
