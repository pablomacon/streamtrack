package com.streamtrack.dao.mysql;

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

    private static final String BASE_SELECT = """
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
            """;

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
        String sqlContenido = """
                INSERT INTO contenido (titulo, sinopsis, anio_estreno, tipo, id_genero, id_plataforma, estado, puntuacion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;
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
        String sqlContenido = """
                INSERT INTO contenido (titulo, sinopsis, anio_estreno, tipo, id_genero, id_plataforma, estado, puntuacion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;
        String sqlSerie = """
                INSERT INTO serie (id_contenido, total_temporadas, capitulos_totales, capitulos_vistos)
                VALUES (?, ?, ?, ?)
                """;

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
        String sqlContenido = """
                UPDATE contenido 
                SET titulo = ?, sinopsis = ?, anio_estreno = ?, id_genero = ?, id_plataforma = ?, estado = ?, puntuacion = ?
                WHERE id = ?
                """;

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
                    String sqlSerie = """
                            UPDATE serie 
                            SET total_temporadas = ?, capitulos_totales = ?, capitulos_vistos = ?
                            WHERE id_contenido = ?
                            """;
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
