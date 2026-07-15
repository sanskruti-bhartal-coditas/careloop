package org.project.javabackend.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class AppointmentDocument {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String documentUrl;

    private String documentType;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    // mapping

    @ManyToOne
    private PatientAppointment patientAppointment;


}
