package org.project.javabackend.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record OtpRequest (

        @Email(message = "please provide the email correctly")
        @NotBlank(message = "email is mandatory to login")
        String email

){
}
