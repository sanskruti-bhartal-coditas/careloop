package org.project.javabackend.dto.request;

import org.springframework.http.HttpStatus;

public record GenericResponse(
        HttpStatus status,
        String message
) {
}
