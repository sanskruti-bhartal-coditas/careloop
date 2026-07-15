package org.project.javabackend.dto.request;

import jakarta.persistence.Column;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Builder;
import org.springframework.format.annotation.NumberFormat;

@Builder
public record PatientProfileRequestDto(

        @NotNull(message = "please provide the user id")
        Long id,

        @NotBlank(message = "please provide the first name")
        String firstName,

        String lastName,

        @NotBlank(message = "please provide the phone number")
        @NumberFormat(style = NumberFormat.Style.NUMBER)
        @Size(min = 10, max = 10)
        String phone,

        Double weight,

        Double height,

        Short age

) {
}
