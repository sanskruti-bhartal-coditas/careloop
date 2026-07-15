package org.project.javabackend.dto.response;


import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.validation.constraints.NotBlank;
import org.project.javabackend.entity.AppointmentDocument;
import org.project.javabackend.entity.PatientDetails;
import org.project.javabackend.enums.AppointmentPriority;

import java.time.LocalDateTime;
import java.util.List;

public record AppointmentResponseDto(


        String appointmentType,

        String disease,

        String description,

        String summary,

        AppointmentPriority priority,

        LocalDateTime createdAt,

        LocalDateTime updatedAt,

        String appointmentStatus,

        // mapping
        List<Long>appointmentDocumentList

) {
}
