package com.streamtrack.dao.mysql;

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
