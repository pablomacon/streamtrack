package com.streamtrack.service;

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
