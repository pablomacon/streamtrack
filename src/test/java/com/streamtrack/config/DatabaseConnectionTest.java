package com.streamtrack.config;

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
