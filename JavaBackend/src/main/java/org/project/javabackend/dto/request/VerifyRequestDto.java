package org.project.javabackend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Builder;

@Builder
public record VerifyRequestDto(
        @Email(message = "please provide the email correctly")
        @NotBlank(message = "email is mandatory to login")
        String email,

        @NotBlank(message = "please provide the otp")
        String otp

) {}
