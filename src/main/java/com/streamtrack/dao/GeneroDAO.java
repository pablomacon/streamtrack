package com.streamtrack.dao;

import com.streamtrack.model.Genero;

import java.sql.SQLException;
import java.util.List;

public interface GeneroDAO {

    List<Genero> listarTodos() throws SQLException;

    Genero buscarPorId(int id) throws SQLException;

    Genero guardar(Genero genero) throws SQLException;
}
