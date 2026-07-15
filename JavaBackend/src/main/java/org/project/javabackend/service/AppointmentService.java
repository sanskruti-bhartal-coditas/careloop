package org.project.javabackend.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.dto.request.AppointmentRequestDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.entity.PatientAppointment;
import org.project.javabackend.repo.AppointmentRepo;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class AppointmentService {

    private final AppointmentRepo appointmentRepo;


    public GenericResponse createAppointment(AppointmentRequestDto appointmentRequestDto) {

        log.info("creating a new appointment");
        PatientAppointment appointment = PatientAppointment.builder()
                .appointmentType(appointmentRequestDto.appointmentType())
                .description(appointmentRequestDto.description())
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .disease(appointmentRequestDto.disease())
                .build();

        appointmentRepo.save(appointment);

        log.info("created a new appointment with the id : {}",appointment.getId());

        return new GenericResponse(HttpStatus.OK,"new appointment is successfully created");
    }
}
