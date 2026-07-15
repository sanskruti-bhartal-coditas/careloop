package org.project.javabackend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.project.javabackend.enums.Role;

public record AccountRequestDto(

        @Email(message = "please provide the email correctly")
        @NotBlank(message = "email is mandatory to login")
        String email,

        @NotNull(message = "must provide the type of the user")
        Role role

) {
}
