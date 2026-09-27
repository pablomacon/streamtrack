package com.streamtrack.service;

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
