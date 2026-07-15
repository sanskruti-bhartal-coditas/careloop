package org.project.javabackend.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.project.javabackend.enums.ReviewerName;

import java.time.LocalDateTime;

@Entity
@Table(name = "panel_review")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PanelReview {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "appointment_id", nullable = false)
    private PatientAppointment appointment;

    @Enumerated(EnumType.STRING)
    @Column(name = "reviewer_name", nullable = false)
    private ReviewerName reviewerName;

    @Column(columnDefinition = "TEXT")
    private String findings;



    @Column(name = "error_message")
    private String errorMessage;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}