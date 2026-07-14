package org.project.javabackend.entity;

import jakarta.persistence.*;
import lombok.*;
import org.project.javabackend.enums.AppointmentPriority;
import org.project.javabackend.enums.AppointmentType;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class PatientAppointment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    private AppointmentType appointmentType;

    private String disease;

    private String description;

    private String  summary;

    @Enumerated(EnumType.STRING)
    private AppointmentPriority priority;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    // mapping
    @ManyToOne
    private PatientDetails patientDetails;

    @OneToMany(mappedBy = "patientAppointment")
    private List<AppointmentDocument> appointmentDocumentList;


    // helper
    public void addDocument(AppointmentDocument appointmentDocument){
        if(appointmentDocumentList==null) appointmentDocumentList = new ArrayList<>();
        appointmentDocumentList.add(appointmentDocument);
        appointmentDocument.setPatientAppointment(this);
    }



}
