package org.project.javabackend.dto.request;

import jakarta.validation.constraints.NotBlank;

public record AppointmentTypeRequestDto(

        @NotBlank(message = "please give me the proper appointment type")
        String type
) {
}
