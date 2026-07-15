package org.project.javabackend.dto.request;

import jakarta.validation.constraints.NotBlank;

public record AppointmentRequestDto (

        @NotBlank(message = "please provide the type of the appointment")
        String appointmentType,


         String disease,

         @NotBlank(message = "please describe the problem")
         String description

){
}
