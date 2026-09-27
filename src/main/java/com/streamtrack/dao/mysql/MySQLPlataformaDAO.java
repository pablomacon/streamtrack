package com.streamtrack.dao.mysql;

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
