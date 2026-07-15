package org.project.javabackend.dto.response;

import org.springframework.http.HttpStatus;

public record GenericResponse(
        HttpStatus status,
        String message
) {
}
