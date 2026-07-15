package org.project.javabackend.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "panel_summary")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PanelSummary {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "appointment_id", nullable = false)
    private PatientAppointment appointment;

    @Column(name = "summary_text", columnDefinition = "TEXT")
    private String summaryText;

    @Column(name = "missing_items", columnDefinition = "TEXT")
    private String missingItems;

    @Column(name = "suggested_priority")
    private String suggestedPriority;

    @Column(name = "consistency_flags", columnDefinition = "TEXT")
    private String consistencyFlags;

    @Column(name = "raw_findings", columnDefinition = "TEXT")
    private String rawFindings;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}