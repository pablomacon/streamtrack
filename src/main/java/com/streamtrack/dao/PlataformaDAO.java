package com.streamtrack.dao;

import com.streamtrack.model.Plataforma;

import java.sql.SQLException;
import java.util.List;

public interface PlataformaDAO {

    List<Plataforma> listarTodos() throws SQLException;

    Plataforma buscarPorId(int id) throws SQLException;

    Plataforma guardar(Plataforma plataforma) throws SQLException;
}
